# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for task group task specific export."""
from integration.ggrc import TestCase


class TestMetricsImport(TestCase):
  """Test for metrics import."""

  def setUp(self):
    super(TestMetricsImport, self).setUp()
    self.client.get("/login")

  def test_metrics_import(self):
    """Test metrics import"""
    filename = "import_metrics.csv"
    response = self.import_file(filename)
    self.assertEqual(response[0]["created"], 2)
