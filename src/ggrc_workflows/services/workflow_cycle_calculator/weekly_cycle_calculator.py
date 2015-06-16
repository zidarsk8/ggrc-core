# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import datetime
import monthdelta
from dateutil import relativedelta

from cycle_calculator import CycleCalculator

class WeeklyCycleCalculator(CycleCalculator):
  time_delta = datetime.timedelta(weeks=1)
  date_domain = set({1,2,3,4,5})

  def relative_day_to_date(self, relative_day):
    today = datetime.date.today()
    # TODO: How to handle if people do stuff on weekend? Move to next week?
    # if today.isoweekday() not in self.date_domain:
    #   today = today + dateutil.relativedelta.relativedelta(
    #     days=)
    return today + relativedelta.relativedelta(
      days=relative_day - today.isoweekday())

  def task_date_range(self, task, base_date=None):
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

    return {
      'start_date': start_day,
      'end_date': end_day
    }

  def workflow_date_range(self):
    # TODO: cache this when object is initialised?
    tasks_start_dates = []
    tasks_end_dates = []

    for task_group in self.workflow.task_groups:
      for task in task_group.task_group_tasks:
        date_range = self.task_date_range(task)
        start_date, end_date = date_range['start_date'], date_range['end_date']
        tasks_start_dates += [start_date]
        tasks_end_dates += [end_date]

    return {
      'start_date': min(tasks_start_dates),
      'end_date': max(tasks_end_dates)
    }

  def next_cycle_start_date(self):
    return self.workflow_date_range()['start_date'] + self.time_delta
