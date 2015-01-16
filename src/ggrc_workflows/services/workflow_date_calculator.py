# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: laran@reciprocitylabs.com
# Maintained By: laran@reciprocitylabs.com

from datetime import date, datetime, timedelta

'''
All dates are calculated raw. They are not adjusted for holidays or workdays.
Use WorkflowDateCalculator.nearest_work_day() to get a date adjusted for
weekends & holidays.
'''

class WorkflowDateCalculator(object):
  def __init__(self, workflow=None):
    self.workflow = workflow

  '''
  direction = 1  indicates FORWARD
  direction = -1 indicates BACKWARD
  '''
  @staticmethod
  def nearest_work_day(date_, direction):
    holidays = []
    while date_.weekday() > 4 or date_ in holidays:
      date_ = date_ + timedelta(direction)
    return date_

  def calc_nearest_start_date_after_basedate(self, basedate):
    frequency = self.workflow.frequency
    min_relative_start_day = self._calc_min_relative_start_day_from_tasks()
    min_relative_start_month = self._calc_min_relative_start_month_from_tasks()
    return WorkflowDateCalculator.calc_nearest_start_date_after_basedate_from_dates(
      basedate, frequency, min_relative_start_month, min_relative_start_day)

  @staticmethod
  def calc_nearest_start_date_after_basedate_from_dates(basedate, frequency, relative_start_month, relative_start_day):

    from monthdelta import monthdelta
    basedate_day_of_week = basedate.weekday()
    basedate_day_of_month = basedate.day
    basedate_month_of_year = basedate.month

    if "one_time" == frequency:
      start_date = date(year=basedate.year, month=relative_start_month, day=relative_start_day)
      if start_date < basedate:
        start_date = start_date + monthdelta(12)
      return start_date
    elif "weekly" == frequency:
      if relative_start_day == basedate_day_of_week:
        return basedate
      elif relative_start_day > basedate_day_of_week:
        day_delta = relative_start_day - basedate_day_of_week
        return basedate + timedelta(days=day_delta)
      elif relative_start_day < basedate_day_of_week:
        day_delta = basedate_day_of_week - relative_start_day
        return basedate + timedelta(days=7 - day_delta)
    elif "monthly" == frequency:
      if relative_start_day == basedate_day_of_month:
        return basedate
      elif relative_start_day > basedate_day_of_month:
        day_delta = relative_start_day - basedate_day_of_month
        return basedate + timedelta(days=day_delta)
      elif relative_start_day < basedate_day_of_month:
        start_date = basedate
        while start_date.day > relative_start_day:
          start_date = start_date + timedelta(days=-1)
        return start_date + monthdelta(1)
    elif "quarterly" == frequency:
      base_quarter_month = basedate_month_of_year % 3
      # We want 1-3 indexing instead of 0-2
      if base_quarter_month == 0:
        base_quarter_month = 3
      min_relative_start_quarter_month = relative_start_month

      if min_relative_start_quarter_month == base_quarter_month:
        if relative_start_day == basedate_day_of_month:
          return basedate  # Start today
        elif relative_start_day < basedate_day_of_month:
          start_date = date(basedate.year, basedate.month, basedate.day)
          start_date = start_date + monthdelta(3)
          day_delta = -1 * (basedate_day_of_month - relative_start_day)
          start_date = start_date + timedelta(days=day_delta)
          return start_date
        else:
          return date(year=basedate.year, month=basedate_month_of_year, day=relative_start_day)
      elif min_relative_start_quarter_month < base_quarter_month:
        start_date = date(
          year=basedate.year,
          month=basedate.month,
          day=relative_start_day
        ) + monthdelta(1)
        tmp_start_date = start_date
        tmp_quarter_month = tmp_start_date.month % 3
        if tmp_quarter_month == 0:
          tmp_quarter_month = 3
        month_counter = 1
        while tmp_quarter_month < min_relative_start_quarter_month:
          # Use start_date + monthdelta instead of adding 1 month at a time
          # with monthdelta(1) because monthdelta(1) adjusts the end date of
          # the month for the number of days in the month.
          tmp_start_date = start_date + monthdelta(month_counter)
          tmp_quarter_month = tmp_start_date.month % 3
          if tmp_quarter_month == 0:
            tmp_quarter_month = 3
        return tmp_start_date
      else:  # min_relative_start_quarter_month > base_quarter_month: Walk forward to a valid month
        return basedate + monthdelta(min_relative_start_quarter_month) - base_quarter_month
    elif "annually" == frequency:
      if basedate_month_of_year == relative_start_month:
        if basedate_day_of_month == relative_start_day:
          return basedate
        elif basedate_day_of_month > relative_start_day:
          return date(year=basedate.year + 1, month=relative_start_month, day=relative_start_day)
        elif basedate_day_of_month < relative_start_day:
          return date(year=basedate.year, month=relative_start_month, day=relative_start_day)
      elif basedate_month_of_year > relative_start_month:
        return date(year=basedate.year + 1, month=relative_start_month, day=relative_start_day)
      else:
        return date(year=basedate.year, month=relative_start_month, day=relative_start_day)
    else:
      pass

  def calc_nearest_end_date_after_start_date(self, start_date):
    frequency = self.workflow.frequency
    max_relative_end_day = self._calc_max_relative_end_day_from_tasks()
    max_relative_end_month = self._calc_max_relative_end_month_from_tasks()
    return WorkflowDateCalculator.calc_nearest_end_date_after_start_date_from_dates(
      frequency, start_date, max_relative_end_month, max_relative_end_day)

  @staticmethod
  def calc_nearest_end_date_after_start_date_from_dates(frequency, start_date, end_month, end_day):

    start_date_day_of_week = start_date.weekday()
    start_date_day_of_month = start_date.day
    start_date_month_of_year = start_date.month
    start_date_year = start_date.year

    if "one_time" == frequency:
      if end_month == start_date_month_of_year:
        if end_day == start_date_day_of_month:
          return start_date
        elif end_day > start_date_day_of_month:
          return date(year=start_date_year, month=end_month, day=end_day)
        else:
          return date(year=start_date_year + 1, month=end_month, day=end_day)
      elif end_month < start_date_month_of_year:
        return date(year=start_date_year + 1, month=end_month, day=end_day)
      else:
        return date(year=start_date_year, month=end_month, day=end_day)
    elif "weekly" == frequency:
      if end_day == start_date_day_of_week:
        return start_date
      elif end_day < start_date_day_of_week:
        return start_date + timedelta(days=end_day + (7 - start_date_day_of_week))
      else:
        return start_date + timedelta(days=(end_day - start_date_day_of_week))
    elif "monthly" == frequency:
      from monthdelta import monthdelta

      if end_day == start_date_day_of_month:
        return start_date
      elif end_day < start_date_day_of_month:
        end_date = start_date + monthdelta(1)
        while end_date.day > end_day:
          end_date = end_date + timedelta(days=-1)
        return end_date
      else:
        return start_date + timedelta(days=(end_day - start_date_day_of_month))
    elif "quarterly" == frequency:
      start_quarter_month = start_date_month_of_year % 3
      # Offset month because we want 1-based indexing, not 0-based
      if start_quarter_month == 0:
        start_quarter_month = 3
      if start_quarter_month == end_month:
        if start_date_day_of_month == end_day:
          return start_date
        elif start_date_day_of_month < end_day:
          return date(year=start_date_year, month=start_date_month_of_year, day=end_day)
        else:
          _end_month = start_date_month_of_year + 3
          _year = start_date_year
          if _end_month > 12:
            _year += _end_month / 12
            _end_month = (_end_month % 12)
          return date(year=_year, month=_end_month, day=end_day)
      elif start_quarter_month < end_month:
        return date(
          year=start_date_year,
          month=start_date_month_of_year + (end_month - start_quarter_month),
          day=end_day)
      else:
        from monthdelta import monthdelta
        end_date = date(
          year=start_date.year,
          month=start_date.month,
          day=end_day
        ) + monthdelta(1)
        tmp_end_date = end_date
        tmp_quarter_month = tmp_end_date.month % 3
        if tmp_quarter_month == 0:
          tmp_quarter_month = 3
        month_counter = 1
        # Can't use less_than operator here because of the looping
        # around quarters.
        while tmp_quarter_month != end_month:
          # Use start_date + monthdelta instead of adding 1 month at a time
          # with monthdelta(1) because monthdelta(1) adjusts the end date of
          # the month for the number of days in the month.
          tmp_end_date = end_date + monthdelta(month_counter)
          tmp_quarter_month = tmp_end_date.month % 3
          if tmp_quarter_month == 0:
            tmp_quarter_month = 3
        return tmp_end_date
    elif "annually" == frequency:
      if start_date_month_of_year == end_month:
        if start_date_day_of_month == end_day:
          return start_date
        elif start_date_day_of_month < end_day:
          return date(year=start_date_year, month=start_date_month_of_year, day=end_day)
        else:
          return date(year=start_date_year + 1, month=start_date_month_of_year, day=end_day)
      elif start_date_month_of_year < end_month:
        return date(year=start_date_year, month=end_month, day=end_day)
      else:
        return date(year=start_date_year + 1, month=end_month, day=end_day)
    else:
      pass

  @staticmethod
  def calc_next_cycle_start_date_after_start_date(start_date, frequency):
    from monthdelta import monthdelta
    if "one_time" == frequency:
      return start_date
    elif "weekly" == frequency:
      return start_date + timedelta(days=7)
    elif "monthly" == frequency:
      return start_date + monthdelta(1)
    elif "quarterly" == frequency:
      return start_date + monthdelta(3)
    elif "annually" == frequency:
      return start_date + monthdelta(12)
    else:
      pass

  @staticmethod
  def calc_next_cycle_start_date_after_basedate_from_dates(
      basedate, frequency, relative_start_month, relative_start_day):
    start_date = WorkflowDateCalculator.\
      calc_nearest_start_date_after_basedate_from_dates(
      basedate, frequency, relative_start_month, relative_start_day)
    return WorkflowDateCalculator.calc_next_cycle_start_date_after_start_date(start_date, frequency)

  def calc_next_cycle_start_date_after_basedate(self, basedate):
    start_date = self.calc_nearest_start_date_after_basedate(basedate)
    frequency = self.workflow.frequency
    return WorkflowDateCalculator.\
      calc_next_cycle_start_date_after_start_date(start_date, frequency)

  @staticmethod
  def calc_previous_cycle_start_date_before_basedate_from_dates(basedate, frequency, relative_start_month, relative_start_day):
    start_date = WorkflowDateCalculator.\
      calc_nearest_start_date_after_basedate_from_dates(
      basedate, frequency, relative_start_month, relative_start_day)
    return WorkflowDateCalculator.\
      calc_previous_cycle_start_date(start_date, frequency)

  @staticmethod
  def calc_previous_cycle_start_date(start_date, frequency):
    from monthdelta import monthdelta
    if "one_time" == frequency:
      return start_date
    elif "weekly" == frequency:
      return start_date + timedelta(days=-7)
    elif "monthly" == frequency:
      return start_date + monthdelta(-1)
    elif "quarterly" == frequency:
      return start_date + monthdelta(-3)
    elif "annually" == frequency:
      return start_date + monthdelta(-12)
    else:
      pass

  def calc_previous_cycle_start_date_before_basedate(self, basedate):
    start_date = self.calc_nearest_start_date_after_basedate(basedate)
    frequency = self.workflow.frequency
    return WorkflowDateCalculator.\
      calc_previous_cycle_start_date(start_date, frequency)

  def _calc_min_relative_start_month_from_tasks(self):
    min_start_month = None
    for tg in self.workflow.task_groups:
      for t in tg.task_group_tasks:
        relative_start_month = t.relative_start_month
        if min_start_month is None or relative_start_month < min_start_month:
          min_start_month = relative_start_month
    return min_start_month

  def _calc_min_relative_start_day_from_tasks(self):
    min_start_day = None
    for tg in self.workflow.task_groups:
      for t in tg.task_group_tasks:
        relative_start_day = t.relative_start_day
        if min_start_day is None or relative_start_day < min_start_day:
          min_start_day = relative_start_day
    return min_start_day

  def _calc_max_relative_end_day_from_tasks(self):
    max_end_day = None
    for tg in self.workflow.task_groups:
      for t in tg.task_group_tasks:
        relative_end_day = t.relative_end_day
        if max_end_day is None or relative_end_day > max_end_day:
          max_end_day = relative_end_day
    return max_end_day

  def _calc_max_relative_end_month_from_tasks(self):
    max_end_month = None
    for tg in self.workflow.task_groups:
      for t in tg.task_group_tasks:
        relative_end_month = t.relative_end_month
        if max_end_month is None or relative_end_month > max_end_month:
          max_end_month = relative_end_month
    return max_end_month
