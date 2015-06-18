# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import datetime
import monthdelta
from dateutil import relativedelta

from cycle_calculator import CycleCalculator

class MonthlyCycleCalculator(CycleCalculator):
  time_delta = monthdelta.monthdelta(1)
  date_domain = set(xrange(31))

  def __init__(self, workflow, base_date=None):
    super(MonthlyCycleCalculator, self).__init__(workflow)

    if not base_date:
      base_date = datetime.date.today()

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
    if relative_day not in MonthlyCycleCalculator.date_domain:
      raise ValueError(
        "Monthly recurring cycles can only have relative day in 1-31 range.")

    if not base_date:
      base_date = datetime.date(today.year, today.month, 1)
      # Base date can't start with 0, we are counting from 1 onwards,
      # therefore -1
      ddate = base_date + relativedelta.relativedelta(days=relative_day - 1)
    else:
      ddate = base_date + relativedelta.relativedelta(days=relative_day - base_date.day)

    # We want to go up to the end of the month and not over
    if ddate.month != base_date.month:
      ddate = ddate - relativedelta.relativedelta(days=ddate.day)

    return ddate
