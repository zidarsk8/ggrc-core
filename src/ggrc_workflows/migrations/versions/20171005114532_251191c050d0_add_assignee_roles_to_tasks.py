# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add Assignee roles to Task and Cycle Task types

Create Date: 2017-10-05 11:45:32.172481
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op


# revision identifiers, used by Alembic.
revision = '251191c050d0'
down_revision = '4131bd4a8a4d'


CREATE_ASSIGNEE = (
    """
       INSERT INTO access_control_roles
       (name, object_type, created_at, updated_at,
        mandatory, non_editable, `delete`)
       SELECT 'Task Assignees', '{object_type}', NOW(), NOW(),
              1, 1, 0
       FROM access_control_roles
       WHERE NOT EXISTS(
          SELECT id FROM access_control_roles
          WHERE name = 'Task Assignees' AND object_type = '{object_type}'
       )
       LIMIT 1
    """
)

INSERT_SQL = """
INSERT INTO access_control_list
    (person_id, object_id, ac_role_id, object_type, created_at, updated_at)
SELECT t.contact_id, t.id, r.id, r.object_type, now(), now()
FROM task_group_tasks as t
JOIN access_control_roles as r on r.object_type = "TaskGroupTask"
WHERE t.contact_id IS NOT NULL and r.name = "Task Assignees"
UNION ALL
SELECT t.contact_id, t.id, r.id, r.object_type, now(), now()
FROM cycle_task_group_object_tasks as t
JOIN access_control_roles as r on r.object_type = "CycleTaskGroupObjectTask"
where t.contact_id IS NOT NULL AND r.name = "Task Assignees";
"""

DELETE_SQL = """
DELETE acr, acl
FROM access_control_roles AS acr
INNER JOIN access_control_list AS acl
WHERE
    acl.ac_role_id = acr.id AND
    acr.name = "Task Assignees" AND (
        acr.object_type = "TaskGroupTask" OR
        acr.object_type = "CycleTaskGroupObjectTask"
    )
"""


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.execute(CREATE_ASSIGNEE.format(object_type="TaskGroupTask"))
  op.execute(CREATE_ASSIGNEE.format(object_type="CycleTaskGroupObjectTask"))
  op.execute(INSERT_SQL)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.execute(DELETE_SQL)
