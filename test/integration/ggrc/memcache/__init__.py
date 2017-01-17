
# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc import settings

if getattr(settings, 'MEMCACHE_MECHANISM', False) is True:
  from ggrc.cache import LocalCache
  from ggrc.cache import MemCache
  from ggrc.cache import CacheManager
  from integration.ggrc.memcache.testcachemanager import TestCacheManager
