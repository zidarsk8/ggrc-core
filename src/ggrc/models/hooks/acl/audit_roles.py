# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""All hooks required by audit roles business cases"""


from collections import defaultdict

import flask
import sqlalchemy as sa

from sqlalchemy.orm import load_only
from sqlalchemy.orm.session import Session

from ggrc import db
from ggrc.models import all_models
from ggrc.models.relationship import Stub, RelationshipsCache
from ggrc.models.hooks.relationship import related


def _get_cache(expr, name):
  """Simple cache function"""
  cached = getattr(flask.g, name, None)
  if cached is not None:
    return cached
  val = expr()
  setattr(flask.g, name, val)
  return val


def _get_program_editor_role():
  """Cache captain and auditor roles"""
  return _get_cache(lambda: db.session.query(all_models.Role).options(
      load_only("id")).filter(
      all_models.Role.name == "ProgramEditor").first().id,
      "acl_program_editor")


def _get_acl_audit_roles():
  """Cache captain and auditor roles"""
  return _get_cache(lambda: {
      role.name: role.id for role in all_models.AccessControlRole.query.filter(
          # Using like `Audit%` because all audit roles start with `Audit`
          # e.g. Auditors, Audit Captains, Audit Captains Mapped
          all_models.AccessControlRole.name.like("Audit%")
      ).options(load_only("id", "name")).all()
  }, "acl_audit_roles")


def _create_mapped_acls(acl, relationship_cache, snapshots_cache, role_map):
  """Helper to propagate roles for auditors and captains"""
  audit = acl.object
  assert isinstance(audit, all_models.Audit), \
      "`{}` role assigned to a non Audit object.".format(acl.ac_role.name)

  # Add Audit Captains Mapped role to all the objects in the audit
  if audit.id not in snapshots_cache:
    snapshots_cache[audit.id] = all_models.Snapshot.query.filter(
        all_models.Snapshot.parent_id == audit.id,
        all_models.Snapshot.parent_type == "Audit"
    ).options(load_only("id")).all()

  for snapshot in snapshots_cache[audit.id]:
    all_models.AccessControlList(
        object=snapshot,
        parent=acl,
        person=acl.person,
        ac_role_id=role_map["Snapshot"]
    )

  # Add Audit Captains Mapped to all related
  audit_stub = Stub(acl.object_type, acl.object_id)
  related_stubs = related([audit_stub], relationship_cache)

  for stub in related_stubs[audit_stub]:
    all_models.AccessControlList(
        object_id=stub.id,
        object_type=stub.type,
        parent=acl,
        person=acl.person,
        ac_role_id=role_map[stub.type]
    )

  # Add Audit Captains Mapped to all realted comments and documents
  mapped_stubs = related(related_stubs[audit_stub], relationship_cache)
  for parent in mapped_stubs:
    for stub in mapped_stubs[parent]:
      if stub.type not in ("Comment", "Document"):
        continue
      all_models.AccessControlList(
          object_id=stub.id,
          object_type=stub.type,
          parent=acl,
          person=acl.person,
          ac_role_id=role_map[stub.type]
      )


def _auditors_handler(acl, audit_roles,
                      relationship_cache, snapshots_cache):
  """Handle auditor role propagation"""
  role_map = defaultdict(lambda: audit_roles['Auditors Mapped'], {
      "Snapshot": audit_roles["Auditors Snapshot Mapped"],
      "Assessment": audit_roles["Auditors Assessment Mapped"],
      "Issue": audit_roles["Auditors Issue Mapped"],
      "Document": audit_roles["Auditors Document Mapped"]
  })
  _create_mapped_acls(acl, relationship_cache, snapshots_cache, role_map)


def _audit_captains_handler(acl, audit_roles,
                            relationship_cache, snapshots_cache):
  """Handle audit captain permission added"""
  audit = acl.object
  assert isinstance(audit, all_models.Audit), \
      "`Audit Captains` role assigned to a non Audit object."

  # Add program editor to program
  program = audit.program
  if not any(ur for ur in program.context.user_roles
             if ur.person_id == acl.person_id):
    program_editor_id = _get_program_editor_role()
    db.session.add(
        all_models.UserRole(
            role_id=program_editor_id,
            context=program.context,
            person_id=acl.person_id
        )
    )

  role_map = defaultdict(lambda: audit_roles['Audit Captains Mapped'])
  _create_mapped_acls(acl, relationship_cache, snapshots_cache, role_map)


def handle_acl_creation(session, _):
  """Handle legacy audit captain -> program editor role propagation"""
  relationship_cache = RelationshipsCache()
  snapshots_cache = {}
  for obj in session.new:
    if not isinstance(obj, all_models.AccessControlList):
      continue

    audit_roles = _get_acl_audit_roles()
    role_handlers = {
        audit_roles["Audit Captains"]: _audit_captains_handler,
        audit_roles["Auditors"]: _auditors_handler,
    }
    if obj.ac_role_id in role_handlers:
      role_handlers[obj.ac_role_id](obj, audit_roles,
                                    relationship_cache, snapshots_cache)


def init_hook():
  """Initialize AccessControlList-related hooks."""
  sa.event.listen(Session, "after_flush", handle_acl_creation)
