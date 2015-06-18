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

  def __init__(self, workflow, base_date=None):
    if not base_date:
      base_date = datetime.date.today()

    super(WeeklyCycleCalculator, self).__init__(workflow)
    self.tasks = sorted(self.tasks, key=lambda t: t.relative_start_day)

    self.reified_tasks = {}
    for task in self.tasks:
      start_date, end_date = self.task_date_range(task, base_date)
      self.reified_tasks[task.id] = {
        'start_date': start_date,
        'end_date': end_date,
        'relative_start': task.relative_start_day,
        'relative_end': task.relative_end_day
      }

  @staticmethod
  def relative_day_to_date(relative_day, base_date=None):
    today = datetime.date.today()
    relative_day = int(relative_day)
    if relative_day not in WeeklyCycleCalculator.date_domain:
      raise ValueError(
        "Weekly recurring cycles can only have relative day in 1-5 "
        "(Monday-Friday) range")

    if not base_date:
      base_date = today

    if base_date == today and base_date.isoweekday() >= 6:
      base_date = base_date + WeeklyCycleCalculator.time_delta

    return base_date + relativedelta.relativedelta(
      days=relative_day - base_date.isoweekday())

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
