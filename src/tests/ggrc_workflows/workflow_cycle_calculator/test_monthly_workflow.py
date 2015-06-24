# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import random
from tests.ggrc import TestCase
from freezegun import freeze_time
from datetime import date, datetime

import os
from ggrc import db
from ggrc_workflows.models import Workflow, Cycle
from ggrc_workflows import start_recurring_cycles
from tests.ggrc_workflows.generator import WorkflowsGenerator
from tests.ggrc.api_helper import Api
from tests.ggrc.generator import ObjectGenerator

from tests.ggrc_workflows.workflow_cycle_calculator.base_workflow_test_case import BaseWorkflowTestCase


if os.environ.get('TRAVIS', False):
  random.seed(1)  # so we can reproduce the tests if needed

class TestMonthlyWorkflow(BaseWorkflowTestCase):
  def test_monthly_workflow(self):
    """Basic monthly workflow test.

    We create a monthly workflow whose cycle should start on 12th and end on
    3rd of next month.
    """
    monthly_workflow = {
      "title": "monthly test wf",
      "description": "start this many a time",
      "frequency": "monthly",
      "task_groups": [
        {"title": "task group 1",
         'task_group_tasks': [
           {
             'title': 'monthly task 1',
             "relative_start_day": 15, # 6/15/2015 Mon
             "relative_start_month": None,
             "relative_end_day": 19, # 6/19/2015 Fri
             "relative_end_month": None,
           },
           {
             'title': 'monthly task 2',
             "relative_start_day": 14, # 6/14/2015 Sun
             "relative_start_month": None,
             "relative_end_day": 3, # 7/3/2015 Fri
             "relative_end_month": None,
           }],
         "task_group_objects": self.random_objects
         },
      ]
    }

    with freeze_time("2015-6-9 13:00:00"): # Tuesday, 6/9/2015
      _, wf = self.generator.generate_workflow(monthly_workflow)
      _, tg = self.generator.generate_task_group(wf)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")

      # Should be 12th, but that is Sunday, so it must be Friday
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 12))

      _, cycle = self.generator.generate_cycle(wf)
      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()

      self.assertEqual(cycle.start_date, date(2015, 6, 12))

      # Should be 3rd but 3rd is Independence Day (Observed)
      self.assertEqual(cycle.end_date, date(2015, 7, 2))
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 7, 14))

    with freeze_time("2015-7-14 13:00:00"): # Tuesday, 7/14/2015
      start_recurring_cycles()

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      cycle = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id,
        Cycle.start_date == date(2015, 7, 14)).one()

      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 8, 14)) # 8/14/2015 Friday
      self.assertEqual(cycle.start_date, date(2015, 7, 14)) # 7/10/2015 Fri
      self.assertEqual(cycle.end_date, date(2015, 8, 3)) # 8/3/2015 Mon
