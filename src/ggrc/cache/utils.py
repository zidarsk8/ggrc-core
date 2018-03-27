# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Common operations on cache managers."""

from ggrc import cache


def get_cache_manager():
  """Returns an instance of CacheManager."""
  cache_manager = cache.CacheManager()
  cache_manager.initialize(cache.MemCache())
  return cache_manager
