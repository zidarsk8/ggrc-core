# Copyright (C) 2016 Google Inc., authors, and contributors
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

import os
import sys

from flask.ext.sqlalchemy import SQLAlchemy

from ggrc import settings


def set_appengine_packages_path():
  if getattr(settings, 'APP_ENGINE', False):
    if os.path.exists(os.path.join(settings.BASE_DIR, 'packages')):
      sys.path.insert(0, os.path.join(settings.BASE_DIR, 'packages'))
    else:
      sys.path.insert(0, os.path.join(settings.BASE_DIR, 'packages.zip'))


def extend_db_string(db):
  """Set the default string lenght to 250."""

  class String(db.String):
    """Simple subclass of sqlalchemy.orm.String which provides a default
    length for `String` types to satisfy MySQL
    """

    def __init__(self, length=None, *args, **kwargs):
      # TODO: Check for MySQL and only apply when needed
      if length is None:
        length = 250
      return super(String, self).__init__(length, *args, **kwargs)
  db.String = String


db = SQLAlchemy()
extend_db_string(db)
set_appengine_packages_path()
