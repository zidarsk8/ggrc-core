# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""fill notification_types table

Revision ID: 27b09c761b4e
Revises: 4f9f00e4faca
Create Date: 2015-04-04 15:36:39.540261

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = '27b09c761b4e'
down_revision = '4f9f00e4faca'


def upgrade():
  notification_types_table = table(
      'notification_types',
      column('id', sa.Integer),
      column('name', sa.String),
      column('description', sa.Text),
      column('template', sa.String),
      column('advance_notice', sa.Integer),
      column('advance_notice_end', sa.Integer),
      column('created_at', sa.DateTime),
      column('modified_by_id', sa.Integer),
      column('updated_at', sa.DateTime),
      column('context_id', sa.Integer),
  )

  op.bulk_insert(
      notification_types_table,
      [
          {"name": "cycle_created",
           "description": ("Notify workflow members that a one time workflow "
                           "has been started and send them their assigned "
                           "tasks."),
           "template": "cycle_created",
           "advance_notice": 0,
           },
          {"name": "manual_cycle_created",
           "description": ("Notify workflow members that a one time workflow "
                           "has been started and send them their assigned "
                           "tasks."),
           "template": "manual_cycle_created",
           "advance_notice": 0,
           },
          {"name": "cycle_task_due_in",
           "description": "Notify task assignee his task is due in X days",
           "template": "cycle_task_due_in",
           "advance_notice": 1,
           },
          {"name": "cycle_task_due_today",
           "description": "Notify task assignee his task is due today",
           "template": "cycle_task_due_today",
           "advance_notice": 0,
           },
          {"name": "cycle_task_reassigned",
           "description": "Notify task assignee his task is due today",
           "template": "cycle_task_due_today",
           "advance_notice": 0,
           },
          {"name": "task_group_assignee_change",
           "description": "Email owners on task group assignee change.",
           "template": "task_group_assignee_change",
           "advance_notice": 0,
           },
          {"name": "weekly_workflow_starts_in",
           "description": "Advanced notification for a reccuring workflow.",
           "template": "weekly_workflow_starts_in",
           "advance_notice": 1,
           },
          {"name": "monthly_workflow_starts_in",
           "description": "Advanced notification for a reccuring workflow.",
           "template": "monthly_workflow_starts_in",
           "advance_notice": 3,
           },
          {"name": "quaterly_workflow_starts_in",
           "description": "Advanced notification for a reccuring workflow.",
           "template": "quaterly_workflow_starts_in",
           "advance_notice": 7,
           },
          {"name": "annually_workflow_starts_in",
           "description": "Advanced notification for a reccuring workflow.",
           "template": "annual_workflow_starts_in",
           "advance_notice": 15,
           },
      ]
  )


def downgrade():
  pass
