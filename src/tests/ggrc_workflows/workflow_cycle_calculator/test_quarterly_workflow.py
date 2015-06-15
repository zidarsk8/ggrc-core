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

class TestQuarterlyWorkflow(BaseWorkflowTestCase):
  def test_quarterly_workflow(self):
    """Basic quarterly workflow test.

    Quarters:
      - Jan/Apr/Jul/Oct (1st)
      - Feb/May/Aug/Nov (2d)
      - Mar/Jun/Sep/Dec (3rd)

    Syntax: 5/#2 - Every 5th of 2nd quarter month => 5th Feb, 5th May, 5th Aug, 5th Nov

    We create a quarterly workflow whose cycle should start on 3rd of Jan/and end on
    3rd of next month.

    Workflow task 1:  Jan/Apr/July/Oct 10   to Feb/May/August/November 15
    Workflow task 2:  Feb/May/August/November 7 to Jan/Apr/July/Oct 14

    """
    with freeze_time("2015-6-8 13:00:00"): # Mon, 6/8/2015
      _, wf = self.generator.generate_workflow(self.monthly_workflow_1)
      resp, tg = self.generator.generate_task_group(wf, data={
        'task_group_tasks': [
          {
            'title': 'quarterly task 1',
            "relative_start_day": 10, # 7/10/2015  Fri
            "relative_start_month": 1,
            "relative_end_day": 15, # 8/15/2015 Sat
            "relative_end_month": 2,
          },
          {
            'title': 'quarterly task 2',
            "relative_start_day": 7, # 6/12/2015 Fri
            "relative_start_month": 2,
            "relative_end_day": 1, # 7/3/2015 Fri
            "relative_end_month": 14,
          }]
      })
      _, cycle = self.generator.generate_cycle(wf)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()

      self.assertEqual(active_wf.status, "Active")

      # q3 cycle starts on july 10th, we are mid cycle
      # q2 cycle lasts from Apr 10th to July 14th
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 7, 10))
      self.assertEqual(cycle.start_date, date(2015, 4, 10))
      self.assertEqual(cycle.end_date, date(2015, 7, 14))
