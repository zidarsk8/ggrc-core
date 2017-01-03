# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Checker function for import pre commit hooks."""

from ggrc.converters import errors


def check_tasks(row_converter):
  """Checker for task group task objects.

  This checker should make sure if a task group task has any invalid values
  that should be ignored. Object will not be checked if there's already
  an error on and it's marked as ignored.

  Args:
    row_converter: RowConverter object with row data for a task group task
      import.
  """
  if row_converter.ignore:
    return

  obj = row_converter.obj
  if obj.start_date > obj.end_date:
    row_converter.add_error(
        errors.INVALID_START_END_DATES,
        start_date="Start date",
        end_date="End date",
    )


def check_cycle_tasks(row_converter):  # noqa
  """Checker for CycleTaskGroupObjectTask model objects.

  This checker should make sure if a cycle-task has any invalid values
  that should be ignored during update via import.

  Args:
    row_converter: RowConverter object with row data for a cycle-task
      import.
  """
  # Cycle-Task creation is denied. Don't need checks for new items.
  if row_converter.is_new:
    return
  obj = row_converter.obj
  if obj.start_date > obj.end_date:
    row_converter.add_error(
        errors.INVALID_START_END_DATES,
        start_date="Start Date",
        end_date="End Date",
    )
  if (obj.finished_date and obj.verified_date and
          obj.finished_date > obj.verified_date):
    row_converter.add_error(
        errors.INVALID_START_END_DATES,
        start_date="Actual Finish Date",
        end_date="Actual Verified Date",
    )
  if obj.cycle.is_current:
    if obj.status not in ('Finished', 'Verified'):
      if obj.finished_date:
        row_converter.add_error(
            errors.INVALID_STATUS_DATE_CORRELATION,
            date="Actual Finish Date",
            status="not Finished",
        )
      if obj.verified_date:
        row_converter.add_error(
            errors.INVALID_STATUS_DATE_CORRELATION,
            date="Actual Verified Date",
            status="not Verified",
        )
    elif obj.status == 'Finished' and obj.verified_date:
      row_converter.add_error(
          errors.INVALID_STATUS_DATE_CORRELATION,
          date="Actual Verified Date",
          status="not Verified",
      )
  else:
    if obj.verified_date:
      if not obj.finished_date:
        row_converter.add_error(
            errors.MISSING_VALUE_ERROR,
            column_name="Actual Finish Date",
        )


CHECKS = {
    "TaskGroupTask": check_tasks,
    "CycleTaskGroupObjectTask": check_cycle_tasks,
}
