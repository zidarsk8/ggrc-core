# cache/config.py
#
# This module provides the implementation of configuration of cache 
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: chandramouliv@google.com
# Maintained By: chandramouliv@google.com
#

from collections import OrderedDict 

class Config:
  properties = OrderedDict()
  policies = OrderedDict()
  dtos = OrderedDict()
  cache_names = []
  policy_manager = None
  dto_manager = None

  def __init__(self, configparam=None): 
    pass

  def setProperties(self, properties):
   self.properties = properties

  def getProperties(self):
    return self.properties	

  def set_policy_manager(self, policy_manager):
    self.policy_manager = policy_manager 

  def get_policy_manager(self):
    return self.policy_manager

  def set_dto_manager(self, dto_manager):
    self.dto_manager = dto_manager

  def get_dto_manager(self):
    return self.dto_manager

  def add_policy(self, name, category, resource, policyConfig):
    return None

  def get_policy(self, name, category, resource):
    return None

  def get_all_cache(self):
    return self.cache_names

  def initialize(self):
    props = self.getProperties()

    if props.has_key('CACHEMECHANISM'):
      self.cache_names= props.get('CACHEMECHANISM').split(',')

