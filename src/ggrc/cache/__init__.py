# cache/__init__.py
#
# This module does initialization of GGRC cache
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: chandramouliv@google.com
# Maintained By: chandramouliv@google.com
#


from .localcache import LocalCache
from .memcache import MemCache
from .cachemanager import CacheManager
from .config import Config
from .factory import Factory

cache_manager=CacheManager()

def get_cache_manager():
   return cache_manager 
