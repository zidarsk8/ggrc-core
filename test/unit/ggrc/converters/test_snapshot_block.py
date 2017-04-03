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
