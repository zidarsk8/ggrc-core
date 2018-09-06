# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""GGRC UI utility functions"""
import nerodia

from lib.utils import test_utils


def select_user(root, email):
  """Selects user in person autocomplete list."""
  def autocomplete_row():
    """Returns a row with an email."""
    # Iterating through elements may raise exception if elements are removed
    # during iteration
    # (https://github.com/watir/watir/issues/769)
    try:
      rows = list(root.elements(class_name="ui-menu-item"))
      # Only user is shown in some cases
      # In others user and "Create" is shown
      if len(rows) in (1, 2):
        row = rows[0]
        if email in row.text:
          return row
    except nerodia.exception.UnknownObjectException:
      pass
    return False
  row = test_utils.wait_for(autocomplete_row)
  row.click()
