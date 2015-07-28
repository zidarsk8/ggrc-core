# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com


from ggrc.converters import handlers
from ggrc.extensions import get_extension_modules

_column_handlers = {
    "contact": handlers.UserColumnHandler,
    "description": handlers.TextareaColumnHandler,
    "end_date": handlers.DateColumnHandler,
    "kind": handlers.OptionColumnHandler,
    "link": handlers.TextColumnHandler,
    "email": handlers.EmailColumnHandler,
    "means": handlers.OptionColumnHandler,
    "notes": handlers.TextareaColumnHandler,
    "owners": handlers.OwnerColumnHandler,
    "private": handlers.CheckboxColumnHandler,
    "report_end_date": handlers.DateColumnHandler,
    "report_start_date": handlers.DateColumnHandler,
    "secondary_contact": handlers.UserColumnHandler,
    "secondary_assessor": handlers.UserColumnHandler,
    "principal_assessor": handlers.UserColumnHandler,
    "slug": handlers.SlugColumnHandler,
    "start_date": handlers.DateColumnHandler,
    "status": handlers.StatusColumnHandler,
    "test_plan": handlers.TextareaColumnHandler,
    "title": handlers.RequiredTextColumnHandler,
    "verify_frequency": handlers.OptionColumnHandler,
    "network_zone": handlers.OptionColumnHandler,
    "program": handlers.ProgramColumnHandler,
    "directive": handlers.SectionDirectiveColumnHandler,
    "control": handlers.ControlColumnHandler,
    "audit": handlers.AuditColumnHandler,
    "program_mapped": handlers.ObjectPersonColumnHandler,
    "categories": handlers.ControlCategoryColumnHandler,
    "assertions": handlers.ControlAssertionColumnHandler,
}


def get_all_column_handlers():
  extension_handlers = _column_handlers
  for extension_module in get_extension_modules():
    contributed_handlers = getattr(
        extension_module, "contributed_column_handlers", None)
    if callable(contributed_handlers):
      extension_handlers.update(contributed_handlers())
    elif type(contributed_handlers) == dict:
      extension_handlers.update(contributed_handlers)
  return extension_handlers


COLUMN_HANDLERS = get_all_column_handlers()
