# cache/factory.py
#
# This module creates the cache based on parameters specified
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: chandramouliv@google.com
# Maintained By: chandramouliv@google.com
#

from .localcache import LocalCache
class Factory:
  def __init__(self): 
    pass

  def create(self, name, arguments=None):
    if "local" in name :
      return LocalCache();
    elif  "remote" in name : 
      return MemCache();
    else: 
      return None
