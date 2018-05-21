# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for /api/assessments endpoints."""

import ddt

from integration.ggrc.models import factories
from integration.ggrc.services import TestCase


@ddt.ddt
class TestAssessmentResource(TestCase):
  """Tests for special people api endpoints."""

  def setUp(self):
    super(TestAssessmentResource, self).setUp()
    self.client.get("/login")

  def _get_related_objects(self, assessment):
    """Helper for retrieving assessment related objects."""
    url = "/api/assessments/{}/related_objects".format(assessment.id)
    return self.client.get(url).json

  def test_object_fields(self):
    """Test that objects contain mandatory fields.

    Front-end relies on audits containing id, type, title, and
    description. This tests ensures that those fields are returned in the
    related_objects response.
    """
    with factories.single_commit():
      assessment = factories.AssessmentFactory()
      factories.IssueFactory()  # unrelated issue
      for _ in range(2):
        issue = factories.IssueFactory()
        factories.RelationshipFactory.randomize(assessment, issue)
    related_objects = self._get_related_objects(assessment)

    expected_keys = {"id", "type", "title", "description"}
    self.assertLessEqual(
        expected_keys,
        set(related_objects["Audit"].keys())
    )

  def test_fields_in_response(self):
    """Test that objects contain only expected field."""
    with factories.single_commit():
      assessment = factories.AssessmentFactory()
      factories.IssueFactory()  # unrelated issue
      for _ in range(2):
        issue = factories.IssueFactory()
        factories.RelationshipFactory.randomize(assessment, issue)

    expected_fields = {"Audit", "Comment", "Snapshot",
                       "Evidence:URL", "Evidence:FILE"}
    related_objects = self._get_related_objects(assessment)

    self.assertEqual(expected_fields, set(related_objects.keys()))
