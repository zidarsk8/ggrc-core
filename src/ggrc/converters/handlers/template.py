# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Handlers specific for Assessment templates."""


from ggrc.converters.handlers import handlers
from ggrc import converters


class TemplateObjectColumnHandler(handlers.ColumnHandler):
  """Handler for template object type field."""

  def parse_item(self):
    """Parse object type field for assessment templates."""
    exportables = converters.get_exportables()
    object_type = exportables.get(self.raw_value.strip().lower())
    if not object_type:
      self.add_error("invalid template object type")
      return

    return object_type.__name__
