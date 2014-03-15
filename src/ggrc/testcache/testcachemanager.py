import unittest

from ggrc.cache import CacheManager, Config
from ggrc.testcache.testfactory import TestFactory
import json
import logging
import sys
from google.appengine.api import memcache
from google.appengine.ext import testbed

class TestCacheManager(unittest.TestCase):
  cache_manager = None
  config = None
  factory = None
  #log_level=logging.DEBUG
  log_level=logging.INFO
  defaultproperties={'CACHEMECHANISM':'memcache'}
  testbed=None

  def setUp(self):
    logging.basicConfig(level=self.log_level)
    self.cache_manager= CacheManager()
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_memcache_stub()

    # setup config
    self.config = Config();
    self.config.setProperties(self.defaultproperties)
    self.config.initialize()

    # setup config
    self.factory = TestFactory()

    # initialize cache manager
    self.cache_manager.set_config(self.config)
    self.cache_manager.set_factory(self.factory)
    self.cache_manager.initialize()

    for i in range(50):
      data = {i: {'name':'control'+str(i), 'type': 'type'+str(i)}}
      self.cache_manager.add_collection('collection', 'controls', data)

  def tearDown(self):
    self.testbed.activate()

  def runTest(self):
    logging.info("\nTest Case #1: Getting data from cache")
    filter1={'ids':[1,5,10], 'attrs':['name']}
    data = self.cache_manager.get_collection('collection', 'controls', filter1)
    if data is not None and len(data) > 0:
     logging.info("==> data returned form getCollection <===")
     for key, value in data.items():
      logging.info("key :%s, data:%s" %(key, value))
    else:
      logging.info("FAILED: No entries in cache")

    filter2={'ids':[1,5,10], 'attrs':None}
    logging.info("\nTest Case #2: Getting data from cache with empty attributes")
    data = self.cache_manager.get_collection('collection', 'controls', filter2)
    if data is not None and len(data) > 0:
     logging.info("==> data returned form getCollection <===")
     converted_data = {'controls_collection': {'controls': []}}
     for cachetype, cachedata in data.items():
       logging.info("cachetype:%s, cachedata:%s" %(cachetype, cachedata))
       for id, attrs in cachedata.items():
         converted_data['controls_collection']['controls'].append(attrs)
         json_data = json.dumps(converted_data)
         logging.info("JSON data: "+ json_data)
    else:
      logging.info("FAILED: No entries in cache")

    self.cache_manager.clean()
    logging.info("\nTest Case #3: Clean cache and try to get data from cache")
    data = self.cache_manager.get_collection('object', 'controls', filter2)
    if data is None:
      logging.info("==> cache must be empty: ")
    else:
      logging.info("FAILED: cache is not empty after cleanup")
