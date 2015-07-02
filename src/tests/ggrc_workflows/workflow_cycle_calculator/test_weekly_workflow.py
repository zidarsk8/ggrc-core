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
from ggrc_workflows.services.workflow_cycle_calculator.weekly_cycle_calculator import WeeklyCycleCalculator

from tests.ggrc_workflows.generator import WorkflowsGenerator
from tests.ggrc.api_helper import Api
from tests.ggrc.generator import ObjectGenerator

from tests.ggrc_workflows.workflow_cycle_calculator.base_workflow_test_case import BaseWorkflowTestCase


if os.environ.get('TRAVIS', False):
  random.seed(1)  # so we can reproduce the tests if needed

class TestWeeklyWorkflow(BaseWorkflowTestCase):
  def test_relative_to_day(self):
    rtd = WeeklyCycleCalculator.relative_day_to_date

    # Test relative day to date conversion at the start of the week
    with freeze_time("2015-6-8 13:00:00"): # Monday, 6/8/2015
      self.assertEqual(rtd("1"), date(2015, 6, 8))
      self.assertEqual(rtd("2"), date(2015, 6, 9))
      self.assertEqual(rtd("3"), date(2015, 6, 10))
      self.assertEqual(rtd("4"), date(2015, 6, 11))
      self.assertEqual(rtd("5"), date(2015, 6, 12))
      with self.assertRaises(ValueError): rtd("6")
      with self.assertRaises(ValueError): rtd(7)

    # Test relative day to date conversion at the end of the week
    with freeze_time("2015-6-12 13:00:00"): # Friday, 6/12/2015
      self.assertEqual(rtd("1"), date(2015, 6, 8))
      self.assertEqual(rtd("2"), date(2015, 6, 9))
      self.assertEqual(rtd("3"), date(2015, 6, 10))
      self.assertEqual(rtd("4"), date(2015, 6, 11))
      self.assertEqual(rtd("5"), date(2015, 6, 12))

    # Test that we correctly adjust if we run on the weekend
    with freeze_time("2015-6-14 13:00:00"): # Sunday, 6/14/2015
      self.assertEqual(rtd("1"), date(2015, 6, 15))
      self.assertEqual(rtd("2"), date(2015, 6, 16))
      self.assertEqual(rtd("3"), date(2015, 6, 17))
      self.assertEqual(rtd("4"), date(2015, 6, 18))
      self.assertEqual(rtd("5"), date(2015, 6, 19))

  def test_future_cycle(self):
    """Future cycle workflow

    We create & activate our workflow on Monday and create a workflow
    with one task with start date on Tuesday (tomorrow) and ending on
    Thursday and second task starting on Wednesday and ending on Monday
    (next week).

    Cycle should be generated for the future.
    """
    weekly_wf = {
      "title": "weekly thingy",
      "description": "start this many a time",
      "frequency": "weekly",
      "task_groups": [{
        "title": "tg_2",
        "task_group_tasks": [
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
          }
        ],
        "task_group_objects": self.random_objects
      },
      ]
    }

    with freeze_time("2015-6-8 13:00:00"): # Monday, 6/8/2015
      _, wf = self.generator.generate_workflow(weekly_wf)
      _, tg = self.generator.generate_task_group(wf)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 9))

      cycles = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id,
        Cycle.start_date > date(2015, 6, 7))

      self.assertEqual(cycles.count(), 0)

    with freeze_time("2015-6-9 13:00:00"):
      start_recurring_cycles()

      cycle = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id,
        Cycle.start_date == date(2015, 6, 9)).one()

      self.assertEqual(cycle.start_date, date(2015, 6, 9))
      self.assertEqual(cycle.end_date, date(2015, 6, 15))
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 16))

    with freeze_time("2015-6-16 13:00:00"):
      start_recurring_cycles()

      cycle = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id,
        Cycle.start_date == date(2015, 6, 16)).one()

      self.assertEqual(cycle.start_date, date(2015, 6, 16))
      self.assertEqual(cycle.end_date, date(2015, 6, 22))
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 23))

  def test_mid_cycle(self):
    """Mid-cycle workflow

    We create & activate our workflow on Wednesday and create a workflow
    with one task with start date on Tuesday (yesterday) and ending on
    Thursday and second task starting on Wednesday and ending on Monday
    (next week).

    Because it's Wednesday, workflow should be activated immediately.
    """
    weekly_wf = {
      "title": "weekly thingy",
      "description": "start this many a time",
      "frequency": "weekly",
      "task_groups": [{
        "title": "tg_2",
        "task_group_tasks": [
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
            }
        ],
        "task_group_objects": self.random_objects
      },
      ]
    }

    with freeze_time("2015-6-10 13:00:00"): # Wednesday, 6/10/2015
      _, wf = self.generator.generate_workflow(weekly_wf)
      _, tg = self.generator.generate_task_group(wf)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")
      # Originally this would be 2015-6-10 but because update_workflow_state
      # fixes workflow next_cycle_start_date it's actually 16
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 16))

      cycle = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id).one()

      # Start date should be Tuesday 9th (yesterday), end date should be Monday 15h
      self.assertEqual(cycle.start_date, date(2015, 6, 9))
      self.assertEqual(cycle.end_date, date(2015, 6, 15))

    with freeze_time("2015-6-16 13:00:00"): # Wednesday, 6/10/2015
      start_recurring_cycles()
      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 23))

      cycle = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id,
        Cycle.start_date > date(2015, 6, 15)).one()

      self.assertEqual(cycle.start_date, date(2015, 6, 16))
      self.assertEqual(cycle.end_date, date(2015, 6, 22))

  def test_past_cycle(self):
    """Past workflow

    We create & activate our workflow on Friday and create a workflow
    with one task with start date on Monday and ending on
    Wednesday and second task starting on Tuesday and ending on Thursday.

    Because it's Friday, created cycles should be in the next week.
    """
    weekly_wf = {
      "title": "weekly thingy",
      "description": "start this many a time",
      "frequency": "weekly",
      "task_groups": [{
        "title": "tg_2",
        "task_group_tasks": [
          {
            'title': 'weekly task 1',
            "relative_start_day": 1, # Monday, 8th
            "relative_start_month": None,
            "relative_end_day": 3, # Wednesday, 10th
            "relative_end_month": None,
          },
          {
            'title': 'weekly task 2',
            "relative_start_day": 2, # Tuesday, 9th
            "relative_start_month": None,
            "relative_end_day": 4, # 11th, Thursday
            "relative_end_month": None,
            }
        ],
        "task_group_objects": self.random_objects
      },
      ]
    }

    with freeze_time("2015-6-12 13:00:00"): # Friday, 6/12/2015
      _, wf = self.generator.generate_workflow(weekly_wf)
      _, tg = self.generator.generate_task_group(wf)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 15))

    with freeze_time("2015-6-15 13:00:00"):
      start_recurring_cycles()
      cycle = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id,
        Cycle.start_date == date(2015, 6, 15)).one()

      self.assertEqual(cycle.start_date, date(2015, 6, 15))
      self.assertEqual(cycle.end_date, date(2015, 6, 18))

      # Next cycle should start next Tuesday
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 22))

    with freeze_time("2015-6-22 14:00"):
      start_recurring_cycles()
      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 29))

      cycle = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id,
        Cycle.start_date == date(2015, 6, 22)).one()

      self.assertEqual(cycle.start_date, date(2015, 6, 22))
      self.assertEqual(cycle.end_date, date(2015, 6, 25))

  def test_type_casting(self):
    """Verify type casting for string input

    Test if string values get converted correctly to integers
    and arithmetic works"""

    weekly_wf = {
      "title": "weekly thingy",
      "description": "start this many a time",
      "frequency": "weekly",
      "task_groups": [{
        "title": "task group 1",
        "task_group_tasks": [],
        "task_group_objects": self.random_objects
      },
      ]
    }

    task = {
      'title': 'weekly task 1',
      "relative_start_day": "3", # Wed
      "relative_start_month": None,
      "relative_end_day": "5", # Fri
      "relative_end_month": None,
    }


    with freeze_time("2015-7-1 13:00"): # Wed
      _, wf = self.generator.generate_workflow(weekly_wf)

      task_group = db.session.query(TaskGroup).filter(TaskGroup.workflow_id == wf.id).one()
      _, tgt = self.generator.generate_task_group_task(task_group, data=task)

      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")

      cycle = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id).one()

      self.assertEqual(cycle.start_date, date(2015, 7, 1))
      self.assertEqual(cycle.end_date, date(2015, 7, 2))
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 7, 8))
