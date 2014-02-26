# cache/factory.py
#
# This module creates the cache based on parameters specified
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# 
# Maintained By: dan@reciprocitylabs.com
#

from .localcache import LocalCache
from .memcache import MemCache 
class Factory:
  def __init__(self): 
    pass

  def create(self, name, arguments=None):
    if "local" in name :
      return LocalCache();
    elif  "memcache" in name : 
      return MemCache();
    else: 
      return None
