
import unittest
from testcache import TestLocalCache
from testcache  import TestCacheManager

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestLocalCache)
	unittest.TextTestRunner(verbosity=2).run(suite)

	suite = unittest.TestLoader().loadTestsFromTestCase(TestCacheManager)
	unittest.TextTestRunner(verbosity=2).run(suite)



