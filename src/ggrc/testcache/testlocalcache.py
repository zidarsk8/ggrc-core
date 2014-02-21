import unittest

from cache import LocalCache

class TestLocalCache(unittest.TestCase):
  localCache = None
  def setUp(self):
    self.local_cache = LocalCache()
    for i in range(50):
      data = {i: {'name':'control'+str(i), 'type': 'type'+str(i)}}
      self.local_cache.add('collection', 'controls', data)
      #print "==> contents of cache <=== ", self.localCache

  def runTest(self):
    print "\nTest Case #1 - Get from local cache"
    filter={'ids':[1,5,10], 'attrs':['name']}
    data = self.local_cache.get('collection', 'controls', filter)
    if data is not None:
      for key, value in data.items():
        print("key : %d, value : %s" %(key, value))
    else:
      print("ERROR: No data found returned")

