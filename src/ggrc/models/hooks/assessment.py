# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
  Assessment generator hooks

  We are applying assessment template properties and make
  new relationships and custom attributes
"""
import collections
import html2text
import itertools
import logging
import time
import urlparse

from sqlalchemy import orm

from google.appengine.api import urlfetch

from ggrc import db
from ggrc.access_control.role import get_custom_roles_for
from ggrc import access_control
from ggrc import utils
from ggrc.login import get_current_user_id
from ggrc.models import all_models
from ggrc.models.hooks import common
from ggrc.services import signals
from ggrc.access_control import role

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


_ISSUE_TRACKER_PARAMS = frozenset((
    'status',
    'title',
))

# mapping of model field name to API property name
_ISSUE_TRACKER_UPDATE_FIELDS = (
    ('title', 'title'),
    ('status', 'status'),
    ('issue_priority', 'priority'),
    ('issue_severity', 'severity'),
    ('component_id', 'component_id'),
    ('assignee', 'assignee'),
)

_ASSESSMENT_MODEL_NAME = 'Assessment'
_ASSESSMENT_TMPL_MODEL_NAME = 'AssessmentTemplate'

def init_hook():
  """Initializes hooks."""

  @signals.Restful.collection_posted.connect_via(all_models.Assessment)
  def handle_assessment_post(sender, objects=None, sources=None):
    """Applies custom attribute definitions and maps people roles.

    Applicable when generating Assessment with template.

    Args:
      sender: A class of Resource handling the POST request.
      objects: A list of model instances created from the POSTed JSON.
      sources: A list of original POSTed JSON dictionaries.
    """
    del sender  # Unused

    logger.info('---> handle_assessment_post: %s', sources)
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
      if template.test_plan_procedure:
        assessment.test_plan = snapshot.revision.content['test_plan']
      else:
        assessment.test_plan = template.procedure_description
      if template.template_object_type:
        assessment.assessment_type = template.template_object_type

    for assessment, src in itertools.izip(objects, sources):
      _create_issuetracker_info(assessment, src.get('issue_tracker'))

  @signals.Restful.model_put.connect_via(all_models.Assessment)
  def handle_assessment_put(sender, obj=None, src=None, service=None):
    # logger.info('------> handle_assessment_model_put: %s', (
    #     sender, obj, src, service))
    del sender, service  # Unused
    # logger.info(
    #     '---> [put] request status: %s, obj status: %s',
    #     src.get('status'), obj.status)
    common.ensure_field_not_changed(obj, 'audit')
    issue_tracker_info = src.get('issue_tracker')
    if issue_tracker_info:
      _update_issuetracker_info(obj, issue_tracker_info)

  @signals.Restful.model_put_after_commit.connect_via(all_models.Assessment)
  def handle_assessment_put_after_commit(
      sender, obj=None, src=None, service=None, event=None, initial_state=None):
    changed_attrs = set()
    if initial_state is not None:
      for k, v in initial_state._asdict().iteritems():
        if v != getattr(obj, k, None):
          changed_attrs.add(k)

    logger.info('------> handle_assessment_put_after_commit: %s', (
        sender, obj, src, service, event, initial_state))
    logger.info(
        '------> handle_assessment_put_after_commit CHANGED: %s', changed_attrs)

    # try:
    #   # form_data = urllib.urlencode(UrlPostHandler.form_fields)
    #   headers = {'Content-Type': 'application/json'}
    #   result = urlfetch.fetch(
    #       url='https://integration-dot-ggrc-test.googleplex.com/',
    #       # payload=form_data,
    #       method=urlfetch.GET,
    #       headers=headers)
    #   self.response.write(result.content)
    # except urlfetch.Error:
    #   logger.error('Caught exception fetching url')

    comment_id = _get_added_comment_id(src)
    props_to_update = changed_attrs & _ISSUE_TRACKER_PARAMS

    logger.info('------> comment_id: %s', comment_id)
    logger.info('------> props_to_update: %s', props_to_update)

    request_params = {}
    if comment_id is not None:
      comment_obj = all_models.Comment.query.filter(
          all_models.Comment.id == comment_id
      ).first()
      if comment_obj is not None:
        request_params['comment'] = html2text.HTML2Text().handle(
            comment_obj.description).strip('\n')

    logger.info('------> request_params: %s', request_params)

  @signals.Restful.model_deleted_after_commit.connect_via(all_models.Assessment)
  def handle_assessment_deleted_after_commit(
      sender, obj=None, service=None, event=None):
    del sender, service, event # Unused
    issue_obj = all_models.IssuetrackerIssue.get_issue(
        _ASSESSMENT_MODEL_NAME, obj.id)
    if issue_obj:
      db.session.delete(issue_obj)

  @signals.Restful.collection_posted.connect_via(all_models.Relationship)
  def handle_relation_post(sender, objects=None, sources=None):
    del sender, sources  # Unused
    logger.info('------> handle_relation_post')
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
      issue_obj = all_models.IssuetrackerIssue.get_issue(
          _ASSESSMENT_MODEL_NAME, assessment.id)
      if issue_obj is None or issue_obj.assignee is not None:
        continue

      assignee_email, cc_list = _collect_issue_emails(assessment)
      issue_tracker_info = issue_obj.to_dict(include_issue=True)
      issue_tracker_info['status'] = 'ASSIGNED'
      issue_tracker_info['assignee'] = assignee_email
      issue_tracker_info['cc_list'] = cc_list
      _update_issuetracker_info(assessment, issue_tracker_info)

  @signals.Restful.collection_posted.connect_via(all_models.AssessmentTemplate)
  def handle_assessment_tmpl_post(sender, objects=None, sources=None):
    del sender  # Unused
    for obj, src in itertools.izip(objects, sources):
      issue_tracker_info = src.get('issue_tracker')
      if not issue_tracker_info:
        continue
      all_models.IssuetrackerIssue.create_or_update_from_dict(
          _ASSESSMENT_TMPL_MODEL_NAME, obj.id, issue_tracker_info)

  @signals.Restful.model_put.connect_via(all_models.AssessmentTemplate)
  def handle_assessment_tmpl_put(sender, obj=None, src=None, service=None):
    del sender, service  # Unused
    issue_tracker_info = src.get('issue_tracker')
    if issue_tracker_info:
      all_models.IssuetrackerIssue.create_or_update_from_dict(
          _ASSESSMENT_TMPL_MODEL_NAME, obj.id, issue_tracker_info)

  @signals.Restful.model_deleted_after_commit.connect_via(
      all_models.AssessmentTemplate)
  def handle_assessment_tmpl_deleted_after_commit(
      sender, obj=None, service=None, event=None):
    del sender, service, event  # Unused
    issue_obj = all_models.IssuetrackerIssue.get_issue(
        _ASSESSMENT_TMPL_MODEL_NAME, obj.id)
    if issue_obj:
      db.session.delete(issue_obj)


def _collect_issue_emails(assessment):
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

  # select l.person_id, p.name, p.email, l.ac_role_id, r.name from access_control_list l join access_control_roles r on r.id=l.ac_role_id join people p on p.id=l.person_id where l.object_type='Assessment' and l.object_id=3;
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


def _create_issuetracker_issue(assessment, issue_tracker_info):
  reported_email = None
  reporter_id = get_current_user_id()
  if reporter_id:
    reporter = all_models.Person.query.filter(
        all_models.Person.id == reporter_id).first()
    if reporter is not None:
      reported_email = reporter.email

  hotlist_id = issue_tracker_info.get('hotlist_id')
  issue_params = {
      'component_id': issue_tracker_info['component_id'],
      'hotlist_ids': [hotlist_id] if hotlist_id else [],
      'title': issue_tracker_info['title'],
      'type': issue_tracker_info['issue_type'],
      'priority': issue_tracker_info['issue_priority'],
      'severity': issue_tracker_info['issue_severity'],
      'reporter': reported_email,
      'assignee': None,
      'verifier': None,
      'ccs': [],
      'comment': (
          'This bug was auto-generated to track a GGRC assessment '
          '(a.k.a PBC Item). Use the following link to find the '
          'assessment - %s.\n'
          'Following is the assessment Requirements/Test Plan from GGRC:\n'
          '[Test Plan text]'
      ) % (urlparse.urljoin(
          utils.get_url_root(), utils.view_url_for(assessment))),
  }

  # TODO(anushovan): create issue here.
  logger.info('------> CREATE ISSUE: %s', issue_params)
  return int(time.time())


def _create_issuetracker_info(assessment, issue_tracker_info):
  if not issue_tracker_info:
    # return
    # TODO(anushovan): remove this when development is done
    issue_tracker_info = {
        "enabled": True,
        "component_id": "64445",
        "hotlist_id": None,
        "issue_type": "PROCESS",
        "issue_priority": "P2",
        "issue_severity": "S2",
        # "issue_id": "1508276850",
        # "issue_url": "http://issuetracker.me/b/1508276850",
    }

  if not issue_tracker_info.get('title'):
    issue_tracker_info['title'] = assessment.title

  if issue_tracker_info.get('enabled'):
    issue_id = _create_issuetracker_issue(assessment, issue_tracker_info)
    issue_tracker_info['issue_id'] = issue_id
    issue_tracker_info['issue_url'] = 'http://issuetracker.me/b/%s' % issue_id

  all_models.IssuetrackerIssue.create_or_update_from_dict(
      _ASSESSMENT_MODEL_NAME, assessment.id, issue_tracker_info)


def _update_issuetracker_issue(assessment, issue_tracker_info):
  issue_params = {}
  current_info = assessment.issue_tracker

  for name, api_name in _ISSUE_TRACKER_UPDATE_FIELDS:
    value = issue_tracker_info.get(name)
    if value != current_info.get(name):
      issue_params[api_name] = value

  comment = issue_tracker_info.get('comment')
  if comment:
    issue_params['comment'] = comment

  hotlist_id = issue_tracker_info.get('hotlist_id')
  if hotlist_id != current_info.get('hotlist_id'):
    issue_params['hotlist_ids'] = [hotlist_id] if hotlist_id else []

  cc_list = issue_tracker_info.get('cc_list')
  if cc_list is not None:
    issue_params['ccs'] = cc_list

  if issue_params:
    # TODO(anushovan): update issue here.
    logger.info('------> UPDATE ISSUE: %s', issue_params)


def _update_issuetracker_info(assessment, issue_tracker_info):
  if issue_tracker_info.get('enabled') and issue_tracker_info.get('issue_id'):
    _update_issuetracker_issue(assessment, issue_tracker_info)

  all_models.IssuetrackerIssue.create_or_update_from_dict(
      _ASSESSMENT_MODEL_NAME, assessment.id, issue_tracker_info)


def _get_added_comment_id(src):
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
