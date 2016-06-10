# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com
"""Handlers for boolean attributes."""

import traceback
from flask import current_app

from ggrc.converters import errors
from ggrc.converters.handlers import handlers


class CheckboxColumnHandler(handlers.ColumnHandler):
  """Generic checkbox handler.

  This handles all possible boolean values that are in the database None, True
  and False.
  """

  ALLOWED_VALUES = {"yes", "true", "no", "false", "--", "---"}
  TRUE_VALUES = {"yes", "true"}
  NONE_VALUES = {"--", "---"}

  def parse_item(self):
    """ mandatory checkboxes will get evelauted to false on empty value """
    if self.raw_value == "":
      return False
    value = self.raw_value.lower() in self.TRUE_VALUES
    if self.raw_value == self.NONE_VALUES:
      value = None
    if self.raw_value.lower() not in self.ALLOWED_VALUES:
      self.add_warning(errors.WRONG_VALUE, column_name=self.display_name)
    return value

  def get_value(self):
    val = getattr(self.row_converter.obj, self.key, False)
    if val is None:
      return "--"
    return "true" if val else "false"

  def set_obj_attr(self):
    """ handle set object for boolean values

    This is the only handler that will allow setting a None value"""
    try:
      setattr(self.row_converter.obj, self.key, self.value)
    except Exception:  # pylint: disable=broad-except
      self.row_converter.add_error(errors.UNKNOWN_ERROR)
      trace = traceback.format_exc()
      error = "Import failed with:\nsetattr({}, {}, {})\n{}".format(
          self.row_converter.obj, self.key, self.value, trace)
      current_app.logger.error(error)


class KeyControlColumnHandler(CheckboxColumnHandler):
  """Handler for key-control column.

  key-control attribute or (Significance on frontend) is a boolean field with a
  dropdown menu that contains key, non-key and --- as values.
  """

  ALLOWED_VALUES = {"key", "non-key", "--", "---"}
  TRUE_VALUES = {"key"}
  NONE_VALUES = {"--", "---"}
