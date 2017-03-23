# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for basic Block Converter."""

from collections import defaultdict

import mock
from ddt import data, ddt

from ggrc import models
from ggrc.converters import base_block
from ggrc.utils import QueryCounter
from integration.ggrc import TestCase
from integration.ggrc.models import factories


@ddt
class TestBaseBlock(TestCase):
  """Tests for BlockConverter."""
  # Protected access check is disable for testing private functions.
  # pylint: disable=protected-access

  QUERY_LIMIT = 4  # maximum number of queries allowed for building the cache

  @staticmethod
  def dd_to_dict(ddict):
    return {
        key: {
            type_: set(ids) for type_, ids in value.items()
        } for key, value in ddict.items()
    }

  @data(0, 1, 2, 4, 8)
  def test_create_mapping_cache(self, count):
    """Test creation of mapping cache for export."""
    regulations = [factories.RegulationFactory() for _ in range(count)]
    markets = [factories.MarketFactory() for _ in range(count)]
    controls = [factories.ControlFactory() for _ in range(count)]

    expected_cache = defaultdict(lambda: defaultdict(list))
    for i in range(count):
      for j in range(i):
        factories.RelationshipFactory(
            source=regulations[j] if i % 2 == 0 else markets[i],
            destination=regulations[j] if i % 2 == 1 else markets[i],
        )
        factories.RelationshipFactory(
            source=regulations[j] if i % 2 == 0 else controls[i],
            destination=regulations[j] if i % 2 == 1 else controls[i],
        )
        expected_cache[regulations[j].id]["Control"].append(
            controls[i].slug
        )
        expected_cache[regulations[j].id]["Market"].append(
            markets[i].slug
        )
    block = base_block.BlockConverter(mock.MagicMock())
    block.object_class = models.Regulation
    block.object_ids = [r.id for r in regulations]

    with QueryCounter() as counter:
      cache = block._create_mapping_cache()
      self.assertEqual(
          self.dd_to_dict(cache),
          self.dd_to_dict(expected_cache),
      )
      self.assertLess(counter.get, self.QUERY_LIMIT)
