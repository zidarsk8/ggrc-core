# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module with issue tracker integration utils."""

from ggrc.integrations import integrations_errors
from ggrc.integrations import issues


def has_access_to_issue(issue_id):
  # type: (int) -> bool
  """Check if there is access to specified issue."""
  has_access = True
  try:
    issues.Client().get_issue(issue_id)
  except integrations_errors.Error:
    has_access = False
  return has_access
