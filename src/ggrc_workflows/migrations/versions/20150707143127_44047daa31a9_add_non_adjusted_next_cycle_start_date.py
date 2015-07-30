# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

"""Add non-adjusted next cycle start date

Revision ID: 44047daa31a9
Revises: 1431e7094e26
Create Date: 2015-07-07 14:31:27.780564

"""

# revision identifiers, used by Alembic.

revision = '44047daa31a9'
down_revision = '3605dca868e4'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from datetime import date
from ggrc.app import app
from ggrc import settings, db
import ggrc_workflows.models as models

def upgrade():
    op.add_column('workflows', sa.Column('non_adjusted_next_cycle_start_date', sa.Date(), nullable=True))

    from ggrc_workflows import adjust_next_cycle_start_date
    from ggrc_workflows.services.workflow_cycle_calculator import get_cycle_calculator


    # Get all active workflows that have:
    # 1. next_cycle_start_date_set,
    # 2. are non-one time
    # 3. are active
    # 4. it's tasks have relative days set OR has any tasks at all
    workflows = db.session.query(models.Workflow) \
        .filter(
        models.Workflow.next_cycle_start_date != None,
        models.Workflow.recurrences == True,
        models.Workflow.status == 'Active',
        models.Workflow.next_cycle_start_date >= date.today()
    ).all()

    for workflow in workflows:
        tasks_start_days = [task.relative_start_day
                                for tg in workflow.task_groups
                                for task in tg.task_group_tasks]

        tasks_end_days = [task.relative_end_day
                            for tg in workflow.task_groups
                            for task in tg.task_group_tasks]

        pre_compute_ncsd = workflow.next_cycle_start_date

        # We must skip tasks that don't have start days and end days defined
        if ((not all(tasks_start_days) and not all(tasks_end_days)) or
            (not tasks_start_days and not tasks_end_days)):
            app.logger.info(
                "Skipping workflow {0} (ID: {1}) because it doesn't "
                "have relative start and end days specified".format(
                    workflow.title,
                    workflow.id))
            continue

        # We want to calculate values as if we are on the date of
        # next cycle start date (either in the past or in the future).
        #
        # That is why we first get the minimum relative start, convert
        # to date manually to avoid  and instantiate a new calculator with base date
        # on that date.
        calculator = get_cycle_calculator(workflow)
        if workflow.frequency in {"weekly", "monthly"}:
            start_day = min(
                v['relative_start'] for v in calculator.reified_tasks.values())
            start_date = calculator.relative_day_to_date(
                relative_day=start_day)
        else:
            start_month, start_day = min(
                v['relative_start'] for v in calculator.reified_tasks.values())
            start_date = calculator.relative_day_to_date(
                relative_day=start_day,
                relative_month=start_month)

        calculator = get_cycle_calculator(workflow, base_date=start_date)
        adjust_next_cycle_start_date(calculator, workflow)
        post_compute_ncsd = workflow.next_cycle_start_date
        if (pre_compute_ncsd != post_compute_ncsd and
                post_compute_ncsd not in [c.start_date for c in workflow.cycles]):
            start_dates = ["{}/{}".format(task.relative_start_month, task.relative_start_day) for tg in workflow.task_groups for task in tg.task_group_tasks]
            end_dates = ["{}/{}".format(task.relative_end_month, task.relative_end_day) for tg in workflow.task_groups for task in tg.task_group_tasks]

            app.logger.info("Fixed next cycle start date for Workflow with ID: {}; Freq: {}, PRE: {}, POST: {}, NON: {}, tasks start: {}, tasks end: {}".format(
                workflow.id,
                workflow.frequency[:2],
                pre_compute_ncsd,
                post_compute_ncsd,
                workflow.non_adjusted_next_cycle_start_date,
                start_dates,
                end_dates))
        db.session.add(workflow)
    # Save
    db.session.commit()

def downgrade():
    op.drop_column('workflows', 'non_adjusted_next_cycle_start_date')
