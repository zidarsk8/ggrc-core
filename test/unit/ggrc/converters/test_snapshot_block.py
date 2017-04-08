# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Unit tests for Snapshot block converter class."""

from collections import OrderedDict

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

  def test_cad_map(self):
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
        self.block._cad_map.items(),
        [
            (3, {"id": 3, "title": "AAA"}),
            (2, {"id": 2, "title": "BBB"}),
            (1, {"id": 1, "title": "CCC"}),
            (4, {"id": 4, "title": "DDD"}),
        ]
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
    attribute_info.gather_visible_aliases.return_value = {
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

  def test_get_content_string(self):
    """Test getting content for special mapped values."""
    self.block.get_value_string = lambda x: x or ""
    self.block.child_type = "Dummy Object"
    self.block._content_value_map = {
        "Dummy Object": {
            "dummy_item": {
                "stored_value_1": "User visible value 1",
                True: "Stored boolean value",
            }
        }
    }
    self.assertEqual(
        self.block.get_content_string({
            "random_item": "Random value",
        }, "random_item"),
        "Random value"
    )
    self.assertEqual(
        self.block.get_content_string({
            "dummy_item": "stored_value_1",
        }, "dummy_item"),
        "User visible value 1"
    )
    self.assertEqual(
        self.block.get_content_string({
            "dummy_item": True,
        }, "dummy_item"),
        "Stored boolean value"
    )

  def test_get_content_string_date(self):
    """Test getting content for date values."""
    self.block.get_value_string = lambda x: x or ""
    self.block.DATE_FIELDS = {
        "dummy_date"
    }
    self.assertEqual(
        self.block.get_content_string({
            "random_item": "Random value",
        }, "random_item"),
        "Random value"
    )
    self.assertEqual(
        self.block.get_content_string({"dummy_date": None}, "dummy_date"),
        ""
    )
    self.assertEqual(
        self.block.get_content_string({"dummy_date": "", }, "dummy_date"),
        ""
    )
    self.assertEqual(
        self.block.get_content_string({
            "dummy_date": "2022-02-22",
        }, "dummy_date"),
        "02/22/2022"
    )
    self.assertEqual(
        self.block.get_content_string({
            "dummy_date": "2017-04-08T17:57:09",
        }, "dummy_date"),
        "2017-04-08 17:57:09"
    )

  def test_get_value_string(self):
    """Test get value string function for all value types."""
    self.block._stub_cache = {
        "Dummy": {
            1: "AAA",
            2: "BBB",
            3: "CCC",
        },
        "Object": {
            1: "DDD",
        }
    }
    self.assertEqual(self.block.get_value_string(None), "")
    self.assertEqual(self.block.get_value_string([]), "")
    self.assertEqual(self.block.get_value_string({}), "")
    self.assertEqual(self.block.get_value_string(True), "yes")
    self.assertEqual(self.block.get_value_string(False), "no")
    self.assertEqual(self.block.get_value_string("Foo"), "Foo")
    self.assertEqual(
        self.block.get_value_string({"type": "Fake", "id": 4}),
        ""
    )
    self.assertEqual(
        self.block.get_value_string({"type": "Dummy", "id": -3}),
        ""
    )
    self.assertEqual(
        self.block.get_value_string({"type": "Dummy", "id": 1}),
        "AAA"
    )
    self.assertEqual(
        self.block.get_value_string([
            {"type": "Dummy", "id": 1},
            {"type": "Object", "id": 1},
            {"type": "Dummy", "id": 3}
        ]),
        "AAA\nDDD\nCCC"
    )

  def test_get_cav_value_string(self):
    """Test get value string function for custom attributes."""
    self.block._cad_map = OrderedDict(
        [
            (3, {"id": 3, "title": "AAA", "attribute_type": "Map:Person"}),
            (2, {"id": 2, "title": "BBB", "attribute_type": "Date"}),
            (1, {"id": 1, "title": "CCC", "attribute_type": "Checkbox"}),
            (4, {"id": 4, "title": "DDD", "attribute_type": "Map:Person"}),
            (5, {"id": 5, "title": "DDD", "attribute_type": "Text"}),
        ]
    )
    self.block._stub_cache = {
        "Person": {
            4: "user@example.com"
        }
    }

    # invalid custom attribute representations should throw errors
    with self.assertRaises(TypeError):
      self.block.get_cav_value_string("XX")
    with self.assertRaises(KeyError):
      self.block.get_cav_value_string({})

    self.assertEqual(self.block.get_cav_value_string(None), "")
    self.assertEqual(
        self.block.get_cav_value_string({
            "custom_attribute_id": 2,
            "attribute_value": "2012-05-22",
        }),
        "05/22/2012"
    )
    self.assertEqual(
        self.block.get_cav_value_string({
            "custom_attribute_id": 2,
            "attribute_value": "",
        }),
        ""
    )
    self.assertEqual(
        self.block.get_cav_value_string({
            "custom_attribute_id": 1,
            "attribute_value": True,
        }),
        "yes"
    )
    self.assertEqual(
        self.block.get_cav_value_string({
            "custom_attribute_id": 1,
            "attribute_value": "1",
        }),
        "yes"
    )
    self.assertEqual(
        self.block.get_cav_value_string({
            "custom_attribute_id": 1,
            "attribute_value": "0",
        }),
        "no"
    )
    self.assertEqual(
        self.block.get_cav_value_string({
            "custom_attribute_id": 3,
            "attribute_value": "Person",
            "attribute_object_id": 4,
        }),
        "user@example.com"
    )
    # If the original object was deleted from the system we do not store all of
    # its values in he revision. Proper thing would be to go through revisions
    # of this object and use those static values. But we do not currently
    # support that.
    self.assertEqual(
        self.block.get_cav_value_string({
            "custom_attribute_id": 3,
            "attribute_value": "Bad Option",
            "attribute_object_id": 4,
        }),
        ""
    )

  def test_obj_attr_line(self):
    """Test get object attribute CSV values."""
    self.block.get_content_string = lambda x, name: x.get(name, "")
    self.block._attribute_name_map = OrderedDict([
        ("name", "display name"),
        ("other", "other display name"),
        ("third", "third display name"),
    ])
    self.assertEqual(
        self.block._obj_attr_line({
            "name": "1",
            "third": "2",
            "other": "3",
        }),
        ["1", "3", "2"]
    )
    self.assertEqual(
        self.block._obj_attr_line({
            "name": "1",
            "third": "2",
        }),
        ["1", "", "2"]
    )

  def test_cav_attr_line(self):
    """Test get custom attribute CSV values."""
    self.block.get_cav_value_string = lambda x: (
        x.get("attribute_value") if x else ""
    )
    self.block._cad_map = OrderedDict(
        [
            (3, {"id": 3, "title": "AAA"}),
            (2, {"id": 2, "title": "BBB"}),
            (5, {"id": 5, "title": "DDD"}),
        ]
    )
    self.assertEqual(
        self.block._cav_attr_line({}),
        ["", "", ""]
    )
    self.assertEqual(
        self.block._cav_attr_line({"custom_attribute_values": []}),
        ["", "", ""]
    )
    self.assertEqual(
        self.block._cav_attr_line({
            "custom_attribute_values": [{
                "custom_attribute_id": 5,
                "attribute_value": "five",
            }, {
                "custom_attribute_id": 3,
                "attribute_value": "three",
            }]
        }),
        ["three", "", "five"]
    )
    self.assertEqual(
        self.block._cav_attr_line({
            "custom_attribute_values": [{
                "custom_attribute_id": 5,
                "attribute_value": "five",
            }, {
                "custom_attribute_id": 8,
                "attribute_value": "eight",
            }]
        }),
        ["", "", "five"]
    )

  def test_header_list(self):
    """Test snapshot export header data."""
    self.block._attribute_name_map = OrderedDict(
        [
            ("key_3", "AAA"),
            ("audit", "Audit"),  # inserted snapshot attribute
            ("key_2", "DDD"),
            ("key_1", "BBB"),
            ("key_4", "CCC"),
        ]
    )
    self.block._cad_name_map = OrderedDict(
        [
            (3, "A"),
            (2, "B"),
            (1, "C"),
            (4, "D"),
        ]
    )
    self.assertEquals(
        self.block._header_list,
        [[], ["AAA", "Audit", "DDD", "BBB", "CCC", "A", "B", "C", "D"]]
    )

  def test_body_list(self):
    """Test basic CSV body format."""
    self.block._content_line_list = lambda x: []
    self.block.snapshots = []
    self.assertEqual(self.block._body_list, [[]])
    self.block.snapshots = [1, 2, 3]
    self.assertEqual(self.block._body_list, [[], [], []])
