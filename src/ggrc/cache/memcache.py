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
    self.client = None

    # Setup Memcache
    for cache_entry in all_cache_entries():
      if cache_entry.cache_type is self.name:
        self.supported_resources[cache_entry.model_plural]=cache_entry.class_name
        self.memcache_client = memcache.Client()
 
  def get_name(self):
   return self.name

  def set_config(self, configparam):
    self.config = configparam
	
  def get_config(self):
   return self.config

  def get(self, category, resource, filter): 
    if not self.is_caching_supported(category, resource):
      return None
    # REVISIT: use memcache.Client.gets_multi() instead of gets()
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
      attrvalues= self.memcache_client.gets(cache_key + ":" + str(id))
      if attrvalues is not None:
        if attrs is None:
          data[id] = attrvalues
        else: 
          attr_dict = OrderedDict()
          for attr in attrs:
            if attrvalues.has_key(attr): 
              attr_dict[attr] = deepcopy(attrvalues.get(attr))
          data[id] = attr_dict
      else:
        # All or None policy is enforced, if one of the objects is not available in cache, then we return empty
        return None
    return data

  def add(self, category, resource, data): 
    if not self.is_caching_supported(category, resource):
      return None
    entries = {}
    cache_key = self.get_key(category, resource)
    if cache_key is None:
      return None
    # REVISIT: use memcache.Client.add_multi() instead of add()
    #
    for key in data.keys(): 
      id = cache_key + ":" + str(key)
      cache_data = self.memcache_client.gets(id) 
      if cache_data is None:
        if self.memcache_client.add(id, data.get(key)) is False:
          # REVISIT: throw exceptions on errors to log critical events
          return  None
        entries[key] = data
    return entries

  def update(self, category, resource, data): 
    if not self.is_caching_supported(category, resource):
      return None
    entries = {}
    cache_key = self.get_key(category, resource)
    if cache_key is None:
      return None
    # REVISIT: use memcache.Client.cas_multi(), gets_multi() instead of cas(), gets()
    #
    for key in data.keys(): 
      id = cache_key + ":" + str(key)
      cache_data = self.memcache_client.gets(id) 
      if cache_data is None:
        # Log the event for add failures
        if self.memcache_client.cas(id, data.get(key)) is False:
          # REVISIT: throw exceptions on errors to log critical events
          return  None
        entries[key] = data
    return entries

  def remove(self, category, resource, data): 
    if not self.is_caching_supported(category, resource):
      return None
    entries = {}
    cache_key = self.get_key(category, resource)
    if cache_key is None:
      return None
    # REVISIT: use memcache.Client.delete_multi(), gets_multi() instead of delete(), gets()
    #
    for key in data.keys(): 
      id = cache_key + ":" + str(key)
      cache_data = self.memcache_client.gets(id) 
      if cache_data is not None:
        retvalue = self.memcache_client.delete(id)
        # Log the event of delete failures
        if retvalue is not 2:
          # REVISIT: throw exceptions on errors to log critical events
          return None
        entries[key] = data
    return entries

  def add_multi(self, data): 
	return self.memcache_client.add_multi(data)

  def get_multi(self, data): 
	return self.memcache_client.gets_multi(data, '', None, True)

  def update_multi(self, data): 
	return self.memcache_client.cas_multi(data)

  def remove_multi(self, data): 
	return self.memcache_client.delete_multi(data)

  def clean(self): 
    pass
