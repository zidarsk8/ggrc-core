# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test blob methods for working with memcache."""

from unittest import TestCase

from appengine import base

from ggrc.utils import memcache


@base.with_memcache
class TestBlobMemcacheOperations(TestCase):
  """Test memcache blob operations."""

  def test_big_value_saving(self):
    """Test storing in memcache huge chunk of data."""
    # Create a structure with a lot of data. It should take more than 1 Mb.
    data = {"a": {"b": ["test" * 10 for _ in range(10 ** 6)]}}
    self.assertTrue(memcache.blob_set(self.memcache_client, "data", data))
    self.assertGreater(
        self.memcache_client.get_stats().get("bytes"),
        memcache.MEMCACHE_MAX_ITEM_SIZE
    )
    self.assertEqual(
        data,
        memcache.blob_get(self.memcache_client, "data")
    )
