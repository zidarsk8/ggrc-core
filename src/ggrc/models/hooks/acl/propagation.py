# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Entry point for all acl handlers.

This package should have the single hook that should handle all acl propagation
and deletion.
"""

import flask
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

  db.session.execute(
      acl_table.insert().from_select(
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
  db.session.plain_commit()


def _rel_parent(parent_acl_ids=None, relationship_ids=None, source=True):
  """Get left side of relationships mappings through source."""
  rel_table = all_models.Relationship.__table__
  acl_table = all_models.AccessControlList.__table__
  parent_acr = all_models.AccessControlRole.__table__.alias(
      "parent_acr_{}".format(source)
  )
  child_acr = all_models.AccessControlRole.__table__.alias(
      "child_acr_{}".format(source)
  )
  where_conditions = [
      child_acr.c.object_type == all_models.Relationship.__name__,
  ]
  if relationship_ids is not None:
    where_conditions.append(rel_table.c.id.in_(relationship_ids))
    if parent_acl_ids:
      where_conditions.append(~acl_table.c.id.in_(parent_acl_ids))
  elif parent_acl_ids is not None:
    where_conditions.append(acl_table.c.id.in_(parent_acl_ids))

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
      acl_table.c.person_id.label("person_id"),
      child_acr.c.id.label("ac_role_id"),
      rel_table.c.id.label("object_id"),
      sa.literal(all_models.Relationship.__name__).label("object_type"),
      sa.func.now().label("created_at"),
      sa.literal(login.get_current_user_id()).label("modified_by_id"),
      sa.func.now().label("updated_at"),
      acl_table.c.id.label("parent_id"),
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
      sa.and_(*where_conditions)
  )
  return select_statement


def _rel_child(parent_acl_ids, source=True):
  """Get left side of relationships mappings through source."""
  rel_table = all_models.Relationship.__table__
  acl_table = all_models.AccessControlList.__table__
  parent_acr = all_models.AccessControlRole.__table__.alias(
      "parent_acr_{}".format(source)
  )
  child_acr = all_models.AccessControlRole.__table__.alias(
      "child_acr_{}".format(source)
  )

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
      acl_table.c.person_id.label("person_id"),
      child_acr.c.id.label("ac_role_id"),
      object_id.label("object_id"),
      object_type.label("object_type"),
      sa.func.now().label("created_at"),
      sa.literal(login.get_current_user_id()).label("modified_by_id"),
      sa.func.now().label("updated_at"),
      acl_table.c.id.label("parent_id"),
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


def _get_relationship_acl_ids(relationship_ids):
  """Get ACL ids for the given relationship ids.

  Note that in the first layer of propagation this function acts the same way
  as _get_child_ids does in all higher levels.

  Args:
    relationship_ids: list of parent acl entries or query with parent ids.
  Returns:
    list of ACL ids that belong to given relationships.
  """
  acl_table = all_models.AccessControlList.__table__

  return sa.select([acl_table.c.id]).where(
      sa.and_(
          acl_table.c.object_type == all_models.Relationship.__name__,
          acl_table.c.object_id.in_(relationship_ids),
      )
  )


def _get_child_ids(parent_ids):
  """Get all acl ids for acl entries with the given parent ids

  Args:
    parent_ids: list of parent acl entries or query with parent ids.
  Returns:
    list of ACL ids for all children from the given parents.
  """
  acl_table = all_models.AccessControlList.__table__

  return sa.select([acl_table.c.id]).where(
      acl_table.c.parent_id.in_(parent_ids)
  )


def _handle_propagation_parents(parent_acl_ids):
  """Propagate ACL records from parent objects to relationships."""
  src_select = _rel_parent(parent_acl_ids, source=True)
  dst_select = _rel_parent(parent_acl_ids, source=False)
  select_statement = sa.union(src_select, dst_select)
  _insert_select_acls(select_statement)


def _handle_propagation_children(new_parent_ids):
  """Propagate ACL records from relationships to child objects."""
  src_select = _rel_child(new_parent_ids, source=True)
  dst_select = _rel_child(new_parent_ids, source=False)
  select_statement = sa.union(src_select, dst_select)
  _insert_select_acls(select_statement)


def _handle_propagation_relationships(relationship_ids, new_acl_ids):
  src_select = _rel_parent(
      parent_acl_ids=new_acl_ids,
      relationship_ids=relationship_ids,
      source=True
  )
  dst_select = _rel_parent(
      parent_acl_ids=new_acl_ids,
      relationship_ids=relationship_ids,
      source=False
  )
  select_statement = sa.union(src_select, dst_select)
  _insert_select_acls(select_statement)


def _handle_acl_step(parent_acl_ids):
  """Handle role propagation through relationships.

  For handling relationships of type:
  Audit > Relationship > Object
  The parent part of this function refers to propagation from Audit to
  Relationship. The child part refers to propagation from Relationship to
  Object (either Assessment, Issue, Document, Comment)
  """

  _handle_propagation_parents(parent_acl_ids)
  new_parent_ids = _get_child_ids(parent_acl_ids)
  _handle_propagation_children(new_parent_ids)

  return _get_child_ids(new_parent_ids)


def _handle_relationship_step(relationship_ids, new_acl_ids):
  """Propagate first level or ACLs caused by new relationships."""

  _handle_propagation_relationships(relationship_ids, new_acl_ids)
  new_parent_ids = _get_relationship_acl_ids(relationship_ids)
  _handle_propagation_children(new_parent_ids)

  return _get_child_ids(new_parent_ids)


def _propagate(parent_acl_ids):
  """Propagate ACL entries through the entire propagation tree."""

  propagation_depth_limit = 50

  # The following for statement is a replacement for `while True` statement
  # with a safety cutoff limit.
  for _ in range(propagation_depth_limit):

    child_ids = _handle_acl_step(parent_acl_ids)

    count_query = child_ids.alias("counts").count()
    child_id_count = db.session.execute(count_query).scalar()

    if child_id_count:
      parent_acl_ids = child_ids
    else:
      # Exit the loop when there are no more ACL entries to propagate
      break


def _propagate_relationships(relationship_ids, new_acl_ids):
  if not relationship_ids:
    return
  child_ids = _handle_relationship_step(relationship_ids, new_acl_ids)
  _propagate(child_ids)


def propagate():
  """Propagate all ACLs caused by objects in new_objects list.

  Args:
    new_acl_ids: list of newly created ACL ids,
    new_relationship_ids: list of newly created relationship ids,
  """
  if not (hasattr(flask.g, "new_acl_ids") and
          hasattr(flask.g, "new_relationship_ids")):
    return

  # The order of propagation of relationships and other ACLs is important
  # because relationship code excludes other ACLs from propagating.
  if flask.g.new_relationship_ids:
    _propagate_relationships(flask.g.new_relationship_ids, flask.g.new_acl_ids)
  if flask.g.new_acl_ids:
    _propagate(flask.g.new_acl_ids)

  del flask.g.new_acl_ids
  del flask.g.new_relationship_ids
