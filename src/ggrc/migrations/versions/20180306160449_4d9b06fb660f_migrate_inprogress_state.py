# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Migrate "In Progress" status.

Create Date: 2018-03-06 16:04:49.536779
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op


# revision identifiers, used by Alembic.
revision = '4d9b06fb660f'
down_revision = '4489d0ec0076'


UPGRADE_TEMPLATE = """
UPDATE {} SET status = 'In Progress' WHERE status = 'InProgress'
"""


DOWNGRADE_TEMPLATE = """
UPDATE {} SET status = 'InProgress' WHERE status = 'In Progress'
"""


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.execute(UPGRADE_TEMPLATE.format("cycles"))
  op.execute(UPGRADE_TEMPLATE.format("cycle_task_groups"))
  op.execute(UPGRADE_TEMPLATE.format("cycle_task_group_object_tasks"))


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.execute(DOWNGRADE_TEMPLATE.format("cycles"))
  op.execute(DOWNGRADE_TEMPLATE.format("cycle_task_groups"))
  op.execute(DOWNGRADE_TEMPLATE.format("cycle_task_group_object_tasks"))
