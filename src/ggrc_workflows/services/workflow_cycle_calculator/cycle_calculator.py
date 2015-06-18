# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import datetime
import monthdelta
import operator
# from datetime import date, datetime, timedelta
from dateutil import relativedelta
from abc import ABCMeta, abstractmethod

@property
def NotImplementedProperty(self):
  raise NotImplementedError

@property
def NotImpementedMethod(self):
  raise NotImplementedError

class CycleCalculator(object):
  __metaclass__ = ABCMeta

  date_domain = NotImplementedProperty
  time_unit = NotImplementedProperty
  time_delta = NotImplementedProperty

  @abstractmethod
  def relative_day_to_date(self):
    raise NotImplementedError("Converting from relative to concrete date"
                              "must be done in concrete classes.")

  YEAR = datetime.date.today().year

  HOLIDAYS = [
    datetime.date(year=YEAR, month=1, day=1),   # Jan 01 New Year's Day
    datetime.date(year=YEAR, month=1, day=19),  # Jan 19 Martin Luther King Day
    datetime.date(year=YEAR, month=2, day=16),  # Feb 16 President's Day
    datetime.date(year=YEAR, month=5, day=25),  # May 25 Memorial Day
    datetime.date(year=YEAR, month=7, day=2),   # Jul 02 Independence Day Holiday
    datetime.date(year=YEAR, month=7, day=3),   # Jul 03 Independence Day Eve
    datetime.date(year=YEAR, month=9, day=7),   # Sep 07 Labor Day
    datetime.date(year=YEAR, month=11, day=26), # Nov 26 Thanksgiving Day
    datetime.date(year=YEAR, month=11, day=27), # Nov 27 Thanksgiving Day 2
    datetime.date(year=YEAR, month=12, day=23), # Dec 23 Christmas Holiday
    datetime.date(year=YEAR, month=12, day=24), # Dec 24 Christmas Eve
    datetime.date(year=YEAR, month=12, day=25), # Dec 25 Christmas Day
    datetime.date(year=YEAR, month=12, day=31), # Dec 31 New Year's Eve
  ]

  def __init__(self, workflow, holidays=HOLIDAYS):
    self.workflow = workflow
    self.holidays = holidays
    self.tasks = [
      task for task_group in self.workflow.task_groups
           for task in task_group.task_group_tasks]

  def is_work_day(self, ddate):
    return ddate.isoweekday() < 6 and ddate not in self.holidays

  def adjust_date(self, ddate):
    # Short path
    if self.is_work_day(ddate):
      return ddate

    # Adjusting for weekends
    weekday = ddate.isoweekday()
    if weekday > 5:
      ddate = ddate - datetime.timedelta(days=(weekday - 5))

    # Adjusting for holidays
    if ddate in self.holidays:
      ddate = ddate - datetime.timedelta(days=1)

    # In case we still don't have a workday, repeat
    if not self.is_work_day(ddate):
      return self.adjust_date(ddate)
    return ddate

  def task_date_range(self, task, base_date=None):
    if task.id in self.reified_tasks:
      return (
        self.reified_tasks[task.id]['start_date'],
        self.reified_tasks[task.id]['end_date']
      )

    if not base_date:
      base_date = datetime.date.today()
    start_day = self.relative_day_to_date(task.relative_start_day)
    end_day = self.relative_day_to_date(task.relative_end_day)

    # If the end day is actually in the next week, we add one week
    if end_day < start_day:
      end_day = end_day + self.time_delta

    # If both start day and end day have already happened we are operating on next week
    if start_day <= end_day < base_date:
      start_day = start_day + self.time_delta
      end_day = end_day + self.time_delta

    return self.adjust_date(start_day), self.adjust_date(end_day)

  def workflow_date_range(self):
    tasks_start_dates = [v['start_date'] for k, v in self.reified_tasks.items()]
    tasks_end_dates = [v['end_date'] for k, v in self.reified_tasks.items()]
    return min(tasks_start_dates), max(tasks_end_dates)

  def next_cycle_start_date(self, base_date=None):
    """Calculates next cycle start date

    Calculates next cycle's start date based on relative day. Usually this
    is first element of self.tasks in the next week but because that can
    get adjusted we need to calculate based on relative_start_day and taking
    into account that both start_date and end_date already happened, which
    means start_date is in the next week already and next_cycle_start_date
    must be two weeks from now.

    Args:
      base_date: The start date of the time unit we are operating on.
    Returns:
      A date when the next cycle is going to be generated.
    """
    today = datetime.date.today()
    if not base_date:
      base_date = today

    tasks_start_dates = \
      sorted([(v['start_date'], v['relative_start']) for k, v in self.reified_tasks.items()],
             key=lambda x: x[0])
    tasks_end_dates = \
      sorted([(v['end_date'], v['relative_end']) for k, v in self.reified_tasks.items()],
             key=lambda x: x[0], reverse=True)

    min_start = self.relative_day_to_date(tasks_start_dates[0][1])
    max_end = self.relative_day_to_date(tasks_end_dates[0][1])

    if max_end < min_start:
      max_end = max_end + self.time_delta

    if min_start <= max_end < today:
      base_date = base_date + self.time_delta

    return self.adjust_date(self.relative_day_to_date(
      self.tasks[0].relative_start_day,
      base_date=base_date + self.time_delta))