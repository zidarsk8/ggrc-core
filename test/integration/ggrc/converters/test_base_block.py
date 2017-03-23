# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


import mock
from collections import defaultdict

from ddt import data, ddt

from ggrc.converters import base_block
from ggrc import models

from integration.ggrc import TestCase
from integration.ggrc.models import factories


@ddt
class TestBaseBlock(TestCase):

  @staticmethod
  def dd_to_dict(ddict):
    return {k: dict(v) for k, v in ddict.items()}

  @data(0, 1, 2, 4)
  def test_create_mapping_cache(self, count):
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

    cache = block._create_mapping_cache()
    self.assertEqual(
        self.dd_to_dict(cache),
        self.dd_to_dict(expected_cache),
    )
