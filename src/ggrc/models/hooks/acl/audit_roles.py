# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""All hooks required by audit roles business cases"""

import sqlalchemy as sa

from ggrc import db
from ggrc import login
from ggrc.models import all_models


def _insert_select_acls(select_statement):
  """Insert acl records from the select statement

  Args:
    select_statement: sql statement that contains the following columns
      person_id,
      ac_role_id,
      object_id,
      object_type,
      created_at,
      modified_by_id,
      updated_at,
      parent_id,
  """

  acl_table = all_models.AccessControlList.__table__

  inserter = acl_table.insert().prefix_with("IGNORE")

  db.session.execute(
      inserter.from_select(
          [
              acl_table.c.person_id,
              acl_table.c.ac_role_id,
              acl_table.c.object_id,
              acl_table.c.object_type,
              acl_table.c.created_at,
              acl_table.c.modified_by_id,
              acl_table.c.updated_at,
              acl_table.c.parent_id,
          ],
          select_statement
      )
  )


def _handle_snapshot_mappings(parent_acl_ids):
  snapshot_table = all_models.Snapshot.__table__
  acl_table = all_models.AccessControlList.__table__
  parent_acr = all_models.AccessControlRole.__table__.alias("parent_acr")
  child_acr = all_models.AccessControlRole.__table__.alias("child_acr")

  select_statement = sa.select([
      acl_table.c.person_id,
      child_acr.c.id,
      snapshot_table.c.id,
      sa.literal(all_models.Snapshot.__name__),
      sa.func.now(),
      sa.literal(login.get_current_user_id()),
      sa.func.now(),
      acl_table.c.id,
  ]).select_from(
      sa.join(
          sa.join(
              sa.join(
                  snapshot_table,
                  acl_table,
                  sa.and_(
                      acl_table.c.object_id == snapshot_table.c.parent_id,
                      acl_table.c.object_type == snapshot_table.c.parent_type,
                  )
              ),
              parent_acr,
              parent_acr.c.id == acl_table.c.ac_role_id
          ),
          child_acr,
          child_acr.c.parent_id == parent_acr.c.id
      )
  ).where(
      sa.and_(
          acl_table.c.id.in_(parent_acl_ids),
          child_acr.c.object_type == all_models.Snapshot.__name__,
      )
  )
  _insert_select_acls(select_statement)


def _rel_parent(parent_acl_ids, source=True):
  """Get left side of relationships mappings through source."""
  rel_table = all_models.Relationship.__table__
  acl_table = all_models.AccessControlList.__table__
  parent_acr = all_models.AccessControlRole.__table__.alias("parent_acr")
  child_acr = all_models.AccessControlRole.__table__.alias("child_acr")

  if source:
    acl_link = sa.and_(
        acl_table.c.object_id == rel_table.c.source_id,
        acl_table.c.object_type == rel_table.c.source_type,
    )
  else:
    acl_link = sa.and_(
        acl_table.c.object_id == rel_table.c.destination_id,
        acl_table.c.object_type == rel_table.c.destination_type,
    )

  select_statement = sa.select([
      acl_table.c.person_id,
      child_acr.c.id,
      rel_table.c.id,
      sa.literal(all_models.Relationship.__name__),
      sa.func.now(),
      sa.literal(login.get_current_user_id()),
      sa.func.now(),
      acl_table.c.id,
  ]).select_from(
      sa.join(
          sa.join(
              sa.join(
                  rel_table,
                  acl_table,
                  acl_link
              ),
              parent_acr,
              parent_acr.c.id == acl_table.c.ac_role_id
          ),
          child_acr,
          child_acr.c.parent_id == parent_acr.c.id
      )
  ).where(
      sa.and_(
          acl_table.c.id.in_(parent_acl_ids),
          child_acr.c.object_type == all_models.Relationship.__name__
      )
  )
  return select_statement


def _rel_child(parent_acl_ids, source=True):
  """Get left side of relationships mappings through source."""
  rel_table = all_models.Relationship.__table__
  acl_table = all_models.AccessControlList.__table__
  parent_acr = all_models.AccessControlRole.__table__.alias("parent_acr")
  child_acr = all_models.AccessControlRole.__table__.alias("child_acr")

  if source:
    object_id = rel_table.c.destination_id
    object_type = rel_table.c.destination_type
  else:
    object_id = rel_table.c.source_id
    object_type = rel_table.c.source_type

  acl_link = sa.and_(
      acl_table.c.object_id == rel_table.c.id,
      acl_table.c.object_type == all_models.Relationship.__name__,
  )

  select_statement = sa.select([
      acl_table.c.person_id,
      child_acr.c.id,
      object_id,
      object_type,
      sa.func.now(),
      sa.literal(login.get_current_user_id()),
      sa.func.now(),
      acl_table.c.id,
  ]).select_from(
      sa.join(
          sa.join(
              sa.join(
                  rel_table,
                  acl_table,
                  acl_link
              ),
              parent_acr,
              parent_acr.c.id == acl_table.c.ac_role_id
          ),
          child_acr,
          child_acr.c.parent_id == parent_acr.c.id
      )
  ).where(
      sa.and_(
          acl_table.c.id.in_(parent_acl_ids),
          child_acr.c.object_type == object_type,
      )
  )
  return select_statement


def _get_child_ids(parent_ids, child_names):
  """Get all acl ids for acl entries with the given parent ids

  Args:
    parent_ids: list of parent acl entries or query with parent ids.

  Returns:
    list of ACL ids for all children from the given parents.
  """
  acl_table = all_models.AccessControlList.__table__

  return sa.select([acl_table.c.id]).where(
      acl_table.c.parent_id.in_(parent_ids)
  ).where(
      acl_table.c.object_type.in_(child_names)
  )


def _handle_relationships(parent_acl_ids):
  """Handle role propagation through relationships.

  For handling relationships of type:
  Audit > Relationship > Object

  The parent part of this function refers to propagation from Audit to
  Relationship. The child part refers to propagation from Relationship to
  Object (either Assessment, Issue, Document, Comment)
  """

  src_select = _rel_parent(parent_acl_ids, source=True)
  dst_select = _rel_parent(parent_acl_ids, source=False)
  select_statement = sa.union(src_select, dst_select)
  _insert_select_acls(select_statement)

  new_parent_ids = _get_child_ids(
      parent_acl_ids,
      [all_models.Relationship.__name__]
  )

  src_select = _rel_child(new_parent_ids, source=True)
  dst_select = _rel_child(new_parent_ids, source=False)
  select_statement = sa.union(src_select, dst_select)
  _insert_select_acls(select_statement)

  return _get_child_ids(
      new_parent_ids,
      [
          all_models.Issue.__name__,
          all_models.Assessment.__name__,
      ]
  )


def handle_audit_acl(acls):
  if not acls:
    return
  acl_ids = [acl.id for acl in acls]
  related_acl_ids = _handle_relationships(acl_ids)
  _handle_relationships(related_acl_ids)
  _handle_snapshot_mappings(acl_ids)
