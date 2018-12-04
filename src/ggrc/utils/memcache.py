# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Methods for working with memcache."""

import collections
import logging
import zlib

import cPickle

logger = logging.getLogger(__name__)

MEMCACHE_MAX_ITEM_SIZE = 10 ** 6 - 1


def blob_delete(cache, key):
  """Delete stored values from memcache."""
  chunk_keys = cache.get(key)
  if chunk_keys is None:
    # Keys are not set, no need to remove them.
    return True
  chunk_keys.append(key)
  return cache.delete_multi(chunk_keys)


# pylint: disable=too-many-arguments
def blob_set(cache, key, value, exp_time=0, key_prefix="", namespace=None):
  """Save object into memcache.

  Object will be compressed and pickled. If size of object bigger 10^6 bytes,
  it will be stored by parts. Maximal size that can be stored is 32 Mb.

  Returns:
      True if object was saved successfully, otherwise - False
  """
  # delete previous entity with the given key
  # in order to conserve available memcache space.
  blob_delete(cache, key)

  compressed_value = zlib.compress(cPickle.dumps(value))
  chunk_map = create_chunk_map(compressed_value, MEMCACHE_MAX_ITEM_SIZE, key)
  unset_ids = cache.set_multi(
      mapping=chunk_map,
      time=exp_time,
      key_prefix=key_prefix,
      namespace=namespace
  )

  if unset_ids:
    return False
  return cache.set(
      key,
      chunk_map.keys(),
      time=exp_time,
      namespace=namespace,
  )


def blob_get(cache, key, key_prefix="", namespace=None):
  """Load object from memcache.

  Object should be compressed and can be stored in divided state.
  """
  chunk_keys = cache.get(key, namespace=namespace)
  if chunk_keys is None:
    return None

  chunk_map = cache.get_multi(
      keys=chunk_keys,
      key_prefix=key_prefix,
      namespace=namespace
  )
  if not chunk_map:
    return None

  chunk_values = [chunk_map[chunk_key] for chunk_key in chunk_keys]
  compressed_value = ''.join(chunk_values)

  try:
    return cPickle.loads(zlib.decompress(compressed_value))
  except Exception:  # pylint: disable=broad-except
    logger.error("Failed to uncompress object from memcache")
    return None


def create_chunk_map(value, chunk_size, key_prefix):
  """Split value to several chunks of data and associate them with keys."""
  chunk_map = collections.OrderedDict()
  for pos in range(0, len(value), chunk_size):
    chunk = value[pos:pos + chunk_size]
    chunk_key = "%s:%d" % (key_prefix, pos)
    chunk_map[chunk_key] = chunk
  return chunk_map
