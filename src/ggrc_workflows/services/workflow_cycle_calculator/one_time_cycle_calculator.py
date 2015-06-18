# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

from ggrc_workflows.services.workflow_cycle_calculator.cycle_calculator import CycleCalculator

class OneTimeCycleCalculator(CycleCalculator):
  def __init__(self, workflow):
    super(OneTimeCycleCalculator, self).__init__(workflow)
    self.tasks = sorted(self.tasks, key=lambda t: t.start_date)

  def relative_day_to_date(self):
    raise NotImplemented("Relative days are not applicable "
                         "for one-time workflows.")

  def task_date_range(self, task, base_date=None):
    return task.start_date, task.end_date

  def workflow_date_range(self):
    tasks_start_dates = [task.start_date for task in self.tasks]
    tasks_end_dates = [task.end_date for task in self.tasks]
    return min(tasks_start_dates), max(tasks_end_dates)

  def next_cycle_start_date(self, base_date=None):
    return None
