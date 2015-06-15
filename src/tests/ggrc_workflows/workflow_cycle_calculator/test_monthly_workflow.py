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

from tests.ggrc_workflows.workflow_date_calculator.BaseWorkflowTestCase import BaseWorkflowTestCase


if os.environ.get('TRAVIS', False):
  random.seed(1)  # so we can reproduce the tests if needed

class TestMonthlyWorkflow(BaseWorkflowTestCase):
  def test_monthly_workflow(self):
    """Basic monthly workflow test.

    We create a monthly workflow whose cycle should start on 12th and end on
    3rd of next month.
    """
    with freeze_time("2015-6-9 13:00:00"): # Tuesday, 6/9/2015
      _, wf = self.generator.generate_workflow(self.monthly_workflow_1)
      resp, tg = self.generator.generate_task_group(wf, data={
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
            "relative_start_day": 12, # 6/12/2015 Fri
            "relative_start_month": None,
            "relative_end_day": 3, # 7/3/2015 Fri
            "relative_end_month": None,
            }]
      })
      _, cycle = self.generator.generate_cycle(wf)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()

      self.assertEqual(active_wf.status, "Active")

      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 7, 10)) # Should be 12th, but that is sunday, so it must be Friday
      self.assertEqual(cycle.start_date, date(2015, 6, 12))
      self.assertEqual(cycle.end_date, date(2015, 7, 3))

    with freeze_time("2015-7-10 13:00:00"): # Friday, 7/10/2015
      start_recurring_cycles()

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()

      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 8, 12)) # 8/12/2015 Wed
      self.assertEqual(cycle.start_date, date(2015, 7, 10)) # 7/10/2015 Fri
      self.assertEqual(cycle.end_date, date(2015, 8, 3)) # 8/3/2015 Mon
