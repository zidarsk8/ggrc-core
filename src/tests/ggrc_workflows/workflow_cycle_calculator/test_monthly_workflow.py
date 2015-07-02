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
from ggrc_workflows.models import Workflow, Cycle, TaskGroupTask, TaskGroup
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

  def test_change_task_dates(self):
    """Test if changing the task dates adjusts the next cycle start date
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
             "relative_start_day": 15, # 7/15/2015 Wed
             "relative_start_month": None,
             "relative_end_day": 20, # 7/20/2015 Mon
             "relative_end_month": None,
           }],
         "task_group_objects": self.random_objects
         },
      ]
    }
    with freeze_time("2015-7-1 14:00:00"): # 7/1/2015 Wed
      _, wf = self.generator.generate_workflow(monthly_workflow)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 7, 15))

      task_group = db.session.query(TaskGroup).filter(TaskGroup.workflow_id == wf.id).one()
      task = db.session.query(TaskGroupTask).filter(TaskGroupTask.task_group_id == task_group.id).one()

      self.generator.modify_object(task, {
        "relative_start_day": 10, # 7/10/2015 Fri
        "relative_end_day": 12 # 7/12/2015 Sun
      })

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 7, 10))

  def test_update_next_cycle_start_date_delete_task(self):
    """Test if deleting a task changes the next cycle start date"""

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
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")

      # Should be 14th, but that is Sunday, so it must be Friday
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 12))

      task_group = db.session.query(TaskGroup).filter(TaskGroup.workflow_id == wf.id).one()
      task = db.session.query(TaskGroupTask).filter(
        TaskGroupTask.task_group_id == task_group.id,
        TaskGroupTask.relative_start_day == 14
      ).one()

      response = self.generator.api.delete(task, task.id)
      self.assert200(response)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 15))

  def test_update_next_cycle_start_date_delete_task_group(self):
    """Test if deleting a task group changes next cycle start date"""
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
           }],
         "task_group_objects": self.random_objects
         },
        {"title": "task group 2",
         'task_group_tasks': [
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
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")

      # Should be 14th, but that is Sunday, so it must be Friday
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 12))

      task_group = db.session.query(TaskGroup).filter(
        TaskGroup.workflow_id == wf.id,
        TaskGroup.title == u"task group 2"
      ).one()

      response = self.generator.api.delete(task_group, task_group.id)
      self.assert200(response)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 15))


  def test_update_next_cycle_start_date_new_task_group(self):
    """Check if adding a new task group changes the next cycle start date"""
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
           }],
         "task_group_objects": self.random_objects
         },
      ]
    }
    with freeze_time("2015-6-9 13:00:00"): # Tuesday, 6/9/2015
      _, wf = self.generator.generate_workflow(monthly_workflow)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")

      # Should be 14th, but that is Sunday, so it must be Friday
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 15))

      _, tg = self.generator.generate_task_group(wf, data=
        {"title": "task group 2",
         'task_group_tasks': [
           {
             'title': 'monthly task 2',
             "relative_start_day": 14, # 6/14/2015 Sun
             "relative_start_month": None,
             "relative_end_day": 3, # 7/3/2015 Fri
             "relative_end_month": None,
           }],
         "task_group_objects": self.random_objects
         })

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 12))

  def test_delete_all_tasks(self):
    """Check that workflow doesn't have next cycle start date when all tasks are deleted"""
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
           }],
         "task_group_objects": self.random_objects
         },
      ]
    }
    with freeze_time("2015-6-9 13:00:00"): # Tuesday, 6/9/2015
      _, wf = self.generator.generate_workflow(monthly_workflow)
      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 6, 15))

      task_group = db.session.query(TaskGroup).filter(TaskGroup.workflow_id == wf.id).one()

      response = self.generator.api.delete(task_group, task_group.id)
      self.assert200(response)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")
      self.assertEqual(active_wf.next_cycle_start_date, None)

  def test_type_casting(self):
    """Verify type casting for string input

    Test if string values get converted correctly to integers
    and arithmetic works"""

    monthly_workflow = {
      "title": "monthly test wf",
      "description": "start this many a time",
      "frequency": "monthly",
      "task_groups": [
        {"title": "task group 1",
         'task_group_tasks': [],
         "task_group_objects": self.random_objects
         },
      ]
    }

    task = {
      'title': 'monthly task 1',
      "relative_start_day": "15", # 7/15/2015 Wed
      "relative_start_month": None,
      "relative_end_day": "19", # 7/19/2015 Sun
      "relative_end_month": None,
    }

    with freeze_time("2015-7-1 13:00"): # Wed
      _, wf = self.generator.generate_workflow(monthly_workflow)

      task_group = db.session.query(TaskGroup).filter(TaskGroup.workflow_id == wf.id).one()
      _, tgt = self.generator.generate_task_group_task(task_group, data=task)

      _, awf = self.generator.activate_workflow(wf)

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()
      self.assertEqual(active_wf.status, "Active")


    with freeze_time("2015-7-15 13:00"): # Wed
      start_recurring_cycles()

      active_wf = db.session.query(Workflow).filter(Workflow.id == wf.id).one()

      cycle = db.session.query(Cycle).filter(
        Cycle.workflow_id == wf.id).one()

      self.assertEqual(cycle.start_date, date(2015, 7, 15))
      self.assertEqual(cycle.end_date, date(2015, 7, 17)) # 19 is Sun
      self.assertEqual(active_wf.next_cycle_start_date, date(2015, 8, 14)) # 15 is Sat
