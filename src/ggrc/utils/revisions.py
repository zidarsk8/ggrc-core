# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Utility class for handling revisions."""

from collections import defaultdict
from logging import getLogger

from sqlalchemy.sql import select
from sqlalchemy import func

from ggrc import db
from ggrc.models import all_models

logger = getLogger(__name__)  # pylint: disable=invalid-name


def _get_revisions_by_type():
  """Get latest revisions for all existing objects

  Returns:
    dict with model name as key and list of latest revisions for that model.
  """
  valid_types = [model.__name__ for model in all_models.all_models]
  revisions_table = all_models.Revision.__table__
  id_query = select([
      func.max(revisions_table.c.id),
  ]).group_by(
      revisions_table.c.resource_type,
      revisions_table.c.resource_id,
  )
  ids = [row for (row,) in db.session.execute(id_query)]
  query = select([
      revisions_table.c.id,
      revisions_table.c.resource_type,
      revisions_table.c.resource_id,
  ]).where(
      revisions_table.c.resource_type.in_(valid_types)
  ).where(
      revisions_table.c.action != "deleted"
  ).where(
      revisions_table.c.id.in_(ids)
  ).order_by(
      revisions_table.c.resource_type,
  )

  rows_by_type = defaultdict(list)
  for row in db.session.execute(query):
    rows_by_type[row.resource_type].append(row)

  return rows_by_type


def _fix_type_revisions(type_, rows):
  """Update revision content for all rows of a given model type."""
  model = getattr(all_models, type_, None)
  revisions_table = all_models.Revision.__table__
  if not model:
    logger.warning("Failed to update revisions for invalid model: %s", type_)
    return

  ids = [row.resource_id for row in rows]
  objects = model.eager_query().filter(model.id.in_(ids))

  obj_content_map = {obj.id: obj.log_json() for obj in objects}

  for row in rows:
    # This if statement checks that we only update content for objects that
    # exist. If an object has been deleted via import or in some other way that
    # its delete revision was not created, this if statement will prevent a
    # false error.
    # Note: there will be other migrations that deal with adding missing
    # revisions for those deleted objects.
    if row.resource_id in obj_content_map:
      db.session.execute(
          revisions_table.update()
          .where(revisions_table.c.id == row.id)
          .values(content=obj_content_map[row.resource_id])
      )
  db.session.commit()


def do_refresh_revisions():
  """Update last revisions of models with fixed data."""

  rows_by_type = _get_revisions_by_type()

  for type_, rows in rows_by_type.iteritems():
    logger.info("Updating revisions for: %s", type_)
    _fix_type_revisions(type_, rows)
