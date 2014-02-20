import unittest

from cache import CacheManager, Config, Factory
import json

class TestCacheManager(unittest.TestCase):
  cache_manager = None
  config = None
  factory = None
  defaultproperties={'CACHEMECHANISM':'local'}

  def setUp(self):
    self.cache_manager= CacheManager()

    # setup config
    self.config = Config();
    self.config.setProperties(self.defaultproperties)
    self.config.initialize()

    # setup config
    self.factory = Factory()

    # initialize cache manager
    self.cache_manager.set_config(self.config)
    self.cache_manager.set_factory(self.factory)
    self.cache_manager.initialize()

    for i in range(50):
      data = {i: {'name':'control'+str(i), 'type': 'type'+str(i)}}
      self.cache_manager.add_collection('object', 'controls', data)

  def runTest(self):
    print "\nTest Case #1: Getting data from cache"
    filter1={'ids':[1,5,10], 'attrs':['name']}
    data = self.cache_manager.get_collection('object', 'controls', filter1)
    if data is not None and len(data) > 0:
     print("==> data returned form getCollection <===")
     for key, value in data.items():
      print "key :%s, data:%s" %(key, value)
    else:
      print "FAILED: No entries in cache"

    filter2={'ids':[1,5,10], 'attrs':None}
    print "\nTest Case #2: Getting data from cache with empty attributes"
    data = self.cache_manager.get_collection('object', 'controls', filter2)
    if data is not None and len(data) > 0:
     print("==> data returned form getCollection <===")
     converted_data = {'controls_collection': {'controls': []}}
     for cachetype, cachedata in data.items():
       print "cachetype:%s, cachedata:%s" %(cachetype, cachedata)
       for id, attrs in cachedata.items():
         converted_data['controls_collection']['controls'].append(attrs)
         json_data = json.dumps(converted_data)
         print "JSON data: ", json_data
    else:
      print "FAILED: No entries in cache"

    self.cache_manager.clean()
    print "\nTest Case #3: Clean cache and try to get data from cache"
    data = self.cache_manager.get_collection('object', 'controls', filter2)
    print "==> cache must be empty: ", data
