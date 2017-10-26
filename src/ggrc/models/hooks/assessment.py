# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
  Assessment generator hooks

  We are applying assessment template properties and make
  new relationships and custom attributes
"""
import collections
import copy
import html2text
import itertools
import json
import logging
import time
import urlparse

from sqlalchemy import orm
from werkzeug import exceptions

from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors

from ggrc import db
from ggrc.access_control.role import get_custom_roles_for
from ggrc import access_control
from ggrc import settings
from ggrc import utils
from ggrc.login import get_current_user_id
from ggrc.models import all_models
from ggrc.models.hooks import common
from ggrc.services import signals
from ggrc.access_control import role

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


_DEFAULT_HEADERS = {}
if settings.URLFETCH_SERVICE_ID:
  _DEFAULT_HEADERS['X-URLFetch-Service-Id'] = settings.URLFETCH_SERVICE_ID

_ENDPOINT = settings.INTEGRATION_SERVICE_URL
_ISSUE_URL_TMPL = settings.ISSUE_TRACKER_BUG_URL_TMPL or 'http://issue/%s'

# mapping of model field name to API property name
_ISSUE_TRACKER_UPDATE_FIELDS = (
    ('title', 'title'),
    ('issue_priority', 'priority'),
    ('issue_severity', 'severity'),
    ('component_id', 'component_id'),

    # just to track assessment's assignment at first time, tracking further
    # updates is not required.
    ('assignee', 'assignee'),
)

_ASSESSMENT_MODEL_NAME = 'Assessment'
_ASSESSMENT_TMPL_MODEL_NAME = 'AssessmentTemplate'

_STATUS_CHANGE_COMMENT_TMPL = (
    'The status of this bug was automatically synced to reflect '
    'current GGRC assessment status. Current status of related GGRC '
    'Assessment is %s. Use the following to link to and get '
    'information from the GGRC Assessment on why the status may have changed. '
    'Link - %s'
)

_NO_VERIFIER_STATUSES = {
    # (from_status, to_status): 'issue_tracker_status'
    ('Not Started', 'In Progress'): 'ACCEPTED',
    ('In Progress', 'Completed'): 'VERIFIED',
    ('Completed', 'In Progress'): 'ACCEPTED',
}

_VERIFIER_STATUSES = {
    # (from_status, to_status, verified): 'issue_tracker_status'
    ('Not Started', 'In Progress', False): 'ACCEPTED',
    ('In Progress', 'In Review', False): 'FIXED',
    ('In Review', 'In Progress', False): 'ACCEPTED',

    # 'Completed' here means Completed and Verified.
    ('In Review', 'Completed', True): 'VERIFIED',
    ('Completed', 'In Review', True): 'FIXED',
    ('Completed', 'In Progress', True): 'ACCEPTED',
}


class Error(Exception):
  """Module level error."""


class HttpError(Error):
  """Base HTTP error."""

  def __init__(self, data, status=500):
    """Instantiates error with give parameters.

    Args:
      data: A string or object describing an error.
      status: An integer representing HTTP status.
    """
    super(HttpError, self).__init__('HTTP Error %s' % status)
    self.data = data
    self.status = status


class BadResponseError(Error):
  """Wrong formatted response error."""


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
    audit_ids = []
    template_ids = []
    snapshot_ids = []

    for src in sources:
      snapshot_ids.append(src.get('object', {}).get('id'))
      audit_ids.append(src.get('audit', {}).get('id'))
      template_ids.append(src.get('template', {}).get('id'))

    snapshot_cache = {
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
    template_cache = {
        t.id: t for t in all_models.AssessmentTemplate.query.options(
            orm.undefer_group('AssessmentTemplate_complete'),
        ).filter(
            all_models.AssessmentTemplate.id.in_(template_ids)
        )
    }
    audit_cache = {
        a.id: a for a in all_models.Audit.query.options(
            orm.undefer_group('Audit_complete'),
        ).filter(
            all_models.Audit.id.in_(audit_ids)
        )
    }

    issue_tracker_templates = {}
    for assessment, src in itertools.izip(objects, sources):
      snapshot_dict = src.get('object') or {}
      common.map_objects(assessment, snapshot_dict)
      common.map_objects(assessment, src.get('audit'))
      snapshot = snapshot_cache.get(snapshot_dict.get('id'))
      if not src.get('_generated') and not snapshot:
        continue
      template = template_cache.get(src.get('template', {}).get('id'))
      audit = audit_cache[src['audit']['id']]
      relate_assignees(assessment, snapshot, template, audit)
      relate_ca(assessment, template)
      assessment.title = u'{} assessment for {}'.format(
          snapshot.revision.content['title'],
          audit.title,
      )
      if not template:
        continue
      issue_tracker_templates[assessment.id] = template.issue_tracker
      if template.test_plan_procedure:
        assessment.test_plan = snapshot.revision.content['test_plan']
      else:
        assessment.test_plan = template.procedure_description
      if template.template_object_type:
        assessment.assessment_type = template.template_object_type

    for assessment, src in itertools.izip(objects, sources):
      info = src.get('issue_tracker') or issue_tracker_templates.get(
          assessment.id)
      _create_issuetracker_info(assessment, info)

  @signals.Restful.model_put.connect_via(all_models.Assessment)
  def handle_assessment_put(
      sender, obj=None, src=None, service=None, initial_state=None):
    """Handles assessment update event."""
    del sender, service  # Unused

    common.ensure_field_not_changed(obj, 'audit')

    issue_tracker_info = src.get('issue_tracker')
    if issue_tracker_info:
      # Preserve initial state of issue tracker info.
      src['__stash']['issue_tracker'] = copy.deepcopy(obj.issue_tracker)
      _update_issuetracker_info(obj, issue_tracker_info)

  @signals.Restful.model_put_after_commit.connect_via(all_models.Assessment)
  def handle_assessment_put_after_commit(
      sender, obj=None, src=None, service=None, event=None, initial_state=None):
    """Handles assessment post update event."""
    del sender, service, event  # Unused

    issue_tracker_info = obj.issue_tracker
    if issue_tracker_info.get('enabled') and issue_tracker_info.get('issue_id'):
      try:
        _update_issuetracker_issue(obj, issue_tracker_info, initial_state, src)
      except (HttpError, BadResponseError) as e:
        logger.error('Unable update Issue Tracker issue: %s', e)
        # Dirty hack to rollback change to issuetracker_issues model.
        # Reverted info doesn't get sent to frontend so page refresh is required
        # but the hack at least allows to keep data in sync.
        initial_issue_tracker_info = src['__stash'].get('issue_tracker')
        if initial_issue_tracker_info:
          _update_issuetracker_info(obj, initial_issue_tracker_info)

  @signals.Restful.model_deleted.connect_via(all_models.Assessment)
  def handle_assessment_deleted(sender, obj=None, service=None):
    """Handles assessment delete event."""
    del sender, service  # Unused

    issue_obj = all_models.IssuetrackerIssue.get_issue(
        _ASSESSMENT_MODEL_NAME, obj.id)

    if issue_obj:
      if issue_obj.enabled and issue_obj.issue_id:
        issue_params = {
            'status': 'OBSOLETE',
            'comment': (
                'Assessment has been deleted. Changes to this GGRC '
                'Assessment will no longer be tracked within this bug.'
            ),
        }
        try:
          _send_request(
              '/api/issues/%s' % issue_obj.issue_id,
              method=urlfetch.PUT, payload=issue_params)
        except (HttpError, BadResponseError) as e:
          logger.error('Unable to update Issue tracker: %s', e)
          raise exceptions.InternalServerError(
              'Unable update Issue Tracker issue.')
      db.session.delete(issue_obj)

  @signals.Restful.collection_posted.connect_via(all_models.Relationship)
  def handle_relation_post(sender, objects=None, sources=None, service=None):
    """Handles create event to Relationships model."""
    del sender, sources, service  # Unused

    if not _is_issue_tracker_enabled():
      return

    assessment_ids = [
        obj.destination_id
        for obj in objects
        if obj.destination_type == _ASSESSMENT_MODEL_NAME
    ]
    if not assessment_ids:
      return

    db.session.flush()

    for assessment in all_models.Assessment.query.filter(
        all_models.Assessment.id.in_(assessment_ids)).all():
      if not _is_issue_tracker_enabled(audit=assessment.audit):
        continue
      issue_obj = all_models.IssuetrackerIssue.get_issue(
          _ASSESSMENT_MODEL_NAME, assessment.id)
      if (issue_obj is None or
          not issue_obj.enabled or
          issue_obj.assignee is not None):
        continue

      assignee_email, cc_list = _collect_issue_emails(assessment)
      issue_tracker_info = issue_obj.to_dict(include_issue=True)
      issue_tracker_info['status'] = 'ASSIGNED'
      issue_tracker_info['assignee'] = assignee_email
      issue_tracker_info['cc_list'] = cc_list
      issue_id = issue_tracker_info.get('issue_id')
      if issue_id:
        issue_params = {
            'status': 'ASSIGNED',
            'assignee': assignee_email,
            'verifier': assignee_email,
            'ccs': cc_list,
        }
        try:
          _send_request(
              '/api/issues/%s' % issue_id,
              method=urlfetch.PUT, payload=issue_params)
        except (HttpError, BadResponseError) as e:
          logger.error('Unable to update Issue tracker: %s', e)
          raise exceptions.InternalServerError(
              'Unable update Issue Tracker issue.')

      _update_issuetracker_info(assessment, issue_tracker_info)

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
      if (not audit_id or audit_id not in audits or
          not _is_issue_tracker_enabled(audit=audits[audit_id])):
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
  def handle_assessment_tmpl_put(
      sender, obj=None, src=None, service=None, initial_state=None):
    """Handles update event to AssessmentTemplate model."""
    del sender, service  # Unused

    if not _is_issue_tracker_enabled(audit=obj.audit):
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
  def handle_assessment_tmpl_deleted_after_commit(
      sender, obj=None, service=None, event=None):
    """Handles delete event to AssessmentTemplate model."""
    del sender, service, event  # Unused

    issue_obj = all_models.IssuetrackerIssue.get_issue(
        _ASSESSMENT_TMPL_MODEL_NAME, obj.id)
    if issue_obj:
      db.session.delete(issue_obj)


def _is_issue_tracker_enabled(audit=None):
  """Returns a boolean whether issue tracker integration feature is enabled.

  Args:
    audit: An optional instance of Audit model. If given function check if
        issue tracker integration is enabled for given audit as well.

  Returns:
    A boolean, True if feature is enabled or False otherwise.
  """
  if not bool(_ENDPOINT):
    return False

  if audit is not None:
    audit_issue_tracker_info = audit.issue_tracker or {}

    if not bool(audit_issue_tracker_info.get('enabled')):
      return False

  return True


def _collect_issue_emails(assessment):
  """Returns email related to given assessment.

  Args:
    assessment: An instance of Assessment model.

  Returns:
    A tuple of (assignee_email, [list of other email related to assessment])
  """
  assignee_email = None
  cc_list = set()

  assignees = assessment.assessors
  if assignees:
    for i, person in enumerate(sorted(assignees, key=lambda o: o.name)):
      if i == 0:
        assignee_email = person.email
        continue
      email = person.email
      if email and email != assignee_email:
        cc_list.add(email)

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
  for r in query.all():
    email = r[2]
    if email != assignee_email:
      cc_list.add(email)
  roles_dict = role.get_custom_roles_for(_ASSESSMENT_MODEL_NAME)

  return assignee_email, list(cc_list)


# TODO(anushovan): migrate to Client object once
#   https://github.com/google/ggrc-core/pull/6584 is submitted.
def _send_http_request(url, method=urlfetch.GET, payload=None, headers=None):
  """Sends HTTP request with given parameters."""
  if _DEFAULT_HEADERS:
    headers.update(_DEFAULT_HEADERS)

  url = urlparse.urljoin(_ENDPOINT, url)

  try:
    response = urlfetch.fetch(
        url,
        method=method,
        payload=payload,
        headers=headers,
        follow_redirects=False,
        deadline=30,
    )
    if response.status_code != 200:
      logger.error(
          'Unable to perform request to %s: %s %s',
          url, response.status_code, response.content)
      raise HttpError(response.content, status=response.status_code)
    return response.content
  except urlfetch_errors.Error as e:
    logger.error('Unable to perform urlfetch request: %s', e)
    raise HttpError('Unable to perform a request')


# TODO(anushovan): migrate to Client object once
#   https://github.com/google/ggrc-core/pull/6584 is submitted.
def _send_request(url, method=urlfetch.GET, payload=None, headers=None):
  """Prepares and sends request."""
  headers = headers or {}
  headers['Content-Type'] = 'application/json'

  if payload is not None:
    payload = json.dumps(payload)

  data = _send_http_request(
      url, method=method, payload=payload, headers=headers)

  try:
    return json.loads(data)
  except (TypeError, ValueError) as e:
    logger.error('Unable to parse JSON from response: %s', e)
    raise BadResponseError('Unable to parse JSON from response.')


def _get_assessment_url(assessment):
  """Returns string URL for assessment view page."""
  return urlparse.urljoin(utils.get_url_root(), utils.view_url_for(assessment))


def _create_issuetracker_issue(assessment, issue_tracker_info):
  """Collects information and sends a request to create external issue."""
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

  component_id = issue_tracker_info['component_id']
  hotlist_id = issue_tracker_info.get('hotlist_id')

  # TODO(anushovan): remove data type casting once integration service
  #   supports strings for following properties.
  try:
    component_id = int(component_id)
  except (TypeError, ValueError):
    raise exceptions.BadRequest('Component ID must be a number.')

  try:
    hotlist_id = [int(hotlist_id)] if hotlist_id else []
  except (TypeError, ValueError):
    raise exceptions.BadRequest('Hotlist ID must be a number.')

  issue_params = {
      'component_id': component_id,
      'hotlist_ids': hotlist_id,
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

  # TODO(anushovan): analyze error and fail back to
  #   settings.ISSUE_TRACKER_DEFAULT_COMPONENT_ID or/and
  #   settings.ISSUE_TRACKER_DEFAULT_HOTLIST_ID in case of access issue.
  res = _send_request(
      '/api/issues', method=urlfetch.POST, payload=issue_params)
  return res['issueId']


def _create_issuetracker_info(assessment, issue_tracker_info):
  """Creates an entry for IssueTracker model."""
  if not issue_tracker_info.get('title'):
    issue_tracker_info['title'] = assessment.title

  if (issue_tracker_info.get('enabled') and
      _is_issue_tracker_enabled(audit=assessment.audit)):

    try:
      issue_id = _create_issuetracker_issue(assessment, issue_tracker_info)
    except (HttpError, BadResponseError) as e:
      logger.error('Unable create Issue Tracker issue: %s', e)
      raise exceptions.InternalServerError('Unable create Issue Tracker issue.')

    issue_tracker_info['issue_id'] = issue_id
    issue_tracker_info['issue_url'] = _ISSUE_URL_TMPL % issue_id
  else:
    issue_tracker_info = {
        'enabled': False,
    }

  all_models.IssuetrackerIssue.create_or_update_from_dict(
      _ASSESSMENT_MODEL_NAME, assessment.id, issue_tracker_info)


def _update_issuetracker_issue(
    assessment, issue_tracker_info, initial_assessment, request):
  """Collects information and sends a request to update external issue."""
  issue_params = {}
  # Handle updates to basic issue tracker properties.
  initial_info = request['__stash'].get('issue_tracker') or {}
  for name, api_name in _ISSUE_TRACKER_UPDATE_FIELDS:
    value = issue_tracker_info.get(name)
    if value != initial_info.get(name):
      issue_params[api_name] = value

  comments = []
  # Handle status update.
  if initial_assessment.status != assessment.status:
    verifiers = assessment.verifiers
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
      issue_params['status'] = status
      comments.append(_STATUS_CHANGE_COMMENT_TMPL % (
          status_text, _get_assessment_url(assessment)))
    else:
      # Default comment to track status update in issue tracker.
      comments.append(
          'Assessment status has been updated: %s -> %s' % (
              initial_assessment.status, status_text))

  # Attach user comments if any.
  comment_text = _get_added_comment_text(request)
  if comment_text is not None:
    comments.append(html2text.HTML2Text().handle(
        comment_obj.description).strip('\n'))

  if comments:
    issue_params['comment'] = '\n\n'.join(comments)

  # Handle hotlist ID update.
  hotlist_id = issue_tracker_info.get('hotlist_id')
  if hotlist_id != initial_info.get('hotlist_id'):
    issue_params['hotlist_ids'] = [hotlist_id] if hotlist_id else []

  # Handle cc_list ID update.
  cc_list = issue_tracker_info.get('cc_list')
  if cc_list is not None:
    issue_params['ccs'] = cc_list

  if issue_params:
    _send_request(
        '/api/issues/%s' % issue_tracker_info['issue_id'],
        method=urlfetch.PUT, payload=issue_params)


def _update_issuetracker_info(assessment, issue_tracker_info):
  """Updates an entry for IssueTracker model."""
  if not (bool(issue_tracker_info.get('enabled')) and
          _is_issue_tracker_enabled(audit=assessment.audit)):
    issue_tracker_info = {
        'enabled': False,
    }

  all_models.IssuetrackerIssue.create_or_update_from_dict(
      _ASSESSMENT_MODEL_NAME, assessment.id, issue_tracker_info)


def _get_added_comment_text(src):
  """Returns comment text from given request."""
  comment_id = _get_added_comment_id(src)
  if comment_id is not None:
    comment_obj = all_models.Comment.query.filter(
        all_models.Comment.id == comment_id).first()
    if comment_obj is not None:
      return html2text.HTML2Text().handle(comment_obj.description).strip('\n')
  return None


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
      for acr_id, acr_name in get_custom_roles_for(assessment.type).items()
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

  acr_dict = role.get_custom_roles_for(snapshot.child_type)
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
