# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Tests for assessment service handle."""
import random

from ddt import data, ddt

from integration.ggrc.models import factories
from integration.ggrc.services.test_query.test_basic import (
    BaseQueryAPITestCase
)


@ddt
class TestCollection(BaseQueryAPITestCase):

  """Test for collection assessment objects."""

  def setUp(self):
    super(TestCollection, self).setUp()
    self.clear_data()
    self.expected_ids = []
    assessments = [factories.AssessmentFactory() for _ in range(10)]
    random.shuffle(assessments)
    for idx, assessment in enumerate(assessments):
      comment = factories.CommentFactory(description=str(idx))
      factories.RelationshipFactory(source=assessment, destination=comment)
      self.expected_ids.append(assessment.id)

  @data(True, False)
  def test_order_by_test(self, desc):
    """Order by fultext attr"""
    query = self._make_query_dict(
        "Assessment", order_by=[{"name": "comment", "desc": desc}]
    )
    expected_ids = self.expected_ids
    if desc:
      expected_ids = expected_ids[::-1]
    results = self._get_first_result_set(query, "Assessment", "values")
    self.assertEqual(expected_ids, [i['id'] for i in results])
