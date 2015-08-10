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
down_revision = '4840f4760f4b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from datetime import date
from ggrc.app import app
from ggrc import settings, db
import ggrc_workflows.models as models
from ggrc_workflows import adjust_next_cycle_start_date
from ggrc_workflows.services.workflow_cycle_calculator import \
    get_cycle_calculator


def upgrade():
    op.add_column('workflows',
                  sa.Column('non_adjusted_next_cycle_start_date',
                  sa.Date(), nullable=True))

    workflows = db.session.query(models.Workflow) \
        .filter(
        models.Workflow.next_cycle_start_date != None,
        models.Workflow.non_adjusted_next_cycle_start_date == None,
        models.Workflow.recurrences == True,
        models.Workflow.status == 'Active',
        models.Workflow.next_cycle_start_date >= date.today()
    ).all()

    app.logger.info("Setting up non-adjusted next cycle start date and "
                    "adjusting existing NCSD...")
    for workflow in workflows:
        tasks_start_days = [task.relative_start_day
                                for tg in workflow.task_groups
                                for task in tg.task_group_tasks]

        tasks_end_days = [task.relative_end_day
                            for tg in workflow.task_groups
                            for task in tg.task_group_tasks]

        # We must skip tasks that don't have start days and end days defined
        if ((not all(tasks_start_days) and not all(tasks_end_days)) or
            (not tasks_start_days and not tasks_end_days)):
            append_msg = ""
            if workflow.next_cycle_start_date:
                workflow.next_cycle_start_date = None
                append_msg += (" Removing existing next cycle start date "
                               "because none are configured.")
                db.session.add(workflow)

            app.logger.info(
                "Skipping workflow {0} (ID: {1}) because it doesn't "
                "have relative start and end days specified.{2}".format(
                    workflow.title,
                    workflow.id,
                    append_msg
                ))
            continue

        pre_compute_ncsd = workflow.next_cycle_start_date
        last_cycle_start_date = None
        if workflow.cycles:
            last_cycle_start_date = max([c.start_date for c in workflow.cycles])

        if last_cycle_start_date:
            base_date = last_cycle_start_date
        else:
            base_date = base_date.today()

        base_date = max(base_date, workflow.next_cycle_start_date)
        calculator = get_cycle_calculator(workflow, base_date=base_date)

        if workflow.frequency in {"weekly", "monthly"}:
            nancsd_day = min(
                v['relative_start'] for v in calculator.reified_tasks.values())
            nancsd_month = None
        else:
            nancsd_month, nancsd_day = min(
                v['relative_start'] for v in calculator.reified_tasks.values())

        nancsd_date = calculator.relative_day_to_date(
            relative_day=nancsd_day,
            relative_month=nancsd_month,
            base_date=base_date)

        if last_cycle_start_date:
            while calculator.adjust_date(nancsd_date) <= last_cycle_start_date:
                base_date = base_date + calculator.time_delta
                nancsd_date = calculator.relative_day_to_date(
                    relative_day=nancsd_day,
                    relative_month=nancsd_month,
                    base_date=base_date
                )
        else:
            base_date = base_date - calculator.time_delta
            while calculator.adjust_date(nancsd_date) <= pre_compute_ncsd:
                base_date = base_date + calculator.time_delta
                nancsd_date = calculator.relative_day_to_date(
                    relative_day=nancsd_day,
                    relative_month=nancsd_month,
                    base_date=base_date
                )

        workflow.non_adjusted_next_cycle_start_date = nancsd_date
        workflow.next_cycle_start_date = calculator.adjust_date(nancsd_date)
        post_compute_ncsd = workflow.next_cycle_start_date

        start_dates = ["{}/{}".format(
            task.relative_start_month,
            task.relative_start_day) for tg in workflow.task_groups
                                     for task in tg.task_group_tasks]
        end_dates = ["{}/{}".format(
            task.relative_end_month,
            task.relative_end_day) for tg in workflow.task_groups
                                   for task in tg.task_group_tasks]

        diff_mark = ""
        if pre_compute_ncsd != post_compute_ncsd:
            diff_mark = "!! ADJUSTED !! "

        app.logger.info(
            "{}Workflow with ID: "
            "{}; Freq: {}, PRE: {}, Last cycle: {}, POST: {}, NON: {},"
            "tasks start: {}, tasks end: {},".format(
                diff_mark,
                workflow.id,
                workflow.frequency[:2],
                pre_compute_ncsd,
                last_cycle_start_date,
                post_compute_ncsd,
                workflow.non_adjusted_next_cycle_start_date,
                start_dates,
                end_dates))
        db.session.add(workflow)
    app.logger.info("Finished setting up non-adjusted next cycle start date.")

    # If somebody deleted all the tasks we should clear the next cycle start
    # date
    workflows = db.session.query(models.Workflow) \
        .filter(
        models.Workflow.next_cycle_start_date != None,
        models.Workflow.recurrences == True,
        models.Workflow.status == 'Active',
        models.Workflow.next_cycle_start_date < date.today()
    ).all()

    app.logger.info("Removing next cycle start date from tasks that have no "
                    "tasks set up...")
    for workflow in workflows:
        tasks_start_days = [task.relative_start_day
                            for tg in workflow.task_groups
                            for task in tg.task_group_tasks]

        tasks_end_days = [task.relative_end_day
                          for tg in workflow.task_groups
                          for task in tg.task_group_tasks]

        if ((not all(tasks_start_days) and not all(tasks_end_days)) or
                (not tasks_start_days and not tasks_end_days)):
            app.logger.info("Removing NCSD from Workflow: {}. Current NCSD: {}".format(
                workflow.id,
                workflow.next_cycle_start_date
            ))
            workflow.next_cycle_start_date = None
            db.session.add(workflow)
    app.logger.info("Finished removing next cycle start date.")

    # Save
    db.session.commit()

def downgrade():
    op.drop_column('workflows', 'non_adjusted_next_cycle_start_date')
