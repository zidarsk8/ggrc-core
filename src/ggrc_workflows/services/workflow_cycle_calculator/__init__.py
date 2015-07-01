# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

from one_time_cycle_calculator import OneTimeCycleCalculator
from weekly_cycle_calculator import WeeklyCycleCalculator
from monthly_cycle_calculator import MonthlyCycleCalculator
from quarterly_cycle_calculator import QuarterlyCycleCalculator
from annually_cycle_calculator import AnnuallyCycleCalculator

def get_cycle_calculator(workflow):
  """Gets the cycle calculator based on the workflow's frequency.

  Args:
    workflow: Workflow object

  Returns:
    SomeCalculator(CycleCalculator): CycleCalculator's concrete implementation
  """
  calculators = {
    "one_time": OneTimeCycleCalculator,
    "weekly": WeeklyCycleCalculator,
    "monthly": MonthlyCycleCalculator,
    "quarterly": QuarterlyCycleCalculator,
    "annually": AnnuallyCycleCalculator
  }
  return calculators[workflow.frequency](workflow)
