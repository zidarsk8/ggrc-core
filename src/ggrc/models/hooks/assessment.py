# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
  Assessment generator hooks

  We are applying assessment template properties and make
  new relationships and custom attributes
"""
import collections
import itertools
import logging
import urlparse
import html2text

from sqlalchemy import orm

from ggrc import db
from ggrc import access_control
from ggrc import settings
from ggrc import utils
from ggrc.integrations import issues
from ggrc.integrations import integrations_errors
from ggrc.login import get_current_user_id
from ggrc.models import all_models
from ggrc.models import exceptions
from ggrc.models.hooks import common
from ggrc.services import signals

logger = logging.getLogger(__name__)


_ISSUE_URL_TMPL = settings.ISSUE_TRACKER_BUG_URL_TMPL or 'http://issue/%s'

_ISSUE_TRACKER_ENABLED = bool(settings.ISSUE_TRACKER_ENABLED)
if not _ISSUE_TRACKER_ENABLED:
  logger.debug('IssueTracker integration is disabled.')

_ASSESSMENT_MODEL_NAME = 'Assessment'
_ASSESSMENT_TMPL_MODEL_NAME = 'AssessmentTemplate'

# mapping of model field name to API property name
_ISSUE_TRACKER_UPDATE_FIELDS = (
    ('title', 'title'),
    ('issue_priority', 'priority'),
    ('issue_severity', 'severity'),
    ('component_id', 'component_id'),
)

_STATUS_CHANGE_COMMENT_TMPL = (
    'The status of this bug was automatically synced to reflect current GGRC '
    'assessment status. Current status of related GGRC Assessment is %s. '
    'Use the following to link to get information from the GGRC Assessment '
    'on why the status may have changed. '
    'Link - %s'
)

_COMMENT_TMPL = (
    'A new comment is added by %s to the Assessment: %s. '
    'Use the following to link to get more information from the '
    'GGRC Assessment. Link - %s'
)

_ARCHIVED_TMPL = (
    'Assessment has been archived. Changes to this GGRC Assessment will '
    'not be tracked within this bug until Assessment is unlocked.'
)

_UNARCHIVED_TMPL = (
    'Assessment has been unarchived. Changes to this GGRC Assessment will '
    'be tracked within this bug.'
)

_ENABLED_TMPL = (
    'Changes to this GGRC Assessment will be tracked within this bug.'
)

_DISABLED_TMPL = (
    'Changes to this GGRC Assessment will no longer be '
    'tracked within this bug.'
)

# Status values maps from GGRC to IssueTracker.
_STATUSES = {
    'Not Started': 'ASSIGNED',
    'In Progress': 'ASSIGNED',
    'In Review': 'FIXED',
    'Rework Needed': 'ASSIGNED',
    'Completed': 'VERIFIED',
    'Deprecated': 'OBSOLETE',
}

# Status transitions map for assessment without verifier.
_NO_VERIFIER_STATUSES = {
    # (from_status, to_status): 'issue_tracker_status'
    ('Not Started', 'Completed'): 'VERIFIED',
    ('In Progress', 'Completed'): 'VERIFIED',

    ('Completed', 'In Progress'): 'ASSIGNED',
    ('Deprecated', 'In Progress'): 'ASSIGNED',

    ('Completed', 'Not Started'): 'ASSIGNED',
    ('Deprecated', 'Not Started'): 'ASSIGNED',

    ('Not Started', 'Deprecated'): 'OBSOLETE',
    ('In Progress', 'Deprecated'): 'OBSOLETE',
    ('Completed', 'Deprecated'): 'OBSOLETE',
}

# Status transitions map for assessment with verifier.
_VERIFIER_STATUSES = {
    # (from_status, to_status, verified): 'issue_tracker_status'
    # When verified is True 'Completed' means 'Completed and Verified'.

    # State: FIXED
    ('Not Started', 'In Review', False): 'FIXED',
    ('In Progress', 'In Review', False): 'FIXED',
    ('Rework Needed', 'In Review', False): 'FIXED',
    ('Completed', 'In Review', True): 'FIXED',
    ('Deprecated', 'In Review', False): 'FIXED',

    # State: ASSIGNED
    ('In Review', 'In Progress', False): 'ASSIGNED',
    ('Completed', 'In Progress', True): 'ASSIGNED',
    ('Deprecated', 'In Progress', False): 'ASSIGNED',

    # State: ASSIGNED
    ('In Review', 'Rework Needed', False): 'ASSIGNED',
    ('Completed', 'Rework Needed', True): 'ASSIGNED',
    ('Deprecated', 'Rework Needed', False): 'ASSIGNED',

    # State: FIXED (Verified)
    ('Not Started', 'Completed', True): 'VERIFIED',
    ('In Progress', 'Completed', True): 'VERIFIED',
    ('In Review', 'Completed', True): 'VERIFIED',
    ('Rework Needed', 'Completed', True): 'VERIFIED',
    ('Deprecated', 'Completed', True): 'VERIFIED',

    # State: ASSIGNED
    ('In Review', 'Not Started', False): 'ASSIGNED',
    ('Rework Needed', 'Not Started', False): 'ASSIGNED',
    ('Completed', 'Not Started', True): 'ASSIGNED',
    ('Deprecated', 'Not Started', False): 'ASSIGNED',

    # State: WON'T FIX (OBSOLETE)
    ('Not Started', 'Deprecated', False): 'OBSOLETE',
    ('In Progress', 'Deprecated', False): 'OBSOLETE',
    ('In Review', 'Deprecated', False): 'OBSOLETE',
    ('Rework Needed', 'Deprecated', False): 'OBSOLETE',
    ('Completed', 'Deprecated', True): 'OBSOLETE',
}


@signals.Restful.model_put_before_commit.connect_via(all_models.Assessment)
def handle_assessment_put_before_commit(sender, obj=None, src=None, **kwargs):
  """Handles assessment update event."""
  del sender  # Unused

  if not _is_issue_tracker_enabled(audit=obj.audit):
    # Skip updating issue and info if feature is disabled on Audit level.
    return

  issue_obj = all_models.IssuetrackerIssue.get_issue(
      _ASSESSMENT_MODEL_NAME, obj.id)

  initial_info = issue_obj.to_dict(
      include_issue=True,
      include_private=True) if issue_obj is not None else {}
  issue_tracker_info = dict(initial_info, **(src.get('issue_tracker') or {}))

  if issue_tracker_info.get('enabled'):

    issue_id = issue_tracker_info.get('issue_id')

    if not issue_id:
      # If assessment initially was created with disabled IssueTracker.
      _create_issuetracker_info(obj, issue_tracker_info)
      return

    _, issue_tracker_info['cc_list'] = _collect_issue_emails(obj)

  else:
    issue_tracker_info = {
        'enabled': False,
    }

  initial_assessment = kwargs.pop('initial_state', None)
  try:
    _update_issuetracker_issue(
        obj, issue_tracker_info, initial_assessment, initial_info, src)
  except integrations_errors.Error as error:
    logger.error(
        'Unable to update IssueTracker issue ID=%s '
        'while updating assessment ID=%d: %s', issue_id, obj.id, error)
    issue_tracker_info = {
        'enabled': False,
    }
    obj.add_warning('issue_tracker', 'Unable to update IssueTracker issue.')

  _update_issuetracker_info(obj, issue_tracker_info)


@signals.Restful.model_deleted.connect_via(all_models.Assessment)
def handle_assessment_deleted(sender, obj=None, service=None):
  """Handles assessment delete event."""
  del sender, service  # Unused

  issue_obj = all_models.IssuetrackerIssue.get_issue(
      _ASSESSMENT_MODEL_NAME, obj.id)

  if issue_obj:
    if (issue_obj.enabled and
            issue_obj.issue_id and
            _is_issue_tracker_enabled(audit=obj.audit)):
      issue_params = {
          'status': 'OBSOLETE',
          'comment': (
              'Assessment has been deleted. Changes to this GGRC '
              'Assessment will no longer be tracked within this bug.'
          ),
      }
      try:
        issues.Client().update_issue(issue_obj.issue_id, issue_params)
      except integrations_errors.Error as error:
        logger.error(
            'Unable to update IssueTracker issue ID=%s while '
            'deleting assessment ID=%d: %s',
            issue_obj.issue_id, obj.id, error)
    db.session.delete(issue_obj)


@signals.Restful.collection_posted.connect_via(all_models.AssessmentTemplate)
def handle_assessment_tmpl_post(sender, objects=None, sources=None):
  """Handles create event to AssessmentTemplate model."""
  del sender  # Unused

  db.session.flush()
  template_ids = {
      obj.id for obj in objects
  }

  if not template_ids:
    return

  # TODO(anushovan): use joined query to fetch audits or even
  #   issuetracker_issues with one query.
  audit_map = {
      r.destination_id: r.source_id
      for r in all_models.Relationship.query.filter(
          all_models.Relationship.source_type == 'Audit',
          all_models.Relationship.destination_type == 'AssessmentTemplate',
          all_models.Relationship.destination_id.in_(template_ids)).all()
  }

  if not audit_map:
    return

  audits = {
      a.id: a
      for a in all_models.Audit.query.filter(
          all_models.Audit.id.in_(audit_map.values())).all()
  }

  for obj, src in itertools.izip(objects, sources):
    audit_id = audit_map.get(obj.id)
    audit = audits.get(audit_id) if audit_id else None
    if not audit or not _is_issue_tracker_enabled(audit=audit):
      issue_tracker_info = {
          'enabled': False,
      }
    else:
      issue_tracker_info = src.get('issue_tracker')

    if not issue_tracker_info:
      continue
    all_models.IssuetrackerIssue.create_or_update_from_dict(
        _ASSESSMENT_TMPL_MODEL_NAME, obj.id, issue_tracker_info)


@signals.Restful.model_put.connect_via(all_models.AssessmentTemplate)
def handle_assessment_tmpl_put(sender, obj=None, src=None, service=None,
                               initial_state=None):
  """Handles update event to AssessmentTemplate model."""
  del sender, service, initial_state  # Unused

  audit = all_models.Audit.query.join(
      all_models.Relationship,
      all_models.Relationship.source_id == all_models.Audit.id,
  ).filter(
      all_models.Relationship.source_type == 'Audit',
      all_models.Relationship.destination_type == 'AssessmentTemplate',
      all_models.Relationship.destination_id == obj.id
  ).first()

  if not audit or not _is_issue_tracker_enabled(audit=audit):
    issue_tracker_info = {
        'enabled': False,
    }
  else:
    issue_tracker_info = src.get('issue_tracker')
  if issue_tracker_info:
    all_models.IssuetrackerIssue.create_or_update_from_dict(
        _ASSESSMENT_TMPL_MODEL_NAME, obj.id, issue_tracker_info)


@signals.Restful.model_deleted_after_commit.connect_via(
    all_models.AssessmentTemplate)
def handle_assessment_tmpl_deleted_after_commit(sender, obj=None,
                                                service=None, event=None):
  """Handles delete event to AssessmentTemplate model."""
  del sender, service, event  # Unused

  issue_obj = all_models.IssuetrackerIssue.get_issue(
      _ASSESSMENT_TMPL_MODEL_NAME, obj.id)
  if issue_obj:
    db.session.delete(issue_obj)


@signals.Restful.model_put_after_commit.connect_via(all_models.Audit)
def handle_audit_put_after_commit(sender, obj=None, **kwargs):
  """Handles updating issue tracker related info."""
  del sender  # Unused

  initial_state = kwargs.get('initial_state')
  if not initial_state:
    logger.debug(
        'Initial state of an Audit is not provided, '
        'skipping IssueTracker update.')
    return

  if (obj.archived == initial_state.archived or
          not obj.issue_tracker.get('enabled', False)):
    return

  start_update_issue_job(
      obj.id,
      _ARCHIVED_TMPL if obj.archived else _UNARCHIVED_TMPL)


def start_update_issue_job(audit_id, message):
  """Creates background job for handling IssueTracker issue update."""
  from ggrc import views
  views.start_update_audit_issues(audit_id, message)


def _load_snapshots(snapshot_ids):
  """Returns snapshots for given IDs."""
  return {
      s.id: s for s in all_models.Snapshot.query.options(
          orm.undefer_group('Snapshot_complete'),
          orm.Load(all_models.Snapshot).joinedload(
              'revision'
          ).undefer_group(
              'Revision_complete'
          )
      ).filter(
          all_models.Snapshot.id.in_(snapshot_ids)
      )
  }


def _load_templates(template_ids):
  """Returns assessment templates for given IDs."""
  return {
      t.id: t for t in all_models.AssessmentTemplate.query.options(
          orm.undefer_group('AssessmentTemplate_complete'),
      ).filter(
          all_models.AssessmentTemplate.id.in_(template_ids)
      )
  }


def _load_audits(audit_ids):
  """Returns audits for given IDs."""
  return {
      a.id: a for a in all_models.Audit.query.options(
          orm.undefer_group('Audit_complete'),
      ).filter(
          all_models.Audit.id.in_(audit_ids)
      )
  }


def _handle_assessment(assessment, src, snapshots, templates, audits):
  """Handles auto calculated properties for Assessment model."""
  snapshot_dict = src.get('object') or {}
  common.map_objects(assessment, snapshot_dict)
  common.map_objects(assessment, src.get('audit'))
  snapshot = snapshots.get(snapshot_dict.get('id'))

  if not src.get('_generated') and not snapshot:
    return

  template = templates.get(src.get('template', {}).get('id'))
  audit = audits[src['audit']['id']]
  relate_assignees(assessment, snapshot, template, audit)
  relate_ca(assessment, template)
  assessment.title = u'{} assessment for {}'.format(
      snapshot.revision.content['title'],
      audit.title,
  )

  if not template:
    # Assessment test plan should inherit test plan of snapshot
    assessment.test_plan = snapshot.revision.content.get("test_plan")
    return

  assessment.test_plan = template.procedure_description
  if template.test_plan_procedure:
    copy_snapshot_plan(assessment, snapshot)
  if template.template_object_type:
    assessment.assessment_type = template.template_object_type


def _handle_issue_tracker(assessment, src, templates, audits):
  """Handles issue tracker related data."""
  # Get issue tracker data from request.
  info = src.get('issue_tracker') or {}

  if not info:
    # Check assessment template for issue tracker data.
    template = templates.get(src.get('template', {}).get('id'))
    if template:
      info = template.issue_tracker

  if not info:
    # Check audit for issue tracker data.
    audit = audits.get(src.get('audit', {}).get('id'))
    if audit:
      info = audit.issue_tracker

  _create_issuetracker_info(assessment, info)


def _validate_issue_tracker_info(info):
  """Insures that component ID and hotlist ID are integers."""
  # TODO(anushovan): remove data type casting once integration service
  #   supports strings for following properties.
  component_id = info.get('component_id')
  if component_id:
    try:
      info['component_id'] = int(component_id)
    except (TypeError, ValueError):
      raise exceptions.ValidationError('Component ID must be a number.')

  hotlist_id = info.get('hotlist_id')
  if hotlist_id:
    try:
      info['hotlist_id'] = int(hotlist_id)
    except (TypeError, ValueError):
      raise exceptions.ValidationError('Hotlist ID must be a number.')


def init_hook():
  """Initializes hooks."""

  @signals.Restful.collection_posted.connect_via(all_models.Assessment)
  def handle_assessment_post(sender, objects=None, sources=None, service=None):
    """Applies custom attribute definitions and maps people roles.

    Applicable when generating Assessment with template.

    Args:
      sender: A class of Resource handling the POST request.
      objects: A list of model instances created from the POSTed JSON.
      sources: A list of original POSTed JSON dictionaries.
    """
    del sender, service  # Unused

    db.session.flush()
    audit_ids = set()
    template_ids = set()
    snapshot_ids = set()

    for src in sources:
      snapshot_ids.add(src.get('object', {}).get('id'))
      audit_ids.add(src.get('audit', {}).get('id'))
      template_ids.add(src.get('template', {}).get('id'))

    snapshot_cache = _load_snapshots(snapshot_ids)
    template_cache = _load_templates(template_ids)
    audit_cache = _load_audits(audit_ids)

    for assessment, src in itertools.izip(objects, sources):
      _handle_assessment(
          assessment, src, snapshot_cache, template_cache, audit_cache)
      _handle_issue_tracker(
          assessment, src, template_cache, audit_cache)

  @signals.Restful.model_put.connect_via(all_models.Assessment)
  def handle_assessment_put(sender, obj=None, src=None, service=None):
    """Handles assessment update event."""
    del sender, src, service  # Unused
    common.ensure_field_not_changed(obj, 'audit')


def _is_issue_tracker_enabled(audit=None):
  """Returns a boolean whether issue tracker integration feature is enabled.

  Args:
    audit: An optional instance of Audit model. If given function check if
        issue tracker integration is enabled for given audit as well.

  Returns:
    A boolean, True if feature is enabled or False otherwise.
  """
  if not _ISSUE_TRACKER_ENABLED:
    return False

  if audit is not None:
    audit_issue_tracker_info = audit.issue_tracker or {}

    if not bool(audit_issue_tracker_info.get('enabled')):
      return False

  return True


def _get_roles(assessment):
  """Returns emails associated with an assessment grouped by role.

  Args:
    assessment: An instance of Assessment model.

  Returns:
    A dict of {'role name': {set of emails}}.
  """
  all_roles = collections.defaultdict(set)

  ac_list = access_control.list.AccessControlList
  ac_role = access_control.role.AccessControlRole
  query = db.session.query(
      ac_list.person_id,
      ac_role.name,
      all_models.Person.email
  ).join(
      ac_role,
      ac_role.id == ac_list.ac_role_id
  ).join(
      all_models.Person,
      all_models.Person.id == ac_list.person_id
  ).filter(
      ac_list.object_type == _ASSESSMENT_MODEL_NAME,
      ac_list.object_id == assessment.id
  )
  for row in query.all():
    # row = (person_id, role_name, email)
    all_roles[row[1]].add(row[2])

  return all_roles


def _collect_issue_emails(assessment):
  """Returns emails related to given assessment.

  Args:
    assessment: An instance of Assessment model.

  Returns:
    A tuple of (assignee_email, [list of other email related to assessment])
  """
  assignee_email = None
  cc_list = set()

  all_roles = _get_roles(assessment)
  for role_name, emails in all_roles.iteritems():
    if role_name == 'Assignees':
      if emails:
        assignee_email = list(sorted(emails))[0]
        emails.remove(assignee_email)
    elif role_name == 'Verifiers':
      # skip verifiers from falling into CC list.
      continue

    cc_list.update(emails)

  return assignee_email, list(cc_list)


def _get_assessment_url(assessment):
  """Returns string URL for assessment view page."""
  return urlparse.urljoin(utils.get_url_root(), utils.view_url_for(assessment))


def _create_issuetracker_issue(assessment, issue_tracker_info):
  """Collects information and sends a request to create external issue."""
  _validate_issue_tracker_info(issue_tracker_info)
  reported_email = None
  reporter_id = get_current_user_id()
  if reporter_id:
    reporter = all_models.Person.query.filter(
        all_models.Person.id == reporter_id).first()
    if reporter is not None:
      reported_email = reporter.email

  comment = [
      'This bug was auto-generated to track a GGRC assessment '
      '(a.k.a PBC Item). Use the following link to find the '
      'assessment - %s.' % _get_assessment_url(assessment),
  ]
  test_plan = assessment.test_plan
  if test_plan:
    comment.extend([
        'Following is the assessment Requirements/Test Plan from GGRC:',
        html2text.HTML2Text().handle(test_plan).strip('\n'),
    ])

  hotlist_id = issue_tracker_info.get('hotlist_id')

  issue_params = {
      'component_id': issue_tracker_info['component_id'],
      'hotlist_ids': [hotlist_id] if hotlist_id else [],
      'title': issue_tracker_info['title'],
      'type': issue_tracker_info['issue_type'],
      'priority': issue_tracker_info['issue_priority'],
      'severity': issue_tracker_info['issue_severity'],
      'reporter': reported_email,
      'assignee': '',
      'verifier': '',
      'ccs': [],
      'comment': '\n'.join(comment),
  }

  assignee = issue_tracker_info.get('assignee')
  if assignee:
    issue_params['status'] = 'ASSIGNED'
    issue_params['assignee'] = assignee
    issue_params['verifier'] = assignee

  cc_list = issue_tracker_info.get('cc_list')
  if cc_list is not None:
    issue_params['ccs'] = cc_list

  res = issues.Client().create_issue(issue_params)
  return res['issueId']


def _create_issuetracker_info(assessment, issue_tracker_info):
  """Creates an entry for IssueTracker model."""
  if not issue_tracker_info.get('title'):
    issue_tracker_info['title'] = assessment.title

  if (issue_tracker_info.get('enabled') and
          _is_issue_tracker_enabled(audit=assessment.audit)):

    assignee_email, cc_list = _collect_issue_emails(assessment)
    if assignee_email is not None:
      issue_tracker_info['assignee'] = assignee_email
      issue_tracker_info['cc_list'] = cc_list

    try:
      issue_id = _create_issuetracker_issue(assessment, issue_tracker_info)
    except integrations_errors.Error as error:
      logger.error(
          'Unable to create IssueTracker issue '
          'while creating assessment ID=%d: %s', assessment.id, error)
      issue_tracker_info = {
          'enabled': False,
      }
      assessment.add_warning(
          'issue_tracker', 'Unable to create IssueTracker issue.')
    else:
      issue_tracker_info['issue_id'] = issue_id
      issue_tracker_info['issue_url'] = _ISSUE_URL_TMPL % issue_id
  else:
    issue_tracker_info = {
        'enabled': False,
    }

  all_models.IssuetrackerIssue.create_or_update_from_dict(
      _ASSESSMENT_MODEL_NAME, assessment.id, issue_tracker_info)


def _build_status_comment(assessment, initial_assessment):
  """Returns status message if status gets changed or None otherwise."""
  if initial_assessment.status == assessment.status:
    return None, None

  verifiers = _get_roles(assessment).get('Verifiers')
  status_text = assessment.status
  if verifiers:
    status = _VERIFIER_STATUSES.get(
        (initial_assessment.status, assessment.status, assessment.verified))
    # Corner case for custom status text.
    if assessment.verified and assessment.status == 'Completed':
      status_text = '%s and Verified' % status_text
  else:
    status = _NO_VERIFIER_STATUSES.get(
        (initial_assessment.status, assessment.status))

  if status:
    return status, _STATUS_CHANGE_COMMENT_TMPL % (
        status_text, _get_assessment_url(assessment))

  return None, None


def _handle_basic_props(issue_tracker_info, initial_info):
  """Handles updates to basic issue tracker properties."""
  issue_params = {}
  for name, api_name in _ISSUE_TRACKER_UPDATE_FIELDS:
    if name not in issue_tracker_info:
      continue
    value = issue_tracker_info[name]
    if value != initial_info.get(name):
      issue_params[api_name] = value
  return issue_params


def _fill_current_value(issue_params, assessment, initial_info):
  """Fills unchanged props with current values."""
  current_issue_params = {}
  for name, api_name in _ISSUE_TRACKER_UPDATE_FIELDS:
    current_issue_params[api_name] = initial_info.get(name)
  issue_params = dict(current_issue_params, **issue_params)

  if 'status' not in issue_params:
    # Resend status on any change.
    status_value = _STATUSES.get(assessment.status)
    if status_value:
      issue_params['status'] = status_value

  if 'hotlist_ids' not in issue_params:
    # Resend hotlists on any change.
    current_hotlist_id = initial_info.get('hotlist_id')
    issue_params['hotlist_ids'] = [current_hotlist_id] if (
        current_hotlist_id) else []

  if 'ccs' not in issue_params:
    current_cc_list = initial_info.get('cc_list')
    if current_cc_list:
      issue_params['ccs'] = current_cc_list

  return issue_params


def _build_cc_list(issue_tracker_info, initial_info):
  """Returns a list of email to update issue with."""
  cc_list = issue_tracker_info.get('cc_list')

  if cc_list is not None:
    current_cc_list = initial_info.get('cc_list')
    current_cc_list = set(current_cc_list) if (
        current_cc_list is not None) else set()
    updated_cc_list = set(cc_list)
    if updated_cc_list - current_cc_list:
      return list(updated_cc_list | current_cc_list)

  return None


def _update_issuetracker_issue(assessment, issue_tracker_info,
                               initial_assessment, initial_info, request):
  """Collects information and sends a request to update external issue."""

  comments = []

  # Handle switching of 'enabled' property.
  initially_enabled = initial_info.get('enabled', False)
  enabled = issue_tracker_info.get('enabled', False)
  if initially_enabled != enabled:
    # Add comment about toggling feature and process further.
    comments.append(_ENABLED_TMPL if enabled else _DISABLED_TMPL)
  elif not enabled:
    # If feature remains in the same status which is 'disabled'.
    return

  _validate_issue_tracker_info(issue_tracker_info)

  issue_params = _handle_basic_props(issue_tracker_info, initial_info)

  # Handle status update.
  status_value, status_comment = _build_status_comment(
      assessment, initial_assessment)
  if status_value:
    issue_params['status'] = status_value
    comments.append(status_comment)

  # Attach user comments if any.
  comment_text, comment_author = _get_added_comment_text(request)
  if comment_text is not None:
    comments.append(
        _COMMENT_TMPL % (
            comment_author, comment_text, _get_assessment_url(assessment)))

  if comments:
    issue_params['comment'] = '\n\n'.join(comments)

  # Handle hotlist ID update.
  hotlist_id = issue_tracker_info.get('hotlist_id')
  if hotlist_id is not None and hotlist_id != initial_info.get('hotlist_id'):
    issue_params['hotlist_ids'] = [hotlist_id] if hotlist_id else []

  # Handle cc_list update.
  cc_list = _build_cc_list(issue_tracker_info, initial_info)
  if cc_list is not None:
    issue_params['ccs'] = cc_list

  if issue_params:
    # Resend all properties upon any change.
    issue_params = _fill_current_value(issue_params, assessment, initial_info)
    issues.Client().update_issue(issue_tracker_info['issue_id'], issue_params)


def _update_issuetracker_info(assessment, issue_tracker_info):
  """Updates an entry for IssueTracker model."""
  if not _is_issue_tracker_enabled(audit=assessment.audit):
    issue_tracker_info['enabled'] = False

  all_models.IssuetrackerIssue.create_or_update_from_dict(
      _ASSESSMENT_MODEL_NAME, assessment.id, issue_tracker_info)


def _get_added_comment_text(src):
  """Returns comment text from given request."""
  comment_id = _get_added_comment_id(src)
  if comment_id is not None:
    comment_row = db.session.query(
        all_models.Comment.description,
        all_models.Person.email,
        all_models.Person.name
    ).outerjoin(
        all_models.Person,
        all_models.Person.id == all_models.Comment.modified_by_id,
    ).filter(
        all_models.Comment.id == comment_id
    ).first()
    if comment_row is not None:
      desc, creator_email, creator_name = comment_row
      if not creator_name:
        creator_name = creator_email
      return html2text.HTML2Text().handle(desc).strip('\n'), creator_name
  return None, None


def _get_added_comment_id(src):
  """Returns comment ID from given request."""
  if not src:
    return None

  actions = src.get('actions') or {}
  related = actions.get('add_related') or []

  if not related:
    return None

  related_obj = related[0]

  if related_obj.get('type') != 'Comment':
    return None

  return related_obj.get('id')


def generate_assignee_relations(assessment,
                                assignee_ids,
                                verifier_ids,
                                creator_ids):
  """Generates db relations to assessment for sent role ids.

    Args:
        assessment (model instance): Assessment model
        assignee_ids (list): list of person ids
        verifier_ids (list): list of person ids
        creator_ids (list): list of person ids
  """
  people = set(assignee_ids + verifier_ids + creator_ids)
  person_dict = {i.id: i for i in all_models.Person.query.filter(
      all_models.Person.id.in_(people)
  )}

  person_roles = []
  for person_id in people:
    person = person_dict.get(person_id)
    if person is None:
      continue
    if person_id in assignee_ids:
      person_roles.append((person, "Assignees"))
    if person_id in verifier_ids:
      person_roles.append((person, "Verifiers"))
    if person_id in creator_ids:
      person_roles.append((person, "Creators"))

  ac_roles = {
      acr_name: acr_id
      for acr_id, acr_name in access_control.role.get_custom_roles_for(
          assessment.type).iteritems()
  }
  db.session.add_all(
      all_models.AccessControlList(
          ac_role_id=ac_roles[role],
          person=person,
          object=assessment
      ) for person, role in person_roles
  )


def get_people_ids_based_on_role(assignee_role,
                                 default_role,
                                 template_settings,
                                 acl_dict):
  """Get people_ids base on role and template settings."""
  if assignee_role not in template_settings:
    return []
  template_role = template_settings[assignee_role]
  if isinstance(template_role, list):
    return template_role
  return acl_dict.get(template_role, acl_dict.get(default_role)) or []


def generate_role_object_dict(snapshot, audit):
  """Generate roles dict for sent snapshot and audit.

  returns dict of roles with key as role name and list of people ids as values.
  """

  acr_dict = access_control.role.get_custom_roles_for(snapshot.child_type)
  acl_dict = collections.defaultdict(list)
  # populated content should have access_control_list
  for acl in snapshot.revision.content["access_control_list"]:
    acl_dict[acr_dict[acl["ac_role_id"]]].append(acl["person_id"])
  # populate Access Control List by generated role from the related Audit
  acl_dict["Audit Lead"].append(audit.contact_id)
  acl_dict["Auditors"].extend([user_role.person_id
                               for user_role in audit.context.user_roles
                               if user_role.role.name == u"Auditor"])
  return acl_dict


def relate_assignees(assessment, snapshot, template, audit):
  """Generates assignee list and relates them to Assessment objects

    Args:
        assessment (model instance): Assessment model
        snapshot (model instance): Snapshot,
        template (model instance): AssessmentTemplate model nullable,
        audit (model instance): Audit
  """
  if template:
    template_settings = template.default_people
  else:
    template_settings = {"assignees": "Principal Assignees",
                         "verifiers": "Auditors"}
  acl_dict = generate_role_object_dict(snapshot, audit)
  assignee_ids = get_people_ids_based_on_role("assignees",
                                              "Audit Lead",  # default assignee
                                              template_settings,
                                              acl_dict)
  verifier_ids = get_people_ids_based_on_role("verifiers",
                                              "Auditors",  # default verifier
                                              template_settings,
                                              acl_dict)
  generate_assignee_relations(assessment,
                              assignee_ids,
                              verifier_ids,
                              [get_current_user_id()])


def relate_ca(assessment, template):
  """Generates custom attribute list and relates it to Assessment objects

    Args:
        assessment (model instance): Assessment model
        template: Assessment Temaplte instance (may be None)
  """
  if not template:
    return

  ca_definitions = all_models.CustomAttributeDefinition.query.options(
      orm.undefer_group('CustomAttributeDefinition_complete'),
  ).filter_by(
      definition_id=template.id,
      definition_type="assessment_template",
  ).order_by(
      all_models.CustomAttributeDefinition.id
  )
  for definition in ca_definitions:
    cad = all_models.CustomAttributeDefinition(
        title=definition.title,
        definition=assessment,
        attribute_type=definition.attribute_type,
        multi_choice_options=definition.multi_choice_options,
        multi_choice_mandatory=definition.multi_choice_mandatory,
        mandatory=definition.mandatory,
        helptext=definition.helptext,
        placeholder=definition.placeholder,
    )
    db.session.add(cad)


def copy_snapshot_plan(assessment, snapshot):
  """Copy test plan of Snapshot into Assessment"""
  if assessment.test_plan and snapshot.revision.content["test_plan"]:
    assessment.test_plan += "<br>"
    assessment.test_plan += snapshot.revision.content["test_plan"]
  elif snapshot.revision.content["test_plan"]:
    assessment.test_plan = snapshot.revision.content["test_plan"]
