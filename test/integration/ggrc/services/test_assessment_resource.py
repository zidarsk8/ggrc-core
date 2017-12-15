# Copyright (C) 2017 Google Inc.
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

  @ddt.data(0, 1, 4)
  def test_related_issues(self, related_issues_count):
    """Test that {0} related issues are returned in related_objects."""
    expected_titles = set()
    with factories.single_commit():
      assessment = factories.AssessmentFactory()
      factories.IssueFactory()  # unrelated issue
      for _ in range(related_issues_count):
        issue = factories.IssueFactory()
        expected_titles.add(issue.title)
        factories.RelationshipFactory.randomize(assessment, issue)

    related_objects = self._get_related_objects(assessment)
    self.assertIn("Issue", related_objects)

    related_issue_titles = {
        issue["title"]
        for issue in related_objects["Issue"]
    }
    self.assertEqual(related_issue_titles, expected_titles)
