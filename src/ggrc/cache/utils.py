# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Common operations on cache managers."""

from ggrc import cache
import ggrc.models


def get_cache_manager():
  """Returns an instance of CacheManager."""
  cache_manager = cache.CacheManager()
  cache_manager.initialize(cache.MemCache())
  return cache_manager


def get_cache_key(obj, type=None, id=None):
  """Returns a string identifier for the specified object or stub.

  `obj` can be:
    <db.Model> -- declarative model instance
    (type, id) -- tuple
    { 'type': type, 'id': id } -- dict
  """
  if isinstance(obj, tuple):
    type, id = obj
  elif isinstance(obj, dict):
    type = obj.get('type', None)
    id = obj.get('id', None)
  if isinstance(type, (str, unicode)):
    model = ggrc.models.get_model(type)
    assert model is not None, "Invalid model name: {}".format(type)
    type = ggrc.models.get_model(type)._inflector.table_plural
  if not isinstance(obj, (tuple, dict)):
    if type is None:
      type = obj._inflector.table_plural
    if id is None:
      id = obj.id
  return 'collection:{type}:{id}'.format(type=type, id=id)
