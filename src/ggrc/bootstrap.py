# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from flask.ext.sqlalchemy import SQLAlchemy


def get_db():
  """Get modified db object."""
  db = SQLAlchemy()

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

  original_commit = db.session.commit

  def new_commit(*args, **kwargs):
    original_commit(*args, **kwargs)
    from ggrc.models.hooks import acl
    acl.after_commit()
    print "hello world"
    original_commit(*args, **kwargs)

  db.session.commit = new_commit
  return db
