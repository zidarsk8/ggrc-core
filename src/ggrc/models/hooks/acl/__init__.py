# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Entry point for all acl handlers.

This package should have the single hook that should handle all acl propagation
and deletion.
"""

import flask
import sqlalchemy as sa
from sqlalchemy.orm.session import Session

from ggrc.models import all_models
from ggrc.models.hooks.acl import propagation
from ggrc_workflows.models.hooks import workflow


def _add_or_update(name, value):
  """Add or update flask.g attribute."""
  if hasattr(flask.g, name):
    getattr(flask.g, name).update(value)
  else:
    setattr(flask.g, name, value)


def add_relationships(relationship_ids):
  """Add extra relationships to propagation queue.

  This function is needed to allow propagation of manually created
  relationships from raw SQL statements. The most common examples for this are
  snapshot relationships and automappings.

  Args:
    relationship_ids: set of ids that might have to propagate permissions.
  """
  _add_or_update("new_acl_ids", set())
  _add_or_update("new_relationship_ids", relationship_ids)
  _add_or_update("deleted_objects", set())


def _get_propagation_entries(session):
  acl_ids = set()
  relationship_ids = set()
  for obj in session.new:
    if isinstance(obj, all_models.AccessControlList):
      acl_ids.add(obj.id)
    if isinstance(obj, all_models.Relationship):
      relationship_ids.add(obj.id)

  deleted = {(obj.type, obj.id) for obj in session.deleted}

  return acl_ids, relationship_ids, deleted


def after_flush(session, _):
  """Handle all ACL hooks after after flush."""
  if not flask.has_app_context():
    return

  acl_ids, relationship_ids, deleted = _get_propagation_entries(session)

  _add_or_update("new_acl_ids", acl_ids)
  _add_or_update("new_relationship_ids", relationship_ids)
  _add_or_update("deleted_objects", deleted)

  # Legacy propagation for workflows that will have to be refactored to use
  # relationships and the code above
  _add_or_update("new_wf_acls", workflow.get_new_wf_acls(session))
  _add_or_update(
      "deleted_wf_objects",
      workflow.get_deleted_wf_objects(session)
  )


def after_commit():
  propagation.propagate()
  workflow.handle_acl_changes()


def init_hook():
  """Initialize Relationship-related hooks."""
  sa.event.listen(Session, "after_flush", after_flush)
