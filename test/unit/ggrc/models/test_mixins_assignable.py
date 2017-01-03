# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for assignable mixin."""

import unittest

from ggrc.models.mixins.assignable import Assignable


class DummyAssignable(Assignable):

  assignees = None


class TestAssignableMixin(unittest.TestCase):
  """ Tests inclusion of correct mixins and their attributes """

  def test_get_assignees(self):
    """Test get_assignable function."""
    dummy = DummyAssignable()
    dummy.assignees = [
        ("Person 1", ("type1", "type2")),
        ("Person 2", ("type3",)),
        ("Person 3", ("type1",)),
        ("Person 4", ("type4",)),
        ("Person 5", ("type1", "type3", "type2")),
    ]

    no_filter = set(dict(dummy.get_assignees()).keys())
    assignees = set(dict(dummy.assignees).keys())
    self.assertEqual(no_filter, assignees)

    type1 = set(dict(dummy.get_assignees("type1")).keys())
    self.assertEqual(set(["Person 1", "Person 3", "Person 5"]), type1)

    type3 = set(dict(dummy.get_assignees("type3")).keys())
    self.assertEqual(set(["Person 2", "Person 5"]), type3)

    filter_list = set(dict(dummy.get_assignees(["type4", "type3"])).keys())
    self.assertEqual(set(["Person 2", "Person 4", "Person 5"]), filter_list)
