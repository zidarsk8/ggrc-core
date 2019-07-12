# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
  Assessment generator hooks

  We are applying assessment template properties and make
  new relationships and custom attributes
"""

from datetime import datetime
import collections
import itertools
import logging

import flask

from ggrc import access_control
from ggrc import db
from ggrc import login
from ggrc import utils
from ggrc.access_control import list as ggrc_acl
from ggrc.access_control import people as ggrc_acp
from ggrc.login import get_current_user_id
from ggrc.models import all_models
from ggrc.models import cache as ggrc_cache
from ggrc.models import custom_attribute_definition as ggrc_cad
from ggrc.models.hooks import common
from ggrc.models.hooks.issue_tracker import assessment_integration
from ggrc.models.hooks.issue_tracker import integration_utils
from ggrc.models.exceptions import StatusValidationError
from ggrc.services import signals
from ggrc.utils import referenced_objects


logger = logging.getLogger(__name__)


def _validate_assessment_done_state(old_value, obj):
  """Checks if it's allowed to set done state from not done."""
  new_value = obj.status
  if old_value in obj.NOT_DONE_STATES and \
     new_value in obj.DONE_STATES:
    if hasattr(obj, "preconditions_failed") and obj.preconditions_failed:
      raise StatusValidationError("CA-introduced completion "
                                  "preconditions are not satisfied. "
                                  "Check preconditions_failed "
                                  "of items of self.custom_attribute_values")


def _handle_assessment(assessment, src):
  """Handles auto calculated properties for Assessment model."""
  snapshot_dict = src.get('object') or {}
  common.map_objects(assessment, snapshot_dict)
  common.map_objects(assessment, src.get('audit'))
  snapshot = referenced_objects.get("Snapshot", snapshot_dict.get('id'))

  template = referenced_objects.get(
      src.get('template', {}).get('type'),
      src.get('template', {}).get('id'),
  )

  if template is not None:
    _mark_cads_to_batch_insert(
        ca_definitions=template.custom_attribute_definitions,
        attributable=assessment,
    )

  if not src.get('_generated') and not snapshot:
    return

  audit = referenced_objects.get(
      src['audit']['type'],
      src['audit']['id'],
  )

  _relate_assignees(assessment, snapshot, template, audit)

  assessment.title = u'{} assessment for {}'.format(
      snapshot.revision.content['title'],
      audit.title,
  )

  if not template:
    # Assessment test plan should inherit test plan of snapshot
    assessment.test_plan = snapshot.revision.content.get("test_plan")
    return

  assessment.test_plan_procedure = template.test_plan_procedure
  assessment.test_plan = template.procedure_description
  if template.test_plan_procedure:
    copy_snapshot_plan(assessment, snapshot)
  if template.template_object_type:
    assessment.assessment_type = template.template_object_type


def init_hook():
  """Initializes hooks."""

  # pylint: disable=unused-variable
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

    for assessment, src in itertools.izip(objects, sources):
      _handle_assessment(assessment, src)

    _batch_insert_cads(attributables=objects)
    _batch_insert_acps(assessments=objects)

    # Flush roles objects for generated assessments.
    db.session.flush()

    tracker_handler = assessment_integration.AssessmentTrackerHandler()
    for assessment, src in itertools.izip(objects, sources):
      # Handling IssueTracker info here rather than in hooks/issue_tracker
      # would avoid querying same data (such as snapshots, audits and
      # templates) twice.
      integration_utils.update_issue_tracker_for_import(assessment)
      tracker_handler.handle_assessment_create(assessment, src)

  # pylint: disable=unused-variable
  @signals.Restful.model_put.connect_via(all_models.Assessment)
  def handle_assessment_put(sender, obj=None, src=None, service=None):
    """Handles assessment update event."""
    del sender, src, service  # Unused
    common.ensure_field_not_changed(obj, 'audit')

  @signals.Restful.model_put_before_commit.connect_via(all_models.Assessment)
  def handle_assessment_done_state(sender, **kwargs):
    """Checks if it's allowed to set done state from not done."""
    del sender  # Unused arg
    obj = kwargs['obj']
    initial_state = kwargs['initial_state']
    old_value = initial_state.status
    try:
      _validate_assessment_done_state(old_value, obj)
    except StatusValidationError as error:
      db.session.rollback()
      raise error


