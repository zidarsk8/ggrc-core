# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc.converters.handlers import handlers
from ggrc.converters import errors


class RequestStatusColumnHandler(handlers.StatusColumnHandler):

  def parse_item(self):
    value = handlers.StatusColumnHandler.parse_item(self)
    if value in {"Final", "Verified"}:
      value = "In Progress"
      self.add_warning(errors.REQUEST_INVALID_STATE)
    return value
