# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""All hooks required by audit roles business cases"""

import flask
import sqlalchemy as sa
from sqlalchemy.orm.session import Session

from ggrc import db
from ggrc.models import all_models


def _get_captain_and_auditor_roles():
  """Cache captain and auditor roles"""
  if getattr(flask.g, "acl_captain_editor_cache", None) is not None:
    return flask.g.acl_captain_editor_cache
  program_editor = db.session.query(all_models.Role).filter(
      all_models.Role.name == "ProgramEditor").first()
  audit_captain = db.session.query(all_models.AccessControlRole).filter(
      all_models.AccessControlRole.name == "Audit Captains").first()
  flask.g.acl_captain_editor_cache = (program_editor, audit_captain)
  return (program_editor, audit_captain)


def handle_acl_creation(session, _):
  """Handle legacy audit captain -> program editor role propagation"""
  for obj in session.new:
    if not isinstance(obj, all_models.AccessControlList):
      continue
    program_editor, audit_captain = _get_captain_and_auditor_roles()
    if obj.ac_role_id != audit_captain.id:
      continue
    audit = obj.object
    program = audit.program
    if not any(ur for ur in program.context.user_roles
               if ur.person_id == obj.person_id):
      db.session.add(
          all_models.UserRole(
              role=program_editor,
              context=program.context,
              person_id=obj.person_id
          )
      )


def init_hook():
  """Initialize AccessControlList-related hooks."""
  sa.event.listen(Session, "after_flush", handle_acl_creation)
