import unittest

from cache import LocalCache
import logging
import sys

class TestLocalCache(unittest.TestCase):
  localCache = None
  #log_level=logging.DEBUG
  log_level=logging.INFO
  def setUp(self):
    logging.basicConfig(level=self.log_level)
    self.local_cache = LocalCache()
    for i in range(50):
      data = {i: {'name':'control'+str(i), 'type': 'type'+str(i)}}
      entries = self.local_cache.add('collection', 'controls', data)
      if entries is not None:
        logging.debug("==> contents of cache <=== " + str(entries))

  def runTest(self):
    print "\nTest Case #1 - Get from local cache"
    filter={'ids':[1,5,10], 'attrs':['name']}
    data = self.local_cache.get('collection', 'controls', filter)
    if data is not None:
      for key, value in data.items():
        logging.info("key : %d, value : %s" %(key, value))
    else:
      logging.info("ERROR: No data found returned")

