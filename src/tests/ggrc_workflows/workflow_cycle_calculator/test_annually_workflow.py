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

class TestAnnualWorkflow(BaseWorkflowTestCase):
  def test_annual_workflow(self):
    """Basic annual workflow test.

    """
    with freeze_time("2015-6-8 13:00:00"): # Mon, 6/8/2015
      _, wf = self.generator.generate_workflow(self.monthly_workflow_1)
      resp, tg = self.generator.generate_task_group(wf, data={
        'task_group_tasks': [
          {
            'title': 'annual task 1',
            "relative_start_day": 10, # 6/10/2015  Wed
            "relative_start_month": 6,
            "relative_end_day": 25, # 6/25/2015 Thu
            "relative_end_month": 6,
          },
          {
            'title': 'annual task 2',
            "relative_start_day": 15, # 6/15/2015 Mon
            "relative_start_month": 6,
            "relative_end_day": 9, # 8/9/2015 Sun
            "relative_end_month": 8,
          }]
      })
      _, cycle = self.generator.generate_cycle(wf)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()

      self.assertEqual(active_wf.status, "Active")

      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 7, 10))
      self.assertEqual(cycle.start_date, date(2015, 6, 10))

      # Because end date is on Sunday, relative start day will have to be adjusted
      self.assertEqual(cycle.end_date, date(2015, 8, 7))
