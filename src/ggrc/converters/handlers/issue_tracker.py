# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Handlers for Issue Tracker fields"""

import re

from ggrc.converters.handlers import handlers
from ggrc.models.hooks.issue_tracker import \
    issue_tracker_params_container as params_container
from ggrc.models import Assessment
from ggrc.converters import errors
from ggrc.integrations.constants import DEFAULT_ISSUETRACKER_VALUES as \
    default_values


class IssueTrackerColumnHandler(handlers.ColumnHandler):
  """Column handler used for Issue Tracker related fields.

  This class provides method for Issue Tracker fields export and Issue Tracker
  default values.
  """

  def get_value(self):
    return self.row_converter.issue_tracker.get(self.key, "")

  def set_obj_attr(self):
    if not self.value:
      self.value = self._get_default_value()
    if self.dry_run or not self.value:
      return
    self.row_converter.issue_tracker[self.key] = self.value

  def _get_default_value(self):
    """Get default value for missed value in Issue Tracker attribute column."""
    value = None
    if isinstance(self.row_converter.obj, Assessment):
      value = self.row_converter.obj.audit.issue_tracker.get(self.key)
    default_value = value or default_values.get(self.key)
    return default_value


class IssueTrackerWithValidStates(IssueTrackerColumnHandler):
  """Column handler for columns with available valid states"""

  available_items = {
      "issue_type":
          params_container.IssueTrackerParamsContainer.AVAILABLE_TYPES,
      "issue_priority":
          params_container.IssueTrackerParamsContainer.AVAILABLE_PRIORITIES,
      "issue_severity":
          params_container.IssueTrackerParamsContainer.AVAILABLE_SEVERITIES,
  }

  def __init__(self, row_converter, key, **options):
    self.valid_states = self.available_items.get(key)
    super(IssueTrackerWithValidStates, self).__init__(row_converter,
                                                      key,
                                                      **options)

  def parse_item(self):
    value = self.raw_value.upper()
    if value not in self.valid_states:
      self.add_warning(errors.WRONG_VALUE_DEFAULT,
                       column_name=self.display_name)
      return None
    return value


class IssueTrackerAddsColumnHandler(IssueTrackerColumnHandler):
  """Column handler for hotlist and components ids"""

  def parse_item(self):
    try:
      value = int(self.raw_value)
    except ValueError:
      self.add_warning(errors.WRONG_VALUE_DEFAULT,
                       column_name=self.display_name)
      return None
    return value


class IssueTrackerTitleColumnHandler(IssueTrackerColumnHandler):
  """Column handler for Issue title for IssueTracked models"""

  def get_value(self):
    return self.row_converter.issue_tracker.get("title", "")

  def parse_item(self):
    """ Remove multiple spaces and new lines from text """
    value = self.raw_value or ""
    value = self.clean_whitespaces(value)
    if not value:
      value = self.row_converter.obj.title or \
          self.row_converter.attrs["title"].value
      self.add_warning(errors.WRONG_VALUE_DEFAULT,
                       column_name=self.display_name)
    return value

  @staticmethod
  def clean_whitespaces(value):
    """Change multiply whitespaces with single one in the value string."""
    return re.sub(r"\s+", " ", value)

  def set_obj_attr(self):
    if self.dry_run or not self.value:
      return
    self.row_converter.issue_tracker["title"] = self.value


class IssueTrackerEnabledHandler(IssueTrackerColumnHandler):
  """Column handler for ticket tracker integration column.

  Enabled flag stored as tinyint(1) in our DB.
  """
  _true = "on"
  _false = "off"

  TRUE_VALUES = {_true, }
  FALSE_VALUES = {_false, }

  def set_obj_attr(self):
    if self.dry_run:
      return
    self.row_converter.issue_tracker[self.key] = self.value

  def get_value(self):
    if self.row_converter.issue_tracker.get(self.key, ""):
      return self._true
    return self._false

  def parse_item(self):
    value = self.raw_value.strip().lower()

    if value in self.TRUE_VALUES:
      return True
    if value not in self.FALSE_VALUES:
      self.add_warning(errors.WRONG_VALUE_DEFAULT,
                       column_name=self.display_name)
    return False
