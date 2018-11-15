# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Util to get objects from flask.g.request_storage"""

import flask


def get(name, default=None):
  """Returns object from storage.
  It is expected that object is mutable(by default returns dict)"""
  if default is None:
    default = {}
  if hasattr(flask.g, "request_storage"):
    storage = flask.g.request_storage
  else:
    storage = flask.g.request_storage = {}
  if name not in storage:
    storage[name] = default
  return storage[name]
