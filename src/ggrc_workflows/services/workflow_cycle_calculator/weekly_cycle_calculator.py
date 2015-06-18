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