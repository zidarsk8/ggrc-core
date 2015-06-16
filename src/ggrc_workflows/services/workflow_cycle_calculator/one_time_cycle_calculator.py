# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import datetime
import monthdelta
from dateutil import relativedelta

from ggrc_workflows.services.workflow_cycle_calculator.cycle_calculator import CycleCalculator

class OneTimeCycleCalculator(CycleCalculator):
  years_10 = relativedelta.relativedelta(years=10)
  today = datetime.date.today()
  date_domain = (today - years_10, today + years_10)

  def time_delta(self):
    return None
