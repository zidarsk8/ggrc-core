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
from ggrc_workflows.models import Workflow, Cycle, TaskGroup
from ggrc_workflows import start_recurring_cycles
from ggrc_workflows.services.workflow_cycle_calculator import get_cycle_calculator
from tests.ggrc_workflows.generator import WorkflowsGenerator
from tests.ggrc.api_helper import Api
from tests.ggrc.generator import ObjectGenerator

from tests.ggrc_workflows.workflow_cycle_calculator.base_workflow_test_case import BaseWorkflowTestCase


if os.environ.get('TRAVIS', False):
  random.seed(1)  # so we can reproduce the tests if needed

class TestAnnuallyWorkflow(BaseWorkflowTestCase):
  def test_annually_workflow(self):
    """Basic annual workflow test.

    """
    annually_wf = {
      "title": "annually thingy",
      "description": "start this many a time",
      "frequency": "annually",
      "task_groups": [{
        "title": "task group",
        "task_group_tasks": [
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
          }],
        "task_group_objects": self.random_objects
      },
      ]
    }
    with freeze_time("2015-6-8 13:00:00"): # Mon, 6/8/2015
      _, wf = self.generator.generate_workflow(annually_wf)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 10))

    with freeze_time("2015-6-10 13:00:00"): # Mon, 6/8/2015
      start_recurring_cycles()

      cycle = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id).one()

      self.assertEqual(cycle.start_date, date(2015, 6, 10))
      # Because end date is on Sunday, relative start day will have to be adjusted
      self.assertEqual(cycle.end_date, date(2015, 8, 7))

      _, cycle = self.generator.generate_cycle(wf) #2016
      _, cycle = self.generator.generate_cycle(wf) #2017
      _, cycle = self.generator.generate_cycle(wf) #2018

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.next_cycle_start_date, date(2019, 6, 10))
      self.assertEqual(cycle.start_date, date(2018, 6, 8))
      self.assertEqual(cycle.end_date, date(2018, 8, 9))

  def test_type_casting(self):
    """Verify type casting for string input

    Test if string values get converted correctly to integers
    and arithmetic works"""

    annually_wf = {
      "title": "annually thingy",
      "description": "start this many a time",
      "frequency": "annually",
      "task_groups": [{
        "title": "task group",
        "task_group_tasks": [],
        "task_group_objects": self.random_objects
      },
      ]
    }

    task = {
      'title': 'annual task 1',
      "relative_start_day": "10", # 6/10/2015  Wed
      "relative_start_month": "6",
      "relative_end_day": "25", # 6/25/2015 Thu
      "relative_end_month": "6",
    }
    with freeze_time("2015-7-1 13:00"):
      _, wf = self.generator.generate_workflow(annually_wf)

      task_group = db.session.query(TaskGroup).filter(TaskGroup.workflow_id == wf.id).one()
      _, tgt = self.generator.generate_task_group_task(task_group, data=task)

      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")
      self.assertEqual(active_wf.next_cycle_start_date, date(2016, 6, 10))

    with freeze_time("2016-6-10 13:00"):
      start_recurring_cycles()

      cycle = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id).one()

      self.assertEqual(cycle.start_date, date(2016, 6, 10))
      self.assertEqual(cycle.end_date, date(2016, 6, 24)) # 6/25/2015 is Sat
      self.assertEqual(active_wf.next_cycle_start_date, date(2017, 6, 9)) # 6/10/2017 is Sat

  def test_task_order(self):
    annually_wf = {
      "title": "annually thingy",
      "description": "start this many a time",
      "frequency": "annually",
      "task_groups": [{
        "title": "task group",
        "task_group_tasks": [
          {
            'title': 'annual task 1',
            "relative_start_day": 21, # 6/21/2015
            "relative_start_month": 6,
            "relative_end_day": 25, # 6/25/2015 Thu
            "relative_end_month": 6,
          },
          {
            'title': 'annual task 2',
            "relative_start_day": 11, # 6/11/2015 Thu
            "relative_start_month": 6,
            "relative_end_day": 16, # 6/16/2015 Tue
            "relative_end_month": 6,
          },
          {
            'title': 'annual task 6',
            "relative_start_day": 2, # 7/2/2015 Thu
            "relative_start_month": 7,
            "relative_end_day": 15, # 7/15/2015 Wed
            "relative_end_month": 7,
          },
          {
            'title': 'annual task 3',
            "relative_start_day": 3, # 6/3/2015 Wed
            "relative_start_month": 6,
            "relative_end_day": 15, # 6/15/2015 Mon
            "relative_end_month": 6,
          },
          {
            'title': 'annual task 4',
            "relative_start_day": 8, # 6/8/2015 Mon
            "relative_start_month": 6,
            "relative_end_day": 15, # 6/15/2015 Mon
            "relative_end_month": 6,
          },
          {
            'title': 'annual task 5',
            "relative_start_day": 2, # 7/2/2015 Thu
            "relative_start_month": 6,
            "relative_end_day": 15, # 6/15/2015 Mon
            "relative_end_month": 6,
          }],
        "task_group_objects": self.random_objects
      },
      ]
    }
    with freeze_time("2015-06-01 13:00"):
      _, wf = self.generator.generate_workflow(annually_wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()

      calculator = get_cycle_calculator(active_wf)
      self.assertEqual([2, 3, 8, 11, 21, 2], [task.relative_start_day for task in calculator.tasks])
