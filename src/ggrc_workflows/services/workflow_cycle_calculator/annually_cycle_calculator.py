# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import datetime
from dateutil import relativedelta

from cycle_calculator import CycleCalculator

class AnnuallyCycleCalculator(CycleCalculator):
  """CycleCalculator implementation for annual workflows.

  Month domain is 1-12, date domain is 1-31.
  """

  time_delta = relativedelta.relativedelta(years=1)
  date_domain = set(xrange(31))
  month_domain = set(xrange(12))

  def __init__(self, workflow, base_date=None):
    if not base_date:
      base_date = datetime.date.today()

    super(AnnuallyCycleCalculator, self).__init__(workflow)
    self.tasks.sort(key=lambda t: "{0}/{1}".format(
      t.relative_start_month,
      t.relative_start_day))

    self.reified_tasks = {}
    for task in self.tasks:
      start_date, end_date = self.task_date_range(task, base_date)
      self.reified_tasks[task.id] = {
        'start_date': start_date,
        'end_date': end_date,
        'relative_start': self._rel_to_str(task.relative_start_day, task.relative_start_month),
        'relative_end': self._rel_to_str(task.relative_end_day, task.relative_end_month)
      }

  @staticmethod
  def relative_day_to_date(relative_day, relative_month=None, base_date=None):
    """Converts an annual relative day representation to concrete date object

    First we ensure that we have both relative_day and relative_month or,
    alternatively, that relative_day carries month information as well.

    While task_date_range calls with explicit relative_month, reified_tasks
    stores relative days as MM/DD and we must first convert these values so
    that it can sort and get min and max values for tasks.

    Afterwards we repeat the math similar to monthly cycle calculator and
    ensure that the day is not overflowing to the next month.
    """
    today = datetime.date.today()
    if relative_month:
      relative_month = int(relative_month)
    if relative_day:
      if "/" in str(relative_day):
        rs = relative_day.split("/")
        relative_day = int(rs[1])
        relative_month = int(rs[0])

    if not relative_day in AnnuallyCycleCalculator.date_domain:
      raise ValueError

    if not relative_month in AnnuallyCycleCalculator.month_domain:
      raise ValueError

    if not base_date:
      base_date = today

    start_month = datetime.date(base_date.year, relative_month, 1)
    ddate = start_month + relativedelta.relativedelta(days=relative_day - 1)

    # We want to go up to the end of the month and not over
    if ddate.month != start_month.month:
      ddate = ddate - relativedelta.relativedelta(days=ddate.day)
    return ddate
