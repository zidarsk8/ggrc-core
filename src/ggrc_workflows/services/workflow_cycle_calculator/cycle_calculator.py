# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import datetime
import monthdelta
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

  def __init__(self, workflow):
    self.workflow = workflow

  next = NotImpementedMethod
  relative_day_to_date = NotImpementedMethod

  @staticmethod
  def weekend_adjust_date(self, ddate):
    if isinstance(ddate, datetime):
      weekday = ddate.isoweekday()
      if weekday >= 6:
        return ddate - datetime.timedelta(days=(weekday - 5))