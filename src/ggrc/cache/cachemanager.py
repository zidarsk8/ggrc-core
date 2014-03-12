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
    CacheManager provides encapsulation to the caching mechanism 

"""
from collections import OrderedDict
from cache import all_cache_entries, all_mapping_entries

class CacheManager:
  """ Cache manager provides encapsulation to caching mechanims such as Memcache

  Attributes:
    cache: Ordered dictionary of all cache objects derived from base class (Cache)
    config: Ordered dictionary of config objects
    supported_classes: Model plural table name for a supported resource type
    supported_mappings: Mapping entry tuples for a supported resource type
    factory: Factory class to create cache object
    policy_manager: Future use to apply All or None and other policies
    dto_manager: Future use to allow transformation of Data transfer object (DTO) into formats such as JSON
    new, dirty, deleted: temporary dictionaries used in session event listeners before and after flush 
    marked_for_<op>: dictionaries used in session event listeners after flush, before and after commit

  Returns:
    None 
  """
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
	
  def initialize(self):
    """
      Initialize Cache Manager, configure cache mechanism and its related policies and DTO mechanisms
    """
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
    """ get collection from cache 

    Args:
      category: collection or stub
      resource: regulation, controls, etc.
      filter: dictionary containing ids and optional attrs

    Returns:
      DTO formatted string, e.g. JSON string representation
    """

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
    """ add collection in cache 

    Args:
      category: collection or stub
      resource: regulation, controls, etc.
      data: dictionary containing ids and attrs to update
    Returns:
     DTO formatted string, e.g. JSON string representation
    """

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
    """ update collection in cache 

    Args:
      category: collection or stub
      resource: regulation, controls, etc.
      data: dictionary containing ids and attrs to update
    Returns:
     DTO formatted string, e.g. JSON string representation
    """

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
    """ delete collection from cache 

    Args:
      category: collection or stub
      resource: regulation, controls, etc.
      data: dictionary containing ids of the resource to delete
    Returns:
      DTO formatted string, e.g. JSON string representation
    """

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
    """ Check if caching is supported

    Args:
      category: collection or stub
      resource: regulation, controls, etc.
      data: additional data such as context information, Default is None
      operation: operation performed such as get, update, delete or add

    Returns:
      True if caching is supported for the category and resource. 
      False otherwise
    """

    # TODO(ggrcdev): Leverage PolicyManager for apply all configured policies for specified parameters
    #
    for key, cache in self.get_cache().items():
      if cache.is_caching_supported(category, resource): 
        return True
    return False 
   
  def bulk_get(self, data):
    """ Perform Bulk Get operations in cache for specified data

    Args:
      data: keys for bulk get
    Returns:
     Result of cache get_multi
    """

    # TODO(ggrcdev): only memcache is supported and the first matched ones is used
    for key, cache in self.get_cache().items():
      return cache.get_multi(data)

  def bulk_add(self, data):
    """ Perform Bulk Add operations in cache for specified data

    Args:
      data: keys for bulk add
    Returns:
     Result of cache add_multi
    """

    # TODO(ggrcdev): only memcache is supported and the first matched ones is used
    for key, cache in self.get_cache().items():
      return cache.add_multi(data)

  def bulk_update(self, data):
    """ Perform Bulk update operations in cache for specified data

    Args:
      data: keys for bulk update
    Returns:
     Result of cache update_multi
    """
    # TODO(ggrcdev): only memcache is supported and the first matched ones is used
    get_result = {}
    for key, cache in self.get_cache().items():
      get_result = cache.get_multi(data.keys())
      for key, updates in data.items():
        for update_key, update_value in updates.items(): 
          get_result[key][update_key] = update_value
    return cache.update_multi(get_result)

  def bulk_delete(self, data):
    """ Perform Bulk Delete operations in cache for specified data

    Args:
      data: keys for bulk delete
    Returns:
     Result of cache remove_multi
    """
    # TODO(ggrcdev): only memcache is supported and the first matched ones is used
    for key, cache in self.get_cache().items():
      return cache.remove_multi(data)

  def parse_dto(self, data):
    """ parse JSON representation into DTO object using DTO manager
    """
    # Apply DTO manager
    return data

  def format_dto(self, data): 
    """ Format DTO object into a representation such as JSON using DTO manager
    """
    # Apply DTO manager
    return data

  def clean(self):
    """ Cleanup cache manager resources
    """
    cache_dict= self.get_cache()
    if len(cache_dict) > 0:
      for name, cache_object in cache_dict.items():
        cache_object.clean()
    cache_dict.clear()
    return True

  def clear_cache(self):
    """ Clear temporary dictionaries used for cache operations
    """
    self.new = {}
    self.dirty = {}
    self.deleted = {}
    self.marked_for_add={}
    self.marked_for_update={}
    self.marked_for_delete=[]
