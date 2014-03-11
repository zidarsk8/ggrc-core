# cache/cachemanager.py
#
# This module provides the encapsulation to GGRC cache mechanism as well apply policies to determine which objects to add, remove, etc.
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
#
# Maintained By: dan@reciprocitylabs.com
#


"""
    CacheManager provides encapsulation to the caching mechanism as well as working with Data transfer objects(DTO)

"""
from collections import OrderedDict
from cache import all_cache_entries, all_mapping_entries

class CacheManager:
  cache = OrderedDict()
  config = OrderedDict()
  supported_classes={}
  supported_mappings={}
  factory = None
  policy_manager = None
  dto_manager = None
  new = {}
  dirty = {}
  deleted = {}
  marked_for_add={}
  marked_for_update={}
  marked_for_delete=[]

  def __init__(self):
    pass	
	
  # Initialize Cache Manager and configure cache mechanism and its related policies
  #
  def initialize(self):
    if self.get_factory() is None:
      return

    if self.get_config() is None:
      return

    # 1. Build supported classes dictionary for getting resource names for SQL Alchemy event listeners
    #
    for cache_entry in all_cache_entries():
      self.supported_classes[cache_entry.class_name] = cache_entry.model_plural

    for mapping_entry in all_mapping_entries():
      self.supported_mappings[mapping_entry.class_name] = mapping_entry

    # 2. Build cache dictionary indexed by cache mechanism such as 'local', 'memcache' 
    #
    cache_list = self.get_config().get_all_cache()
    for cache_name in cache_list:
      cache_object = self.get_factory().create(cache_name)
      self.get_cache()[cache_object.get_name()]=cache_object

    # 3. Setup policy manager 
    #
    self.policy_manager = self.get_config().get_policy_manager()

    # 4. Setup DTO manager 
    #
    self.dto_manager= self.get_config().get_dto_manager()

    # 5. Initialize dictionaries for caching updates
    #
    self.dto_manager= self.get_config().get_dto_manager()
    self.new = {}
    self.dirty = {}
    self.deleted = {}
    self.marked_for_add={}
    self.marked_for_update={}
    self.marked_for_delete=[]

  def set_factory(self, factory):
    self.factory = factory
	
  def set_config(self, config):
    self.config = config

  def get_factory(self):
    return self.factory 
	
  def get_config(self):
    return self.config

  def get_policy_manager(self):
    return self.policy_manager

  def get_dto_manager(self):
    return self.dto_manager

  def get_cache(self):
    return self.cache

  def get_collection(self, category, resource, filter): 
    # 1. Apply policyManager rules to check if caching is allowed
    #
    if not self.is_caching_supported(category, resource, filter, 'get_collection'): 
      return None
		
    # 2. Add for each cache mechanism, by calling all the configured cache mechanisms
    #
    objs = OrderedDict()
    cache_dict = self.get_cache()
    for key, obj in cache_dict.items():
      # returned_obj is returned None if one of configured policies for the cache fails or ERRORs
      returned_obj = obj.get(category, resource, filter)
      if returned_obj is not None:
        objs[key] = returned_obj

    # 3. Apply DTO Manager to convert the objs into a JSON - TBD
    # 
    return self.format_dto(objs)

  def add_collection(self, category, resource, data): 
    # 1. Parse the data into DTO
    #
    dto = self.parse_dto(data)

    # 2. Apply policyManager rules - TBD
    #
    if not self.is_caching_supported(category, resource, dto, 'add_collection'): 
      return None

    # 3. For each cache mechanism, add entries in cache  if allowed
    #
    objs = OrderedDict()
    cache_dict = self.get_cache()
    for name, cache_object in cache_dict.items():
      objs[name] = cache_object.add(category, resource, dto)

    # 4. Apply DTO Manager to convert the objs into a JSON 
    #
    return self.format_dto(objs)

  def update_collection(category, resource, data): 
    # 1. Parse the data into DTO
    dto = self.parse_dto(data)

    # 2. Apply policyManager rules - TBD
    #
    if not self.is_caching_supported(category, resource, dto, 'update_collection'): 
      return None

    # 3. For each cache mechanism, update entries in cache 
    #
    objs = OrderedDict()
    cache_dict = self.get_cache()
    for name, cache_object in cache_dict.items():
      objs[name] = cache_object.update(category, resource, dto)

    # 4. Apply DTO Manager to convert the objs into a JSON 
    #
    return self.format_dto(objs)

  def delete_collection(self, category, resource, data): 
    # 1. Parse the data into DTO
    dto = self.parse_dto(data)

    # 2. Apply policyManager rules - TBD
    #
    if not self.is_caching_supported(category, resource, dto, 'delete_collection'): 
      return None

    # 3. For each cache mechanism, update entries in cache 
    #
    objs = OrderedDict()
    cacheDict = self.get_cache()
    for name, cacheObject in cacheDict:
      objs[name] = cacheObject.remove(category, resource, dto)

    # 4. Apply DTO Manager to convert the objs into a JSON 
    #
    return self.formatDTO(objs)

  def is_caching_supported(self, category, resource, data=None, operation=None):
    # REVISIT: Leverage PolicyManager for apply all configured policies for specified parameters
    #
    for key, cache in self.get_cache().items():
      if cache.is_caching_supported(category, resource): 
        return True
    return False 
   
  def bulk_get(self, data):
    # REVISIT: only one cache mechanism is supported and returns the first matched ones
    for key, cache in self.get_cache().items():
      return cache.get_multi(data)

  def bulk_add(self, data):
    # REVISIT: only one cache mechanism is supported and returns the first matched ones
    for key, cache in self.get_cache().items():
      return cache.add_multi(data)

  def bulk_update(self, data):
    # REVISIT: only one cache mechanism is supported and returns the first matched ones
    get_result = {}
    for key, cache in self.get_cache().items():
      get_result = cache.get_multi(data.keys())
      for key, updates in data.items():
        for update_key, update_value in updates.items(): 
          get_result[key][update_key] = update_value
    return cache.update_multi(get_result)

  def bulk_delete(self, data):
    # REVISIT: only one cache mechanism is supported and returns the first matched ones
    for key, cache in self.get_cache().items():
      return cache.remove_multi(data)

  def parse_dto(self, data):
    # Apply DTO manager
    return data

  def format_dto(self, data):
    # Apply DTO manager
    return data

  def clean(self):
    cache_dict= self.get_cache()
    if len(cache_dict) > 0:
      for name, cache_object in cache_dict.items():
        cache_object.clean()
    cache_dict.clear()
    return True

  def clear_cache(self):
    self.new = {}
    self.dirty = {}
    self.deleted = {}
    self.marked_for_add={}
    self.marked_for_update={}
    self.marked_for_delete=[]
