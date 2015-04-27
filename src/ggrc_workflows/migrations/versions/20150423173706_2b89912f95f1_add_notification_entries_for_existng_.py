
"""add notification entries for existng workflows

Revision ID: 2b89912f95f1
Revises: 27b09c761b4e
Create Date: 2015-04-23 17:37:06.366115

"""

from datetime import date
from sqlalchemy import and_
from ggrc import db
from ggrc.models import Notification
from ggrc_workflows.models import CycleTaskGroupObjectTask, Workflow
from ggrc_workflows.notification.notification_handler import (
    add_cycle_task_due_notifications,
    handle_workflow_modify,
    get_notification_type,
)

# revision identifiers, used by Alembic.
revision = '2b89912f95f1'
down_revision = '27b09c761b4e'


def upgrade():
  existing_tasks = CycleTaskGroupObjectTask.query.filter(and_(
      CycleTaskGroupObjectTask.end_date >= date.today(),
      CycleTaskGroupObjectTask.status != "Verified"
  )).all()
  for cycle_task in existing_tasks:
    if cycle_task.end_date >= date.today():
      add_cycle_task_due_notifications(cycle_task)

  existing_wfs = Workflow.query.filter(and_(
      Workflow.frequency.in_(["weekly", "monthly", "quarterly", "annually"]),
      Workflow.next_cycle_start_date >= date.today()
  ))
  for wf in existing_wfs:
    handle_workflow_modify(None, wf)

  db.session.commit()


def downgrade():
  delete_types_list = [
      "cycle_task_due_in",
      "one_time_cycle_task_due_in",
      "weekly_cycle_task_due_in",
      "monthly_cycle_task_due_in",
      "quarterly_cycle_task_due_in",
      "annually_cycle_task_due_in",
      "cycle_task_due_today",
      "weekly_workflow_starts_in",
      "monthly_workflow_starts_in",
      "quarterly_workflow_starts_in",
      "annually_workflow_starts_in",
  ]

  for delete_type in delete_types_list:
    notif_type = get_notification_type(delete_type)
    Notification.query.filter(
        Notification.notification_type == notif_type).delete()

  db.session.commit()
