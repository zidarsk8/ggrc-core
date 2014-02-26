# caching/memcache.py
#
# This module provides wrapper to the Google AppEngine Memcache 
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# 
# Maintained By: dan@reciprocitylabs.com
#

from google.appengine.api import memcache
from cache import Cache
from cache import all_cache_entries
from collections import OrderedDict
from copy import deepcopy

"""
    Memcache implements the remote AppEngine Memcache mechanism

"""
class MemCache(Cache):

  def __init__(self, configparam=None):
    self.config = configparam
    self.name = 'memcache'

    # Setup Memcache
    for cache_entry in all_cache_entries():
      if cache_entry.cache_type is self.name:
        self.supported_resources[cache_entry.model_plural]=cache_entry.class_name
 
  def get_name(self):
   return self.name

  def set_config(self, configparam):
    self.config = configparam
	
  def get_config(self):
   return self.config

  def get(self, category, resource, filter): 
    if not self.is_caching_supported(category, resource):
      return None
    # Construct the Attributes for the given filter, resource and category
    # Invoke Google AppEngine mem cache API
    #
    data = OrderedDict()
    cache_key = self.get_key(category, resource)
    if cache_key is None:
      return  None
    ids, attrs = self.parse_filter(filter)
    if ids is None and attrs is None:
      return None
    else:
      if ids is None:
        return None
    for id in ids:
      attrvalues= memcache.get(cache_key + ":" + str(id))
      if attrvalues is not None:
        if attrs is None:
          data[id] = attrvalues
        else: 
          attr_dict = OrderedDict()
          for attr in attrs:
            if attrvalues.has_key(attr): 
              attr_dict[attr] = deepcopy(attrvalues.get(attr))
          data[id] = attr_dict
    return data

  def add(self, category, resource, data): 
    if not self.is_caching_supported(category, resource):
      return None
    entries = {}
    cache_key = self.get_key(category, resource)
    if cache_key is None:
      return None
    for key in data.keys(): 
      id = cache_key + ":" + str(key)
      cache_data = memcache.get(id) 
      if cache_data is None:
        memcache.add(id, deepcopy(data.get(key)))
        entries[key] = data
    return entries

  def update(self, category, resource, data): 
    return None

  def remove(self, category, resource, data): 
    return None

  def clean(self): 
    pass
