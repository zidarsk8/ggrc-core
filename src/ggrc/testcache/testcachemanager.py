import unittest

from ggrc.cache import CacheManager, MemCache
import json
import logging
import sys
from google.appengine.api import memcache
from google.appengine.ext import testbed

class TestCacheManager(unittest.TestCase):
  cache_manager = None
  log_level=logging.DEBUG
  testbed=None

  def setUp(self):
    self.logger=logging.getLogger('testcache')
    self.logger.setLevel(self.log_level)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_memcache_stub()

    # initialize cache manager
    self.cache_manager= CacheManager()
    self.memcache = MemCache()
    self.cache_manager.initialize(self.memcache)

    for i in range(50):
      data = {i: {'id': i, 'name':'control'+str(i), 'type': 'type'+str(i)}}
      self.cache_manager.add_collection('collection', 'controls', data)

  def tearDown(self):
    self.testbed.deactivate()
    self.memcache = None
    self.cache_manager= None

  def runTest(self):
    self.logger.info("Test Case #1: Getting data from cache with one attribute")
    filter1={'ids':[1,5,10,25,49], 'attrs':['name']}
    data = self.cache_manager.get_collection('collection', 'controls', filter1)
    self.assertTrue(data is not None and len(data) > 0 and isinstance(data, dict), "No Entries in Cache")
    for key, value in data.items():
      self.assertTrue(isinstance(value, dict), "Data returned from cache is not a dictionary") 
      name = value['name']
      self.assertTrue(isinstance(name, str), "Name attribute type is not string") 
      self.assertEqual(name, 'control' + str(key))

    filter2={'ids':[1,5,10,25,49], 'attrs':None}
    self.logger.info("Test Case #2: Getting data from cache with empty attributes")
    data = self.cache_manager.get_collection('collection', 'controls', filter2)
    self.assertTrue(data is not None and len(data) > 0 and isinstance(data, dict), "No Entries in Cache")
    for key, value in data.items():
      self.assertTrue(isinstance(value, dict), "Data returned from cache is not a dictionary") 
      name = value['name']
      self.assertTrue(isinstance(name, str), "Name attribute type is not a string") 
      self.assertEqual(name, 'control' + str(key), "Name attribute value mismatch")
      type = value['type']
      self.assertTrue(isinstance(type, str), "Type attribute type is not a string") 
      self.assertEqual(type, 'type' + str(key), "Type attribute value mismatch")
      id = value['id']
      self.assertTrue(isinstance(id, int), "ID attribute type is not a int") 
      self.assertEqual(id, key, "ID attribute value mismatch")

    self.cache_manager.clean()
    self.logger.info("Test Case #3: Clean cache and try to get data from cache")
    data = self.cache_manager.get_collection('object', 'controls', filter2)
    self.assertTrue(data is None, "Cache is not empty after cleanup")
