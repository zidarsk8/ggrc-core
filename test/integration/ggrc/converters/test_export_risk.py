# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

# pylint: disable=maybe-no-member, invalid-name

"""Test Risk export."""

from integration.ggrc.models import factories
from integration.ggrc import TestCase


class TestExportRisk(TestCase):
  """Basic Risk export tests."""

  def setUp(self):
    super(TestExportRisk, self).setUp()
    self.client.get("/login")

  def test_risk_export(self):
    """Test basic risk export."""
    with factories.single_commit():
      creator = factories.PersonFactory(email="risk_creator@example.com")
      risk_slug = factories.RiskFactory(created_by=creator).slug
    data = [
        {
            "object_name": "Risk",
            "filters": {
                "expression": {
                    "left": "code",
                    "op": {
                        "name": "="
                    },
                    "right": risk_slug
                }
            },
            "fields": "all"
        }
    ]
    response = self.export_csv(data)
    self.assertIn("risk_creator@example.com", response.data)
