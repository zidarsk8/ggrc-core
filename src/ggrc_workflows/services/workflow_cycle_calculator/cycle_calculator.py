# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import datetime
import monthdelta
import operator
from datetime import date, datetime, timedelta
from dateutil import relativedelta

@property
def NotImplementedProperty(self):
  raise NotImplementedError

@property
def NotImpementedMethod(self):
  raise NotImplementedError

class CycleCalculator(object):
  date_domain = NotImplementedProperty
  time_unit = NotImplementedProperty
  time_delta = NotImplementedProperty

  relative_day_to_date = NotImpementedMethod

  YEAR = date.today().year

  HOLIDAYS = [
    date(year=YEAR, month=1, day=1),   # Jan 01 New Year's Day
    date(year=YEAR, month=1, day=19),  # Jan 19 Martin Luther King Day
    date(year=YEAR, month=2, day=16),  # Feb 16 President's Day
    date(year=YEAR, month=5, day=25),  # May 25 Memorial Day
    date(year=YEAR, month=7, day=2),   # Jul 02 Independence Day Holiday
    date(year=YEAR, month=7, day=3),   # Jul 03 Independence Day Eve
    date(year=YEAR, month=9, day=7),   # Sep 07 Labor Day
    date(year=YEAR, month=11, day=26), # Nov 26 Thanksgiving Day
    date(year=YEAR, month=11, day=27), # Nov 27 Thanksgiving Day 2
    date(year=YEAR, month=12, day=23), # Dec 23 Christmas Holiday
    date(year=YEAR, month=12, day=24), # Dec 24 Christmas Eve
    date(year=YEAR, month=12, day=25), # Dec 25 Christmas Day
    date(year=YEAR, month=12, day=31), # Dec 31 New Year's Eve
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
      ddate = ddate - timedelta(days=(weekday - 5))

    # Adjusting for holidays
    if ddate in self.holidays:
      ddate = ddate - timedelta(days=1)

    # In case we still don't have a workday, repeat
    if not self.is_work_day(ddate):
      self.adjust_date(ddate)

    return ddate