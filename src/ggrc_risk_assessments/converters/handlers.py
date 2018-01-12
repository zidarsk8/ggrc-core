# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc.converters.handlers.handlers import UserColumnHandler

COLUMN_HANDLERS = {
    "default": {
        "ra_counsel": UserColumnHandler,
        "ra_manager": UserColumnHandler,
    }
}
