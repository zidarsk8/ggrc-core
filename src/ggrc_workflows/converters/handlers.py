# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

""" Module for all special column handlers for workflow objects """

from ggrc.converters.handlers import ColumnHandler
from ggrc.converters import errors


class FrequencyColumnHandler(ColumnHandler):

  """ Handler for workflow frequency column """

  frequency_map = {
      "one time": "one_time"
  }

  def parse_item(self):
    """ parse frequency value

    Returning None will set the default frequency to one_time.
    """
    if not self.raw_value:
      return None
    value = self.raw_value.lower()
    frequency = self.frequency_map.get(value, value)
    if value not in self.row_converter.object_class.VALID_FREQUENCIES:
      self.add_error(errors.WRONG_VALUE, column_name=self.display_name)
    return frequency

  def get_value(self):
    reverse_map = {v: k for k, v in self.frequency_map.items()}
    value = getattr(self.row_converter.obj, self.key, self.value)
    return reverse_map.get(value, value)


COLUMN_HANDLERS = {
    "frequency": FrequencyColumnHandler,
}
