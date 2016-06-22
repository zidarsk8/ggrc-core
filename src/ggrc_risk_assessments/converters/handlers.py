# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc.converters.handlers.handlers import UserColumnHandler

COLUMN_HANDLERS = {
    "ra_counsel": UserColumnHandler,
    "ra_manager": UserColumnHandler,
}
