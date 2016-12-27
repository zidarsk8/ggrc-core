# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Utility class for handling revisions."""

from logging import getLogger

from sqlalchemy.sql import select
from sqlalchemy import func

from ggrc import db
from ggrc.models import all_models

logger = getLogger(__name__)  # pylint: disable=invalid-name


def _get_revisions_by_type(type_):
  """Get latest revisions for all existing objects

  Args:
    type_ (str): the resource_type of revisions to fetch.

  Returns:
    dict with object_id as key and revision_id of the latest revision as value.
  """
  revisions_table = all_models.Revision.__table__
  id_query = select([
      func.max(revisions_table.c.id),
  ]).where(
      revisions_table.c.resource_type == type_,
  ).group_by(
      revisions_table.c.resource_id,
  )
  ids = [row for (row,) in db.session.execute(id_query)]

  if ids:
    query = select([
        revisions_table.c.id,
        revisions_table.c.resource_id,
    ]).where(
        revisions_table.c.action != "deleted"
    ).where(
        revisions_table.c.id.in_(ids)
    )

    return {row.resource_id: row.id for row in db.session.execute(query)}

  else:
    # no revisions found
    return {}


def _fix_type_revisions(type_, obj_rev_map):
  """Update revision content for all rows of a given model type."""
  model = getattr(all_models, type_, None)
  revisions_table = all_models.Revision.__table__
  if not model:
    logger.warning("Failed to update revisions for invalid model: %s", type_)
    return

  if not hasattr(model, "log_json"):
    logger.warning("Model '%s' has no log_json method, revision generation "
                   "skipped", type_)
    return

  ids = list(obj_rev_map.keys())
  if ids:
    objects_with_revisions = model.eager_query().filter(model.id.in_(ids))
  else:
    objects_with_revisions = []

  for obj in objects_with_revisions:
    # This block only updates the content of existing revisions and does not
    # recreate missing revision objects
    rev_id = obj_rev_map.pop(obj.id)
    # Update revisions_table.content to the latest object's json
    db.session.execute(
        revisions_table.update()
        .where(revisions_table.c.id == rev_id)
        .values(content=obj.log_json())
    )

  db.session.commit()


def do_refresh_revisions():
  """Update last revisions of models with fixed data."""

  valid_types = {model.__name__ for model in all_models.all_models}

  # No sense in storing revisions for Revisions or Events
  valid_types -= {"Revision", "Event"}

  # Not storing revisions for RelationshipAttrs (part of Relationships)
  valid_types -= {"RelationshipAttr"}

  for type_ in valid_types:
    logger.info("Updating revisions for: %s", type_)
    _fix_type_revisions(type_, _get_revisions_by_type(type_))
