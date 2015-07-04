# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import datetime
from dateutil import relativedelta

from cycle_calculator import CycleCalculator

class QuarterlyCycleCalculator(CycleCalculator):
  """CycleCalculator implementation for quarterly workflows.

  Quarterly workflows have a specific date domain that also requires a bit more
  math. Option 1 is for Jan/Apr/Jul/Oct, option 2 is for Feb/May/Aug/Nov and
  option 3 is for Mar/Jun/Sep/Dec. Each task can go UP TO three
  months (non-inclusive).
  """
  time_delta = relativedelta.relativedelta(months=3)

  date_domain = {
    "1": set({1, 4, 7, 10}),
    "2": set({2, 5, 8, 11}),
    "3": set({3, 6, 9, 12})
  }

  def __init__(self, workflow, base_date=None):
    if not base_date:
      base_date = datetime.date.today()

    super(QuarterlyCycleCalculator, self).__init__(workflow)
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
    """Converts a quarterly representation of a day into concrete date object.

    Relative month is not the best description, but we have to standardize on
    something (better would be relative_quarter) to ensure consistent calls
    from CycleCalculator.

    First we ensure that we have both relative_day and relative_month or,
    alternatively, that relative_day carries month information as well.

    While task_date_range calls with explicit relative_month, reified_tasks
    stores relative days as MM/DD and we must first convert these values so
    that it can sort and get min and max values for tasks.

    Afterwards we must the LARGEST month for a specified quarter option that
    is SMALLER than base_date's month.

    Afterwards we repeat the math similar to monthly cycle calculator and
    ensure that the day is not overflowing to the next month.
    """
    today = datetime.date.today()

    # If we don't get relative month as argument, get month information from
    # relative day.
    if relative_month:
      relative_month = str(relative_month)
    elif relative_day:
      if "/" in str(relative_day):
        rs = relative_day.split("/")
        relative_day = int(rs[1])
        relative_month = rs[0]
      else:
        raise ValueError("Unknown format.")

    if not base_date:
      base_date = today

    # relative_month is 1, 2 or 3 and represents quarterly option, based
    # on which we select the month domain. Month is then the LARGEST
    # number from all the months that were before base_date.month
    month_domain = QuarterlyCycleCalculator.date_domain[relative_month]
    month = max(filter(lambda x: x <= base_date.month, month_domain))

    start_month = datetime.date(base_date.year, month, 1)
    ddate = start_month + relativedelta.relativedelta(days=relative_day - 1)

    # We want to go up to the end of the month and not over
    if ddate.month != start_month.month:
      ddate = ddate - relativedelta.relativedelta(days=ddate.day)
    return ddate