# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test for not_empty operator."""

from ggrc.models import all_models

from integration import ggrc as test_ggrc
from integration.ggrc import factories
from integration.ggrc import api_helper
from integration.ggrc import query_helper


class TestNotEmptyRevisions(test_ggrc.TestCase, query_helper.WithQueryApi):
  """Test for correctness of `not_empty_revisions` operator."""

  @classmethod
  def setUpClass(cls):
    cls.api = api_helper.Api()

  def setUp(self):
    super(TestNotEmptyRevisions, self).setUp()
    self.client.get("/login")

  def test_not_empty_revisions(self):
    """Test `not_empty_revisions` returns revisions with changes."""
    with factories.single_commit():
      control = factories.ControlFactory()

    edits_count = 3
    for _ in range(edits_count):
      response = self.api.put(control, {})
      self.assert200(response)

    all_revisions_count = all_models.Revision.query.filter(
        all_models.Revision.resource_type == "Control",
        all_models.Revision.resource_id == control.id
    ).count()
    # Revision also is created when creating an object
    self.assertEqual(all_revisions_count, edits_count + 1)

    not_empty_revisions = self._get_first_result_set(
        {
            "object_name": "Revision",
            "type": "ids",
            "filters": {
                "expression": {
                    "op": {"name": "not_empty_revisions"},
                    "resource_type": "Control",
                    "resource_id": control.id
                }
            }
        },
        "Revision",
        "ids"
    )
    self.assertEqual(len(not_empty_revisions), 1)
