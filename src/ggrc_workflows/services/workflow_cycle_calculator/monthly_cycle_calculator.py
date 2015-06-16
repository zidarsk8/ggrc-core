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