def _generate_assignee_relations(assessment,
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

  for person_id in people:
    person = person_dict.get(person_id)
    if person is None:
      continue
    if person.id in assignee_ids:
      _mark_acps_to_batch_insert(person, "Assignees", assessment)
    if person_id in verifier_ids:
      _mark_acps_to_batch_insert(person, "Verifiers", assessment)
    if person_id in creator_ids:
      _mark_acps_to_batch_insert(person, "Creators", assessment)


def get_people_ids_based_on_role(assignee_role,
                                 default_role,
                                 template_settings,
                                 acl_dict):
  """Get people_ids base on role and template settings."""
  if not template_settings.get(assignee_role):
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
  audit_acr = access_control.role.get_custom_roles_for("Audit")
  auditors_role = next(id_ for id_, val in audit_acr.iteritems()
                       if val == "Auditors")
  leads_role = next(id_ for id_, val in audit_acr.iteritems()
                    if val == "Audit Captains")

  acl_dict = collections.defaultdict(list)
  # populated content should have access_control_list
  for acl in snapshot.revision.content["access_control_list"]:
    acr = acr_dict.get(acl["ac_role_id"])
    if not acr:
      # This can happen when we try to create an assessment for a control that
      # had a custom attribute role removed. This can not cause a bug as we
      # only use the acl_list for getting new assessment assignees and those
      # can only be from non editable roles, meaning the roles that we actually
      # need can not be removed. Non essential roles that are removed might
      # should not affect this assessment generation.
      logger.info("Snapshot %d contains deleted role %d",
                  snapshot.id, acl["ac_role_id"])
      continue
    acl_dict[acr].append(acl["person_id"])

  # populate Access Control List by generated role from the related Audit
  acl_dict["Audit Lead"].extend([person.id
                                 for person, acl in audit.access_control_list
                                 if acl.ac_role_id == leads_role])
  auditors = [
      person.id for person, acl in audit.access_control_list
      if acl.ac_role_id == auditors_role
  ]
  acl_dict["Auditors"].extend(auditors or acl_dict["Audit Lead"])
  return acl_dict


def _relate_assignees(assessment, snapshot, template, audit):
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
  _generate_assignee_relations(assessment,
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
    return None

  created_cads = []
  for definition in template.custom_attribute_definitions:
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
    created_cads.append(cad)
  return created_cads


def _mark_cads_to_batch_insert(ca_definitions, attributable):
  """Mark custom attribute definitions for batch insert.

  Create stubs of `ca_defintions` with definition set to `attributable` and add
  them to `flask.g.cads_to_batch_insert` list. All CAD stubs presented in
  `flask.g.cads_to_batch_insert` will be inserted in custom attribute
  defintiions table upon `_batch_insert_cads` call.

  Args:
    ca_definitions (List[models.CustomAttributeDefinition]): List of CADs to
      be marked for batch insert.
    attributable (db.Model): Model instance for which CADs should be created.
  """

  def clone_cad_stub(cad_stub, target):
    """Create a copy of `cad_stub` CAD and assign it to `target`."""
    now = datetime.utcnow()
    current_user_id = login.get_current_user_id()

    clone_stub = dict(cad_stub)
    clone_stub["definition_type"] = target._inflector.table_singular
    clone_stub["definition_id"] = target.id
    clone_stub["created_at"] = now
    clone_stub["updated_at"] = now
    clone_stub["modified_by_id"] = current_user_id
    clone_stub["id"] = None

    return clone_stub

  if not hasattr(flask.g, "cads_to_batch_insert"):
    flask.g.cads_to_batch_insert = []

  for ca_definition in ca_definitions:
    stub = ca_definition.to_dict()
    new_ca_stub = clone_cad_stub(stub, attributable)
    flask.g.cads_to_batch_insert.append(new_ca_stub)


def _batch_insert_cads(attributables):
  """Insert custom attribute definitions marked for batch insert.

  Insert CADs stored in `flask.g.cads_to_batch_insert` in custom attribute
  definitions table. Attributables are passed here to obtain inserted CADs from
  DB so they could be placed in cache.

  Args:
    attributables (List[db.Model]): List of model instances for which CADs
      should be inserted.
  """
  cads_to_batch_insert = getattr(flask.g, "cads_to_batch_insert", [])
  if not cads_to_batch_insert:
    return
  with utils.benchmark("Insert CADs in batch"):
    flask.g.cads_to_batch_insert = []
    inserter = ggrc_cad.CustomAttributeDefinition.__table__.insert()
    db.session.execute(
        inserter.values([stub for stub in cads_to_batch_insert])
    )

    # Add inserted CADs into new objects collection of the cache, so that
    # they will be logged within event and appropriate revisions will be
    # created. At this point it is safe to query CADs by definition_type and
    # definition_id since this batch insert will be called only at assessment
    # creation time and there will be no other LCAs for it.
    new_cads_q = ggrc_cad.CustomAttributeDefinition.query.filter(
        ggrc_cad.CustomAttributeDefinition.definition_type == "assessment",
        ggrc_cad.CustomAttributeDefinition.definition_id.in_([
            attributable.id for attributable in attributables
        ])
    )

    _add_objects_to_cache(new_cads_q)


def _mark_acps_to_batch_insert(assignee, role_name, assessment):
  """Mark access control people for batch insert.

  Create stub of ACP with person set to `assignee` and access control role to
  ACL of `assessment` object with `role_name` role. Add created stub to
  `flask.g.acps_to_batch_insert` list. All ACP stubs presented in
  `flask.g.acps_to_batch_insert` will be inserted in access control people
  table upon `_batch_insert_acps` call.

  Args:
    assignee (models.Person): Person for new ACP.
    role_name (str): ACR role name.
    assessment (models.Assessment): Assessment where person should be added.
  """

  def add_person_to_acl(person, ac_list):
    """Add `person` person to `ac_list` ACL."""
    now = datetime.utcnow()
    current_user_id = login.get_current_user_id()
    return {
        "id": None,
        "person_id": person.id,
        "ac_list_id": ac_list.id,
        "created_at": now,
        "updated_at": now,
        "modified_by_id": current_user_id,
    }

  if not hasattr(flask.g, "acps_to_batch_insert"):
    flask.g.acps_to_batch_insert = []

  acl = assessment.get_acl_with_role_name(role_name)
  if not acl:
    return

  acp_stub = add_person_to_acl(assignee, acl)
  flask.g.acps_to_batch_insert.append(acp_stub)


def _batch_insert_acps(assessments):
  """Insert access control people marked for batch insert.

  Insert ACPs stored in `flask.g.acps_to_batch_insert` in access control people
  table. Assessments are passed here to obtain inserted ACPs from DB so they
  could be placed in cache.

  Args:
    assessments (List[models.Assessment]): List of model instances for which
      ACPs should be inserted.
  """
  acps_to_batch_insert = getattr(flask.g, "acps_to_batch_insert", [])
  if not acps_to_batch_insert:
    return
  with utils.benchmark("Insert ACPs in batch"):
    flask.g.acps_to_batch_insert = []
    inserter = ggrc_acp.AccessControlPerson.__table__.insert()
    db.session.execute(
        inserter.values([stub for stub in acps_to_batch_insert])
    )

    # Add inserted ACPs into new objects collection of the cache, so that
    # they will be logged within event and appropriate revisions will be
    # created. At this point it is safe to query ACPs by ac_list_id since
    # this batch insert will be called only at assessment creation time and
    # there will be no other ACPs for it.
    new_acls_q = db.session.query(
        ggrc_acl.AccessControlList.id,
    ).filter(
        ggrc_acl.AccessControlList.object_type == "Assessment",
        ggrc_acl.AccessControlList.object_id.in_([
            assessment.id for assessment in assessments
        ]),
    )
    new_acps_q = ggrc_acp.AccessControlPerson.query.filter(
        ggrc_acp.AccessControlPerson.ac_list_id.in_([
            new_acl.id for new_acl in new_acls_q
        ])
    )

    _add_objects_to_cache(new_acps_q)


def _add_objects_to_cache(objs_q):
  """Add objects from `objs_q` query to cache."""
  cache = ggrc_cache.Cache.get_cache(create=True)
  if cache:
    cache.new.update((obj, obj.log_json()) for obj in objs_q)


def copy_snapshot_plan(assessment, snapshot):
  """Copy test plan of Snapshot into Assessment"""
  snapshot_plan = snapshot.revision.content.get("test_plan", "")
  if assessment.test_plan and snapshot_plan:
    assessment.test_plan += "<br>"
    assessment.test_plan += snapshot_plan
  elif snapshot_plan:
    assessment.test_plan = snapshot_plan
