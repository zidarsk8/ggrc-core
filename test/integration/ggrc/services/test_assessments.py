# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Tests for assessment service handle."""
import random

from ddt import data, ddt

from ggrc.models import all_models
from integration.ggrc import TestCase
from integration.ggrc.query_helper import WithQueryApi
from integration.ggrc.models import factories
from integration.ggrc.api_helper import Api
from integration.ggrc.generator import ObjectGenerator


@ddt
class TestCollection(TestCase, WithQueryApi):

  """Test for collection assessment objects."""

  def setUp(self):
    super(TestCollection, self).setUp()
    self.client.get("/login")
    self.clear_data()
    self.expected_ids = []
    self.api = Api()
    self.generator = ObjectGenerator()
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

  @data("Assessor", "Creator", "Verifier")
  def test_delete_assessment_by_role(self, role_name):
    """Delete assessment not allowed for based on Assignee Type."""
    with factories.single_commit():
      assessment = factories.AssessmentFactory()
      context = factories.ContextFactory(related_object=assessment)
      assessment.context = context
      person = factories.PersonFactory()
      object_person_rel = factories.RelationshipFactory(
          source=assessment, destination=person)
      factories.RelationshipAttrFactory(
          relationship_id=object_person_rel.id,
          attr_name="AssigneeType",
          attr_value=role_name,
      )
    assessment_id = assessment.id
    role = all_models.Role.query.filter(
        all_models.Role.name == "Creator"
    ).first()
    self.generator.generate_user_role(person, role, context)
    self.api.set_user(person)
    assessment = all_models.Assessment.query.get(assessment_id)
    resp = self.api.delete(assessment)
    self.assert403(resp)
    self.assertTrue(all_models.Assessment.query.filter(
        all_models.Assessment.id == assessment_id).one())
