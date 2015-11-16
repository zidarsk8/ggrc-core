# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import unittest
import mock

from ggrc.converters import query_helper


class TestQueryHelper(unittest.TestCase):

  def test_expression_keys(self):
    """ test expression keys function

    Make sure it works with:
      empty query
      simple query
      complex query
      invalid complex query
    """
    query = mock.MagicMock()
    helper = query_helper.QueryHelper(query)

    expressions = [
        (set(), {}),
        (set(["key_1"]), {
            "left": "key_1",
            "op": {"name": "="},
            "right": "",
        }),
        (set(["key_1", "key_2"]), {
            "left": {
                "left": "key_2",
                "op": {"name": "="},
                "right": "",
            },
            "op": {"name": "AND"},
            "right": {
                "left": "key_1",
                "op": {"name": "!="},
                "right": "",
            },
        }),
        (set(), {
            "left": {
                "left": "5",
                "op": {"name": "="},
                "right": "",
            },
            "op": {"name": "="},
            "right": {
                "left": "key_1",
                "op": {"name": "!="},
                "right": "",
            },
        }),
    ]

    for expected_result, expression in expressions:
      self.assertEqual(expected_result, helper.expression_keys(expression))
