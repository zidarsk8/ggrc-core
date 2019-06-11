# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for pagination tests"""

import unittest

from ggrc.query import pagination


class TestPaginationHelper(unittest.TestCase):
  """Tests for pagination module"""

  def test_add_additional_sorting(self):
    """Test additional sorting"""
    order_by = pagination.add_additional_sorting([{"name": "title",
                                                   "desc": True}])
    self.assertEqual([{"name": "title", "desc": True},
                      {"name": "id", "desc": True}], order_by)

  def test_do_not_add_sorting(self):
    """We do not additional sorting if sort by id"""
    expected = [{"name": "id", "desc": True}]
    order_by = pagination.add_additional_sorting(expected)
    self.assertEqual(expected, order_by)
