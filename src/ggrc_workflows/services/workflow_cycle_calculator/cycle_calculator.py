# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import datetime
from abc import ABCMeta, abstractmethod

from ggrc_workflows.services.workflow_cycle_calculator.google_holidays import GoogleHolidays

@property
def NotImplementedProperty(self):
  raise NotImplementedError

@property
def NotImpementedMethod(self):
  raise NotImplementedError

class CycleCalculator(object):
  """Cycle calculation for all workflow frequencies with the exception of
  one-time workflows.

  Cycle calculator is an abstract class that implements all the operations
  needed by workflows, namely task_date_range, workflow_date_range and
  next_cycle_start_date.

  Each concrete class has to implement it's own
  relative_day_to_date method that calculates the concrete date based on
  the base_date provided to the method and taking into account the specifics
  of the frequency. relative_day_to_date SHOULD NOT adjust dates but
  should only convert them to datetime.date objects.

  Attributes:
    date_domain: Concrete class's domain in which values passed to it are
                 to be found
    time_delta: Concrete class's atomic unit by which addition/subtraction
                will take place during calculations.
    HOLIDAYS: Official holidays with the addition of several days that Google
              observes. See file google_holidays.py for details.
  """
  __metaclass__ = ABCMeta

  date_domain = NotImplementedProperty
  time_delta = NotImplementedProperty

  HOLIDAYS = GoogleHolidays()

  @abstractmethod
  def relative_day_to_date(self):
    raise NotImplementedError("Converting from relative to concrete date"
                              "must be done in concrete classes.")


  def __init__(self, workflow, holidays=HOLIDAYS):
    """Initializes calculator based on the workflow and holidays.

    Generates a flat list of all the tasks in all task groups.

    Concrete classes have to sort tasks based on relative
    start days (DD or MM/DD) and generate a dictionary self.reified_tasks
    where each key is task.id and values are dictionaries with
    relative_start, relative_end and concrete start_date and end_date
    values. Example:

      self.reified_tasks[task.id] = {
        'start_date': start_date,
        'end_date': end_date,
        'relative_start': task.relative_start_day,
        'relative_end': task.relative_end_day
      }

    Args:
      workflow: Workflow for which we are calculating
      holidays: List (or object supporting 'in' operation) with the list of
                holidays on which events won't happen.
    """
    self.workflow = workflow
    self.holidays = holidays
    self.tasks = [
      task for task_group in self.workflow.task_groups
      for task in task_group.task_group_tasks]
    self.tasks.sort(key=lambda t: (t.relative_start_month, t.relative_start_day))

  def is_work_day(self, ddate):
    """Check whether specific ddate is workday or if it's a holiday/weekend.

    Args:
      ddate: datetime object
    Returns:
      Boolean: True if it's workday otherwise false.
    """
    return ddate.isoweekday() < 6 and ddate not in self.holidays

  def adjust_date(self, ddate):
    """Adjust date if it's not a work day.

    Calculates the first workday by going backwards by either subtracting
    appropriate number of days (if ddate is during weekend) or substracting
    by one day if it's a holiday. In case we still aren't on a workday we repeat
    the process recursively until we find the first workday.

    Args:
      date: datetime object
    Returns:
      datetime.date: First available workday.
    """
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

  def workflow_date_range(self):
    """Calculates the min start date and max end date across all tasks.

    Returns:
      tuple({datetime.date, datetime.date}): First start date and
      last end date.
    """
    tasks_start_dates = [v['start_date'] for _, v in self.reified_tasks.items()]
    tasks_end_dates = [v['end_date'] for _, v in self.reified_tasks.items()]
    return min(tasks_start_dates), max(tasks_end_dates)

  def task_date_range(self, task, base_date=None):
    """Calculates individual task's start and end date based on base_date.

    Taking base_date into account calculates individual task's start and
    end date with relative_day_to_date function provided by a specific
    concrete class.

    Args:
      task: Task object for which we are calculating start and end date
      base_date: Date based on which we convert from relative day to
                 concrete date.
    Returns:
      tuple({datetime.date, datetime.date}): Weekend and holiday
        adjusted start and end date.
    """
    if not base_date:
      base_date = datetime.date.today()

    start_day = self.relative_day_to_date(
      task.relative_start_day,
      relative_month=task.relative_start_month,
      base_date=base_date)

    end_day = self.relative_day_to_date(
      task.relative_end_day,
      relative_month=task.relative_end_month,
      base_date=base_date)

    # If the end_day is before start_day, end_date is overflowing
    # to next time unit.
    if end_day < start_day:
      end_day = end_day + self.time_delta

    # If both start day and end day have already happened we are
    # operating on time unit.
    if start_day <= end_day < base_date:
      start_day = start_day + self.time_delta
      end_day = end_day + self.time_delta

    # Before returning date object we adjust for holidays and weekends.
    return self.adjust_date(start_day), self.adjust_date(end_day)

  def next_cycle_start_date(self, base_date=None):
    """Calculates workflow's next cycle start date.

    Calculates workflow's next cycle start date based based on the minimum
    start date of the tasks.

    Usually this is first element of self.tasks,

    Args:
      base_date: The start date of the time unit we are operating on.
    Returns:
      datetime.date: Adjusted date when the next cycle is going to be
                     generated.
    """
    today = datetime.date.today()
    if not base_date:
      base_date = today

    tasks_start_dates = [
      (v['start_date'], v['relative_start'])
      for v in self.reified_tasks.values()]
    tasks_start_dates.sort(key=lambda x: x[0])

    tasks_end_dates = [
      (v['end_date'], v['relative_end'])
      for v in self.reified_tasks.values()]
    tasks_end_dates.sort(key=lambda x: x[0], reverse=True)

    min_date, min_rel = tasks_start_dates[0]
    if type(min_rel) is tuple:
      min_rsm, min_rsd = min_rel # min_relative_start_month, min_relative_start_day
    else:
      min_rsd = min_rel
      min_rsm = None

    min_start = self.relative_day_to_date(
      relative_day=min_rsd, relative_month=min_rsm,
      base_date=base_date)

    max_date, max_rel = tasks_end_dates[0]
    if type(max_rel) is tuple:
      max_rem, max_red = max_rel # max_relative_start_month, max_relative_start_day
    else:
      max_red = max_rel
      max_rem = None

    max_end = self.relative_day_to_date(
      relative_day=max_red, relative_month=max_rem,
      base_date=base_date)

    if max_end < min_start:
      max_end = max_end + self.time_delta

    # If we are calculating for a workflow who's first cycle is in the future
    # next start date is already calculated (min_start) and we don't have to
    # add to it, otherwise we have to add one time unit to the min_start.
    #
    # Example: We activate a weekly workflow on Monday, cycle start date
    # is on Tuesday, therefore next cycle start date is THIS Tuesday and
    # NOT NEXT Tuesday.
    #
    # This is only relevant when we activate workflow and not afterwards.
    if base_date == today:
      if self.adjust_date(min_start) > today and self.adjust_date(max_end) > today:
        base_date = base_date
      else:
        base_date = base_date + self.time_delta
    else:
      base_date = base_date + self.time_delta

    return self.adjust_date(self.relative_day_to_date(
      relative_day=min_rsd, relative_month=min_rsm,
      base_date=base_date))
