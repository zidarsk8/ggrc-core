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

class TestOneTimeWorkflow(BaseWorkflowTestCase):
  def test_basic_one_time_workflow(self):
    """Basic one time workflow test.


    """
    with freeze_time("2014-06-10 13:00:00"):
      _, wf = self.generator.generate_workflow(self.one_time_workflow_1)
      resp, tg = self.generator.generate_task_group(wf, data={
        'task_group_tasks': [
          {
            'title': 'task 1',
            'start_date': date(2015, 6, 18), # 6/18/2015 Thursday
            'end_date': date(2015, 7, 3) # 7/3/2015 Friday
          },
          {
            'title': 'task 2',
            'start_date': date(2015, 6, 20), # 6/20/2015 Thursday
            'end_date': date(2015, 8, 9) # 8/9/2015 # Sunday
          }]
      })
      _, cycle = self.generator.generate_cycle(wf)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")

      # one-time workflow shouldn't do date adjustment
      self.assertEqual(cycle.start_date, date(2015, 6, 18))
      self.assertEqual(cycle.end_date, date(2015, 8, 9))
