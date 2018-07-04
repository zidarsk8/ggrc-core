# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Bootstrap for ggrc db."""
import threading

from flask.ext.sqlalchemy import SQLAlchemy


def get_db():
  """Get modified db object."""
  database = SQLAlchemy()

  class String(database.String):
    """Simple subclass of sqlalchemy.orm.String which provides a default
    length for `String` types to satisfy MySQL
    """
    # pylint: disable=too-few-public-methods
    # this class is just to set the default string length and is not meant to
    # do anything else, so it does not need any other public methods.

    def __init__(self, length=None, *args, **kwargs):
      # TODO: Check for MySQL and only apply when needed
      if length is None:
        length = 250
      super(String, self).__init__(length, *args, **kwargs)
  database.String = String

  database.session.plain_commit = database.session.commit

  class HooksSemaphore(threading.local):

    def __init__(self, *args, **kwargs):
      super(HooksSemaphore, self).__init__(*args, **kwargs)
      self._flag = True


    def enable(self):
      self._flag = True

    def disable(self):
      self._flag = False

    def __bool__(self):
      return self._flag

    __nonzero__ = __bool__

  database.session.delay_hooks_semaphore = HooksSemaphore()

  def pre_commit_hooks():
    if not database.session.delay_hooks_semaphore:
      return
    database.session.flush()
    if hasattr(database.session, "reindex_set"):
      database.session.reindex_set.push_ft_records()

  def post_commit_hooks():
    if not database.session.delay_hooks_semaphore:
      return
    from ggrc.models.hooks import acl
    acl.after_commit()
  database.session.post_commit_hooks = post_commit_hooks
  database.session.pre_commit_hooks = pre_commit_hooks

  def hooked_commit(*args, **kwargs):
    """Commit override function.

    This function is meant for a single after commit hook that should only be
    used for ACL propagation.
    """
    database.session.pre_commit_hooks()
    database.session.plain_commit(*args, **kwargs)
    database.session.post_commit_hooks()

  database.session.commit = hooked_commit

  return database
