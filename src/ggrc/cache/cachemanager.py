# cache/cachemanager.py
#
# This module provides the encapsulation to GGRC cache mechanism as well apply policies to determine which objects to add, remove, etc.
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: chandramouliv@google.com
# Maintained By: chandramouliv@google.com
#


"""
    CacheManager provides encapsulation to the caching mechanism as well as working with Data transfer objects(DTO)

"""
from collections import OrderedDict
from sqlalchemy.orm.session import Session
from sqlalchemy import event
from cache import all_cache_entries

class CacheManager:
  cache = OrderedDict()
  polices = OrderedDict()
  config = OrderedDict()
  supported_classes={}
  factory = None
  policy_manager = None
  dto_manager = None
  new = None
  dirty = None
  deleted = None

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

    # 5. Setup Event listeners for SQL Alchemy Session flush, commit, rollback events
    #    before flush and after flush will invoke update/delete collection in cache
    #
    self.new = {}
    self.dirty = {}
    self.deleted = {}
    event.listen(Session, 'before_flush', self.update_cache_before_flush)
    event.listen(Session, 'after_flush', self.update_cache_after_flush)
    event.listen(Session, 'after_commit', self.clear_cache)
    event.listen(Session, 'after_rollback', self.clear_cache)

	
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
    #print "CACHE: dictionary: ", cache_dict
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
    #print "CACHE: data to add to collection %s" %(dto)
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
      else:
         return False 

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

  def update_cache_before_flush(self, session, flush_context, objects):
    """
    Before the flush happens, we can still access to-be-deleted objects, so
    record JSON for log here
    """
    for o in session.new:
      if hasattr(o, 'log_json'):
        self.new[o] = o.log_json()
    for o in session.deleted:
      if hasattr(o, 'log_json'):
        self.deleted[o] = o.log_json()
    dirty = set(o for o in session.dirty if session.is_modified(o))
    for o in dirty - set(self.new) - set(self.deleted):
      if hasattr(o, 'log_json'):
        self.dirty[o] = o.log_json()

    """
    REVISIT: Update local or mem cache state that the object is marked for delete or update ONLY   
    The session.new entries are ignored
    """

  def update_cache_after_flush(self, session, flush_context):
    """
    After the flush, we know which objects were actually deleted, not just
    modified (deletes due to cascades are not known pre-flush), so fix up
    cache.
    """
    #import ipdb

    #ipdb.set_trace()

    for o in self.dirty.keys():
      # SQLAlchemy magic to determine whether object was actually deleted due
      #   to `cascade="all,delete-orphan"`
      # If an object was actually deleted, move it into `deleted`
      if flush_context.is_deleted(o._sa_instance_state):
        self.deleted[o] = self.dirty[o]
        del self.dirty[o]

    """
    Update local or mem cache 
    The session.new entries are ignored
    """
    if len(self.dirty) > 0: 
      for o, json_obj in self.dirty.items():
        cls = o.__class__.__name__
        if self.supported_classes.has_key(cls):
          print "CACHE: Updating object instance of model: " + cls + " resource type: " + self.supported_classes[cls] 

    if len(self.deleted) > 0: 
      for o, json_obj in self.deleted.items():
        cls = o.__class__.__name__
        if self.supported_classes.has_key(cls):
          print "CACHE: Deleting object instance of model: " + cls + " resource type: " + self.supported_classes[cls] 

  def clear_cache(self, session):
    self.new = {}
    self.dirty = {}
    self.deleted = {}
