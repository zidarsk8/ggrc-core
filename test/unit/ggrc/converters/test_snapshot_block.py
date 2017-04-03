# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Unit tests for Snapshot block converter class."""

import unittest
import mock

from ggrc.converters.snapshot_block import SnapshotBlockConverter


class TestSnapshotBlockConverter(unittest.TestCase):
  """Unit tests for Snapshot block converter."""
  # Removing protected access checks because we wish to tests even the
  # protected functions.
  # pylint: disable=protected-access

  def setUp(self):
    super(TestSnapshotBlockConverter, self).setUp()
    converter = mock.MagicMock()
    ids = []
    self.block = SnapshotBlockConverter(converter, ids)

  def test_gather_stubs(self):
    """Test _gather_stubs method."""
    snapshot_mock1 = mock.MagicMock()
    snapshot_mock1.revision.content = {
        "id": 44,
        "owners": [
            {"type": "person", "id": 1},
            {"type": "person", "id": 2},
        ],
        "contact": {"type": "person", "id": 2},
        "cavs": [
            {"cav_value": {"type": "person", "id": 3}},
            {
                "cav_value": {"type": "option", "id": 3},
                "type": "cav",
                "id": 6,
            },
        ],
        "options": [{"type": "option", "id": 1}],
    }

    snapshot_mock2 = mock.MagicMock()
    snapshot_mock2.revision.content = {
        "id": 44,
        "type": "other",
        "options": [{"type": "option", "id": 4}],
    }

    self.block.snapshots = [
        snapshot_mock1,
        snapshot_mock2,
    ]
    stubs = self.block._gather_stubs()
    self.assertEqual(
        stubs,
        {
            "person": {1, 2, 3},
            "option": {1, 3, 4},
            "other": {44},
            "cav": {6},
        }
    )

  def test_cad_name_map(self):
    """Test gathering name map for all custom attribute definitions."""
    snapshot_mock1 = mock.MagicMock()
    snapshot_mock1.revision.content = {
        "id": 44,
        "custom_attribute_definitions": [
            {"id": 1, "title": "CCC"},
            {"id": 2, "title": "BBB"},
        ],
    }

    snapshot_mock2 = mock.MagicMock()
    snapshot_mock2.revision.content = {
        "id": 45,
        "custom_attribute_definitions": [
            {"id": 1, "title": "CCC"},
            {"id": 3, "title": "AAA"},
            {"id": 4, "title": "DDD"},
        ],
    }
    self.block.snapshots = [
        snapshot_mock1,
        snapshot_mock2,
    ]
    self.assertEqual(
        self.block._cad_name_map.items(),
        [
            (3, "AAA"),
            (2, "BBB"),
            (1, "CCC"),
            (4, "DDD"),
        ]
    )

  @mock.patch("ggrc.converters.snapshot_block.models")
  @mock.patch("ggrc.converters.snapshot_block.AttributeInfo")
  def test_attribute_name_map(self, attribute_info, _):
    """Test getting attribute name map for a valid model."""
    self.block.child_type = "Dummy"
    attribute_info.gather_aliases.return_value = {
        "key_1": "BBB",
        "key_2": "DDD",
        "key_3": {"display_name": "AAA"},
        "key_4": {"display_name": "CCC"},
    }
    attribute_info.get_column_order.return_value = [
        "key_3",
        "audit",
        "key_2",
        "key_1",
        "key_4",
    ]
    self.assertEqual(
        self.block._attribute_name_map.items(),
        [
            ("key_3", "AAA"),
            ("audit", "Audit"),  # inserted snapshot attribute
            ("key_2", "DDD"),
            ("key_1", "BBB"),
            ("key_4", "CCC"),
        ]
    )

  @mock.patch("ggrc.converters.snapshot_block.models")
  def test_bad_attribute_name_map(self, models):
    """Test getting attribute name map for an invalid model."""
    self.block.child_type = "Dummy"
    models.all_models.Dummy = None
    self.assertEqual(
        self.block._attribute_name_map.items(),
        []
    )
