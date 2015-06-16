# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

from one_time_cycle_calculator import OneTimeCycleCalculator
from weekly_cycle_calculator import WeeklyCycleCalculator
from monthly_cycle_calculator import MonthlyCycleCalculator

class WorkflowCycleCalculator:
  calculators = {
    "one_time": OneTimeCycleCalculator,
    "weekly": WeeklyCycleCalculator,
    "monthly": MonthlyCycleCalculator,
    # "quarterly": QuarterlyCycleCalculator,
    # "annually": AnnualCycleCalculator
  }

  def __init__(self, workflow):
    self.calculator = self.calculators[workflow.frequency](workflow)

  def task_date_range(self, task):
    return self.calculator.task_date_range(task)

  def workflow_date_range(self):
    return self.calculator.workflow_date_range()

  def next_cycle_start_date(self):
    return self.calculator.next_cycle_start_date()