# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Entry point for all acl handlers.

This package should have the single hook that should handle all acl propagation
and deletion.
"""

import flask
import sqlalchemy as sa
from sqlalchemy.orm.session import Session

from ggrc.models.hooks.acl import audit_roles
from ggrc.models.hooks.acl import program_roles
from ggrc.models.hooks.acl import relationship_deletion
from ggrc.models.hooks import access_control_list
from ggrc.models.hooks import relationship

from ggrc.models import all_models
from ggrc.models.hooks.acl import propagation
from ggrc_workflows.models.hooks import workflow


def _get_propagation_entries(session):
  acl_ids = set()
  relationship_ids = set()
  for obj in session.new:
    if isinstance(obj, all_models.AccessControlList):
      acl_ids.add(obj.id)
    if isinstance(obj, all_models.Relationship):
      relationship_ids.add(obj.id)

  return acl_ids, relationship_ids


def after_flush(session, _):
  """Handle all ACL hooks after after flush."""
  if not flask.has_app_context():
    return

  acl_ids, relationship_ids = _get_propagation_entries(session)

  if hasattr(flask.g, "new_acl_ids"):
    flask.g.new_acl_ids.update(acl_ids)
  else:
    flask.g.new_acl_ids = acl_ids

  if hasattr(flask.g, "new_relationship_ids"):
    flask.g.new_relationship_ids.update(relationship_ids)
  else:
    flask.g.new_relationship_ids = relationship_ids

  relationship.handle_relationship_creation(session)
  access_control_list.handle_acl_creation(session)
  program_role_handler = program_roles.ProgramRolesHandler()
  program_role_handler.after_flush(session)
  audit_role_handler = audit_roles.AuditRolesHandler()
  audit_role_handler.after_flush(session)
  relationship_deletion.after_flush(session)

  # Legacy propagation for workflows that will have to be refactored to use
  # relationships and the code above

  if hasattr(flask.g, "new_wf_acls"):
    flask.g.new_wf_acls.update(workflow.get_new_wf_acls(session))
  else:
    flask.g.new_wf_acls = workflow.get_new_wf_acls(session)

  if hasattr(flask.g, "deleted_wf_objects"):
    flask.g.deleted_wf_objects.update(workflow.get_deleted_wf_objects(session))
  else:
    flask.g.deleted_wf_objects = workflow.get_deleted_wf_objects(session)


def after_commit():
  propagation.propagate()
  workflow.handle_acl_changes()


def init_hook():
  """Initialize Relationship-related hooks."""
  sa.event.listen(Session, "after_flush", after_flush)
