# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

from datetime import date

import holidays

class GoogleHolidays(holidays.UnitedStates):
  def _populate(self, year):
    holidays.UnitedStates._populate(self, year)
    self[date(year, 11, 27)] = "Thanksgiving Day 2"
    self[date(year, 12, 23)] = "Christmas Holiday"
    self[date(year, 12, 24)] = "Christmas Eve"
    self[date(year, 12, 31)] = "New Year's Eve"
