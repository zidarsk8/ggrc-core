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
from tests.ggrc_workflows.generator import WorkflowsGenerator
from tests.ggrc.api_helper import Api
from tests.ggrc.generator import ObjectGenerator

from tests.ggrc_workflows.workflow_date_calculator.BaseWorkflowTestCase import BaseWorkflowTestCase


if os.environ.get('TRAVIS', False):
  random.seed(1)  # so we can reproduce the tests if needed

class TestWeeklyWorkflow(BaseWorkflowTestCase):
  def test_weekly_workflow(self):
    """Basic weekly workflow test.

    We begin the test on Wednesday and create a workflow with one task with
    start date on Tuesday (yesterday) and ending on Thursday and second task starting on
    Wednesday and ending on Monday (next week).

    Because it's Wednesday, workflow should be activated immediately.
    """
    with freeze_time("2015-6-10 13:00:00"): # Wednesday, 6/10/2015
      _, wf = self.generator.generate_workflow(self.weekly_wf_1)
      resp, tg = self.generator.generate_task_group(wf, data={
        'task_group_tasks': [
          {
            'title': 'weekly task 1',
            "relative_start_day": 2, # Tuesday, 9th
            "relative_start_month": None,
            "relative_end_day": 4, # Thursday, 11th
            "relative_end_month": None,
          },
          {
            'title': 'weekly task 2',
            "relative_start_day": 3, # Wednesday, 10th
            "relative_start_month": None,
            "relative_end_day": 1, # 15th, Monday
            "relative_end_month": None,
            }]
      })
      _, cycle = self.generator.generate_cycle(wf)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")

      # Start date should be Tuesday 9th (yesterday), end date should be Monday 15h
      self.assertEqual(cycle.start_date, date(2015, 6, 9))
      self.assertEqual(cycle.end_date, date(2015, 6, 15))

      # Next cycle should start next Tuesday
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 16))

