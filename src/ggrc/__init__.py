# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Main GGRC module"""

from ggrc import bootstrap

db = bootstrap.get_db()

__all__ = [
    db
]
