# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Checker function for import pre commit hooks."""

from ggrc.converters import errors


def check_tasks(row_converter):
  """Checker for task group task objects.

  This checker should make sure if a task group task has any invalid values
  that should be ignored.

  Args:
    row_converter: RowConverter object with row data for a task group task
      import.
  """
  obj = row_converter.obj
  if obj.start_date > obj.end_date:
    row_converter.add_error(
        errors.INVALID_START_END_DATES,
        start_date="Start date",
        end_date="End date",
    )


CHECKS = {
    "TaskGroupTask": check_tasks,
}
