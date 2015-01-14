# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: brad@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

# from ggrc import db
from datetime import date, timedelta
from tests.ggrc import TestCase
from ggrc_workflows.services.workflow_date_calculator import WorkflowDateCalculator
from ggrc_workflows.models import *
from ggrc.models import *

class TestWorkflowDateCalculator(TestCase):
  SQLALCHEMY_DATABASE_URI = "sqlite://"

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def _workflow_factory(self):
    workflow = Workflow()
    workflow.id = 1
    return workflow

  def _create_one_time_workflow(self):
    # Create one-time workflow
    workflow = self._workflow_factory()
    workflow.id = 1
    workflow.frequency = "one_time"
    workflow.title = "One Time Workflow"
    return workflow

  def _create_weekly_workflow(self):
    # Create one-time workflow
    workflow = self._workflow_factory()
    workflow.frequency = "weekly"
    workflow.title = "Weekly Workflow"
    return workflow

  def _create_monthly_workflow(self):
    # Create one-time workflow
    workflow = self._workflow_factory()
    workflow.frequency = "monthly"
    workflow.title = "Monthly Workflow"
    return workflow

  def _create_quarterly_workflow(self):
    # Create one-time workflow
    workflow = self._workflow_factory()
    workflow.frequency = "quarterly"
    workflow.title = "Quarterly Workflow"
    return workflow

  def _create_annual_workflow(self):
    # Create one-time workflow
    workflow = self._workflow_factory()
    workflow.frequency = "annually"
    workflow.title = "Annual Workflow"
    return workflow

  def _set_date_range_for_workflow(self, workflow, relative_start_month, relative_start_day,
                                   relative_end_month, relative_end_day):
    task_group = TaskGroup()
    task_group.id = 1
    task_group.workflow_id = workflow.id
    task_group.title = workflow.title
    workflow.task_groups.append(task_group)

    task_group_task = TaskGroupTask()
    task_group_task.id = 1
    task_group_task.task_group_id = task_group.id
    task_group_task.title = "Task: "+workflow.title
    task_group_task.relative_start_month=relative_start_month
    task_group_task.relative_start_day=relative_start_day
    task_group_task.relative_end_month=relative_end_month
    task_group_task.relative_end_day=relative_end_day
    task_group.task_group_tasks.append(task_group_task)

    # Use DataAsset because it just has a title. Easy to work with.
    data_asset = DataAsset()
    data_asset.id = 1
    data_asset.title = "Data Asset: "+workflow.title

    task_group_object = TaskGroupObject()
    task_group_object.id = 1
    task_group_object.task_group_id=task_group.id
    task_group_object.object_id = data_asset.id
    task_group_object.object_type = data_asset.type
    task_group.task_group_objects.append(task_group_object)

    return workflow

  def cycle_for_workflow(self, workflow):
    cycle = Cycle()
    cycle.workflow = workflow
    cycle.title = workflow.title
    cycle.description = workflow.description
    return cycle

  def today(self):
    return date.today()

  def tomorrow(self):
    return self.today() + timedelta(days=1)

  def day_after_tomorrow(self):
    return self.today() + timedelta(days=2)

  def yesterday(self):
    return self.today() + timedelta(days=-1)

  def day_before_yesterday(self):
    return self.today() + timedelta(days=-2)

  def seven_days_ago(self):
    return self.today()+ timedelta(days=-7)

  def seven_days_from_now(self):
    return self.today() + timedelta(days=7)

  def thirty_days_ago(self):
    return self.today() + timedelta(days=-30)

  def thirty_days_from_now(self):
    return self.today() + timedelta(days=30)

  def one_year_ago(self):
    return self.today() + timedelta(weeks=-52)

  def one_year_from_now(self):
    return self.today() + timedelta(weeks=52)

  def day_this_week(self, weekday_number):
    day = self.today()
    while day.weekday() < weekday_number:
      day = day + timedelta(days=1)
    while day.weekday() > weekday_number:
      day = day + timedelta(days=-1)
    return day

  def day_this_month(self, day_number):
    day = self.today()
    while day.day < day_number:
      day = day + timedelta(days=1)
    while day.day > day_number:
      day = day + timedelta(days=-1)
    return day

  def test_start_date_sets_properly(self):
    workflow = self._create_one_time_workflow()
    workflow = \
      self._set_date_range_for_workflow(
        workflow,
        self.today().month,
        self.today().day,
        self.tomorrow().month,
        self.tomorrow().day
      )

    self.assertEqual(1, len(workflow.task_groups))

    calc = WorkflowDateCalculator(workflow)

    start_day = calc._calc_min_relative_start_day_from_tasks()
    start_month = calc._calc_min_relative_start_month_from_tasks()
    end_day = calc._calc_max_relative_end_day_from_tasks()
    end_month = calc._calc_max_relative_end_month_from_tasks()

    self.assertEqual(start_day, self.today().day)
    self.assertEqual(start_month, self.today().month)
    self.assertEqual(end_day, self.tomorrow().day)
    self.assertEqual(end_month, self.tomorrow().month)

  def test_calc_start_date_one_time_workflow(self):
    workflow = self._create_one_time_workflow()
    workflow = \
      self._set_date_range_for_workflow(
        workflow,
        self.today().month,
        self.today().day,
        self.tomorrow().month,
        self.tomorrow().day
      )

    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(self.yesterday())
    self.assertEqual(start_date, self.yesterday())

  def test_calc_end_date_weekly_workflow_start_before_end(self):
    workflow = self._create_weekly_workflow()
    workflow = \
      self._set_date_range_for_workflow(
        workflow,
        self.yesterday().month, # irrelevant for weekly wf
        self.yesterday().weekday(),
        self.day_after_tomorrow().month, # irrelevant for weekly wf
        self.day_after_tomorrow().weekday()
      )

    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(self.day_before_yesterday())
    self.assertEqual(start_date, self.yesterday())

  def test_weekly_workflow_basedate_after_start_date(self):
    workflow = self._create_weekly_workflow()
    day_start, day_end = 1, 4
    workflow = \
      self._set_date_range_for_workflow(
        workflow, self.yesterday().month, day_start, self.day_after_tomorrow().month, day_end
      )

    day_2 = self.day_this_week(2)

    # start_date is a Tuesday
    # day_2 is a Wednesday
    # end_date is a Friday

    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(day_2)
    end_date = calc.calc_nearest_end_date_after_start_date(start_date)
    self.assertEqual(start_date, day_2 + timedelta(days=6))
    self.assertEqual(end_date, start_date + timedelta(days=3))

  def test_weekly_workflow_basedate_before_start_date(self):
    workflow = self._create_weekly_workflow()
    day_start, day_end = 2, 4
    workflow = \
      self._set_date_range_for_workflow(
        workflow, self.yesterday().month, day_start, self.day_after_tomorrow().month, day_end
      )

    day_1 = self.day_this_week(1)

    # day_1 is a Tuesday
    # start_date is a Wednesday
    # end_date is a Friday

    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(day_1)
    end_date = calc.calc_nearest_end_date_after_start_date(start_date)
    self.assertEqual(start_date, day_1 + timedelta(days=1))
    self.assertEqual(end_date, start_date + timedelta(days=2))

  def test_weekly_workflow_end_day_before_start_day_basedate_before_start_day(self):
    workflow = self._create_weekly_workflow()
    day_start, day_end = 3, 1
    workflow = \
      self._set_date_range_for_workflow(
        workflow, self.yesterday().month, day_start, self.day_after_tomorrow().month, day_end
      )

    day_1 = self.day_this_week(1)

    # day_1 is a Tuesday
    # start_date is a Thursday
    # end_date is a Tuesday

    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(day_1)
    end_date = calc.calc_nearest_end_date_after_start_date(start_date)
    self.assertEqual(start_date, day_1 + timedelta(days=2))
    self.assertEqual(end_date, start_date + timedelta(days=5))

  def test_weekly_workflow_end_day_equals_start_day_basedate_before_start_day(self):
    workflow = self._create_weekly_workflow()
    day_start, day_end = 2, 2
    workflow = \
      self._set_date_range_for_workflow(
        workflow, self.yesterday().month, day_start, self.day_after_tomorrow().month, day_end
      )

    day_1 = self.day_this_week(1)
    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(day_1)
    end_date = calc.calc_nearest_end_date_after_start_date(start_date)
    self.assertEqual(start_date, day_1 + timedelta(days=1))
    self.assertEqual(end_date, start_date)

  def test_weekly_workflow_end_day_equals_start_day_basedate_equals_start_day(self):
    workflow = self._create_weekly_workflow()
    day_start, day_end = 1, 1
    workflow = \
      self._set_date_range_for_workflow(
        workflow, self.yesterday().month, day_start, self.day_after_tomorrow().month, day_end
      )

    day_1 = self.day_this_week(1)
    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(day_1)
    end_date = calc.calc_nearest_end_date_after_start_date(start_date)
    self.assertEqual(start_date, day_1)
    self.assertEqual(end_date, start_date)

  # Monthly workflow tests

  def test_monthly_workflow_calc_start_and_end_date_after_basedate(self):
    workflow = self._create_monthly_workflow()
    workflow = self._set_date_range_for_workflow(workflow, None, 5, None, 10)
    day_4 = self.day_this_month(4)
    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(day_4)
    end_date = calc.calc_nearest_end_date_after_start_date(start_date)
    self.assertEqual(start_date, day_4 + timedelta(days=1))
    self.assertEqual(end_date, start_date + timedelta(days=5))

  def test_monthly_workflow_calc_start_date_on_basedate(self):
    workflow = self._create_monthly_workflow()
    workflow = self._set_date_range_for_workflow(workflow, None, 5, None, 10)
    day_5 = self.day_this_month(5)
    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(day_5)
    end_date = calc.calc_nearest_end_date_after_start_date(start_date)
    self.assertEqual(start_date, day_5)
    self.assertEqual(end_date, start_date + timedelta(days=5))

  def test_monthly_workflow_start_date_before_end_date_and_start_date_before_basedate(self):
    from monthdelta import *
    workflow = self._create_monthly_workflow()
    workflow = self._set_date_range_for_workflow(workflow, None, 5, None, 10)
    day_15_this_month = self.day_this_month(15)
    day_5_this_month = self.day_this_month(5)
    day_5_next_month = day_5_this_month + monthdelta(1)

    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(day_15_this_month)
    end_date = calc.calc_nearest_end_date_after_start_date(start_date)
    self.assertEqual(start_date, day_5_next_month)
    self.assertEqual(end_date, start_date + timedelta(days=5))

  def test_monthly_workflow_start_date_before_end_date_and_start_date_after_basedate(self):
    workflow = self._create_monthly_workflow()
    workflow = self._set_date_range_for_workflow(workflow, None, 10, None, 15)
    day_5_this_month = self.day_this_month(5)
    day_10_this_month = self.day_this_month(10)
    day_15_this_month = self.day_this_month(15)

    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(day_5_this_month)
    end_date = calc.calc_nearest_end_date_after_start_date(start_date)
    self.assertEqual(start_date, day_10_this_month)
    self.assertEqual(end_date, day_15_this_month)

  def test_monthly_workflow_start_date_before_end_date_and_start_date_equals_basedate(self):
    workflow = self._create_monthly_workflow()
    workflow = self._set_date_range_for_workflow(workflow, None, 10, None, 15)
    day_10_this_month = self.day_this_month(10)
    day_15_this_month = self.day_this_month(15)

    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(day_10_this_month)
    end_date = calc.calc_nearest_end_date_after_start_date(start_date)
    self.assertEqual(start_date, day_10_this_month)
    self.assertEqual(end_date, day_15_this_month)

  def test_monthly_workflow_start_date_after_end_date_and_start_date_after_basedate(self):
    from monthdelta import *
    workflow = self._create_monthly_workflow()
    workflow = self._set_date_range_for_workflow(workflow, None, 15, None, 10)
    day_10_this_month = self.day_this_month(10)
    day_10_next_month = day_10_this_month + monthdelta(1)
    day_15_this_month = self.day_this_month(15)
    calc = WorkflowDateCalculator(workflow)
    start_date = calc.calc_nearest_start_date_after_basedate(day_10_this_month)
    end_date = calc.calc_nearest_end_date_after_start_date(start_date)
    self.assertEqual(start_date, day_15_this_month)
    self.assertEqual(end_date, day_10_next_month)

  def test_calc_end_date_quarterly_workflow(self):
    pass

  def test_calc_end_date_annually_workflow(self):
    pass

  def test_calc_next_cycle_start_date_weekly(self):
    pass

  def test_calc_next_cycle_start_date_monthly(self):
    pass

  def test_calc_next_cycle_start_date_quarterly(self):
    pass

  def test_calc_next_cycle_start_date_annually(self):
    pass

  def test_calc_previous_cycle_start_date_weekly(self):
    pass

  def test_calc_previous_cycle_start_date_monthly(self):
    pass

  def test_calc_previous_cycle_start_date_quarterly(self):
    pass

  def test_calc_previous_cycle_start_date_annually(self):
    pass
