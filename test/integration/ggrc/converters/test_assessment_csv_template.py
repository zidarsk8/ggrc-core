# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests attributes order in csv file for assessments."""

from integration.ggrc import TestCase
from integration.ggrc.models import factories


class TestAssessmentCSVTemplate(TestCase):
  """Tests order of the attributes in assessment csv.

  Test suite for checking attributes order both in the
  the exported assessment csv (will be the same for
  assessment csv template).
  """

  def setUp(self):
    """Set up for test cases."""
    super(TestAssessmentCSVTemplate, self).setUp()
    self.client.get("/login")

  def test_exported_csv(self):
    """Tests attributes order in exported assessment csv."""
    factories.CustomAttributeDefinitionFactory(
        definition_type="assessment", title="GCA 1", )
    data = [{
        "object_name": "Assessment",
        "filters": {
            "expression": {},
        },
        "fields": "all",
    }]

    response = self.export_csv(data)
    self.assertEqual(response.status_code, 200)
    self.assertIn("Verifiers,Comments,Last Comment,GCA 1", response.data)

  def test_exclude_evidence_file(self):
    """Test exclude evidence file field from csv template"""
    objects = [{"object_name": "Assessment"}]
    response = self.export_csv_template(objects)
    self.assertNotIn("Evidence File", response.data)
