# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Helper methods."""

from flask import _app_ctx_stack

from ggrc.utils import structures


def without_sqlalchemy_cache(func):
  """Switch off SQLAlchemy queries cache filling.

  SQLAlchemy cache all executed queries in
  _app_ctx_stack.top.sqlalchemy_queries variable if DEBUG or
  SQLALCHEMY_RECORD_QUERIES config variable is set to True.
  This decorator make the cache empty everywhere in wrapped function.
  """
  def wrapper(*args, **kwargs):
    """Wrapper function."""
    queries = None
    has_queries = False
    if hasattr(_app_ctx_stack.top, "sqlalchemy_queries"):
      queries = _app_ctx_stack.top.sqlalchemy_queries
      has_queries = True

    _app_ctx_stack.top.sqlalchemy_queries = structures.EmptyList()

    try:
      res = func(*args, **kwargs)
    finally:
      if has_queries:
        _app_ctx_stack.top.sqlalchemy_queries = queries
      else:
        del _app_ctx_stack.top.sqlalchemy_queries
    return res
  return wrapper
