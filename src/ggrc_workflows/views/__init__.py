# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

from datetime import date
from flask import render_template, redirect, url_for
from jinja2 import Environment, PackageLoader

from ggrc import db
from ggrc.app import app
from ggrc.login import login_required
from ggrc.views.cron import run_job
from ggrc_workflows import start_recurring_cycles
from ggrc_workflows.models import Workflow

env = Environment(loader=PackageLoader('ggrc', 'templates'))

# TODO: move these views to ggrc_views and all the functions to notifications
# module.


def _get_unstarted_workflows():
  return db.session.query(Workflow).filter(
      Workflow.next_cycle_start_date < date.today(),
      Workflow.recurrences == True,  # noqa
      Workflow.status == 'Active',
  ).all()


def unstarted_cycles():
  workflows = _get_unstarted_workflows()
  return render_template("unstarted_cycles.haml", workflows=workflows)


def start_unstarted_cycles():
  workflows = _get_unstarted_workflows()
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
      app.logger.info(
          "Skipping workflow {0} (ID: {1}) because it doesn't "
          "have relative start and end days specified".format(
              workflow.title,
              workflow.id))
      continue

    workflow.next_cycle_start_date = date.today()
    workflow.non_adjusted_next_cycle_start_date = date.today()
    db.session.add(workflow)
  db.session.commit()
  run_job(start_recurring_cycles)
  return redirect(url_for('unstarted_cycles'))


def init_extra_views(app):
  app.add_url_rule(
      "/admin/unstarted_cycles",
      view_func=login_required(unstarted_cycles))

  app.add_url_rule(
      "/admin/start_unstarted_cycles",
      view_func=login_required(start_unstarted_cycles))
