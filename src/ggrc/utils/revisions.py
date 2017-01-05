# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Utility class for handling revisions."""

from logging import getLogger

from sqlalchemy.sql import select
from sqlalchemy import func
from sqlalchemy import literal
from sqlalchemy import not_

from ggrc import db
from ggrc.login import get_current_user_id
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
    objects_without_revisions = model.eager_query().filter(
        not_(model.id.in_(ids)),
    )
  else:
    objects_with_revisions = []
    objects_without_revisions = model.eager_query()

  for obj in objects_with_revisions:
    rev_id = obj_rev_map.pop(obj.id)
    # Update revisions_table.content to the latest object's json
    db.session.execute(
        revisions_table.update()
        .where(revisions_table.c.id == rev_id)
        .values(content=obj.log_json())
    )

  # Every revision present in obj_rev_map has no object in the DB
  missing_delete_revisions = list(obj_rev_map.values())

  # Every object with id not present in obj_
  missing_create_revisions = [
      (obj.id, obj.log_json()) for obj in objects_without_revisions
  ]

  if missing_delete_revisions or missing_create_revisions:
    # Log a "BULK" event for missing revision creation
    event = all_models.Event(action="BULK")
    db.session.add(event)
    db.session.flush([event])  # to get its id

  if missing_delete_revisions:
    # For each lost object log a "deleted" revision with content identical to
    # the last logged revision
    _recover_delete_revisions(revisions_table, event, missing_delete_revisions)

  if missing_create_revisions:
    # For each unlogged object log a "created"/"modified" revision with content
    # equal to obj.log_json()
    _recover_create_revisions(revisions_table, event,
                              type_, missing_create_revisions)

  db.session.commit()


def _recover_delete_revisions(revisions_table, event,
                              last_available_revision_ids):
  """Log an action="deleted" copy for revisions with ids in passed list."""
  columns_to_clone = sorted(set(c.name for c in revisions_table.c) -
                            {"id", "event_id", "action", "created_at",
                             "updated_at"})
  db.session.execute(
      revisions_table.insert().from_select(
          ["event_id",
           "action",
           "created_at",
           "updated_at"] + columns_to_clone,
          select(
              [event.id,
               literal("deleted"),
               func.now(),
               func.now()] + columns_to_clone,
          ).select_from(
              revisions_table,
          ).where(
              revisions_table.c.id.in_(last_available_revision_ids),
          ),
      ),
  )


def _recover_create_revisions(revisions_table, event, object_type,
                              object_ids_with_jsons):
  """Log a "created"/"modified" revision for every passed object's json.

  If json["updated_at"] == json["created_at"], log action="created".
  If json["updated_at"] != json["created_at"], log action="modified".
  """
  def determine_action(obj_content):
    if obj_content.get("created_at") != obj_content.get("updated_at"):
      return "modified"
    else:
      return "created"

  db.session.execute(
      revisions_table.insert(),
      [{"resource_id": obj_id,
        "resource_type": object_type,
        "event_id": event.id,
        "action": determine_action(obj_content),
        "content": obj_content,
        "context_id": obj_content.get("context_id"),
        "modified_by_id": (obj_content.get("modified_by_id") or
                           get_current_user_id()),
        "source_type": obj_content.get("source_type"),
        "source_id": obj_content.get("source_id"),
        "destination_type": obj_content.get("destination_type"),
        "destination_id": obj_content.get("destination_id")}
       for (obj_id, obj_content) in object_ids_with_jsons],
  )


def do_refresh_revisions():
  """Update last revisions of models with fixed data."""

  valid_types = {model.__name__ for model in all_models.all_models}

  # No sense in storing revisions for Revisions or Events
  valid_types -= {"Revision", "Event"}

  # Not storing revisions for RelationshipAttrs (part of Relationships)
  valid_types -= {"RelationshipAttr"}

  # TODO: fix the errors for the next excluded types and remove this block
  valid_types -= {
      "BackgroundTask",  # over max content length
      "Role",  # no FK by modified_by_id to Person
      "RiskObject",  # does not mix in Relatable, thus fails on eager_query
  }

  for type_ in sorted(valid_types):
    logger.info("Updating revisions for: %s", type_)
    _fix_type_revisions(type_, _get_revisions_by_type(type_))
