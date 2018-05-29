# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Fill objects_without_revisions table. Delete invalid objects.

Create Date: 2018-05-18 10:25:12.111617
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from ggrc.migrations import utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1a399a5cfed'
down_revision = 'fd8706aad739'


def _add_model_inst_to_obj_without_rev(connection, model_name, table_name):
  """Add info about objects without revisions to corresponding table."""
  sql = """
      SELECT o.id
      FROM {table_name} AS o
      LEFT JOIN revisions AS r
          ON r.resource_type='{model_name}' AND r.resource_id=o.id
      WHERE r.id IS NULL
  """.format(model_name=model_name, table_name=table_name)
  res = connection.execute(sa.text(sql)).fetchall()
  obj_ids = [o.id for o in res]
  if obj_ids:
    utils.add_to_objects_without_revisions_bulk(connection, obj_ids,
                                                model_name)


def _fill_objects_without_revisions_table(connection):
  """Fill objects_without_revisions table for objects without revisions."""
  models = {
      "Cycle": "cycles",
      "CycleTaskEntry": "cycle_task_entries",
      "CycleTaskGroup": "cycle_task_groups",
      "CycleTaskGroupObjectTask": "cycle_task_group_object_tasks",
      "TaskGroup": "task_groups",
      "TaskGroupObject": "task_group_objects",
      "TaskGroupTask": "task_group_tasks",
      "Workflow": "workflows",
      "Control": "controls",
      "Assessment": "assessments",
  }
  for model_name, table_name in models.iteritems():
    _add_model_inst_to_obj_without_rev(connection, model_name, table_name)


def _delete_invalid_objects(connection):
  """Delete invalid objects.

  Invalid objects are:
      Comments that are not mapped to any other object - orphans.
      Revisions for orphan comments.
      Notifications for orphan comments.
  """
  sql = """
      CREATE TEMPORARY TABLE orphan_comments AS
          SELECT DISTINCT c.id FROM comments AS c
              WHERE c.id NOT IN (
                  SELECT r.source_id
                  FROM relationships AS r
                  WHERE r.source_type="Comment"
              ) AND c.id NOT IN (
                  SELECT r.destination_id
                  FROM relationships AS r
                  WHERE r.destination_type="Comment"
              )
  """
  connection.execute(sa.text(sql))

  sql = """
      DELETE FROM revisions
      WHERE resource_type="Comment" AND resource_id IN (
          SELECT oc.id FROM orphan_comments AS oc)
  """
  connection.execute(sa.text(sql))

  sql = """
      DELETE FROM notifications
      WHERE object_type="Comment" AND object_id IN (
          SELECT oc.id FROM orphan_comments AS oc)
  """
  connection.execute(sa.text(sql))

  sql = """
      DELETE FROM comments
      WHERE id IN (SELECT oc.id FROM orphan_comments AS oc)
  """
  connection.execute(sa.text(sql))

  connection.execute(sa.text("DROP TEMPORARY TABLE orphan_comments"))


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  connection = op.get_bind()
  _fill_objects_without_revisions_table(connection)
  _delete_invalid_objects(connection)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  connection = op.get_bind()
  utils.clean_new_revisions(connection)
