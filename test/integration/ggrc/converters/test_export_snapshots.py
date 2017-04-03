# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for snapshot export."""

from integration.ggrc import TestCase


class TestExportSnapshots(TestCase):
  """Tests basic snapshot export."""

  def setUp(self):
    super(TestExportSnapshots, self).setUp()
    self.client.get("/login")
    self.headers = {
        'Content-Type': 'application/json',
        "X-Requested-By": "GGRC",
        "X-export-view": "blocks",
    }

  def test_simple_export(self):
    """Test simple empty snapshot export."""
    search_request = [{
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": "child_type",
                "op": {"name": "="},
                "right": "Control",
            },
        },
    }]
    parsed_data = self.export_parsed_csv(search_request)["Snapshot"]
    self.assertEqual(parsed_data, [])
