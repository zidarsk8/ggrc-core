# caching/memcache.py
#
# This module provides wrapper to the Google AppEngine Memcache 
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: chandramouliv@google.com
# Maintained By: chandramouliv@google.com
#


"""
    Memcache implements the remote AppEngine Memcache mechanism

"""
class MemCache(Cache):

  def __init__(self, configparam=None)
    self.config = configparam
    self.name = 'Memcache'

    # Setup Memcache

  def get_name(self):
   return self.name

  def set_config(self, configparam):
    self.config = configparam
	
  def get_config(self):
   return self.config

  def get(self, category, resource, filter): 
    # construct the Attributes for the given filter, resource and category
    # Invoke Google AppEngine mem cache API
    return None

   def add(self, category, resource, data): 
     return None

   def update(self, category, resource, data): 
     return None

   def remove(self, category, resource, data): 
     return None

   def clean(self): 
     return False
