# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for WithSimilarityScore logic."""

import json

from ggrc.models import Assessment
from ggrc.models import Request
import integration.ggrc
from integration.ggrc.models import factories


# pylint: disable=super-on-old-class; TestCase is a new-style class
class TestWithSimilarityScore(integration.ggrc.TestCase):
  """Integration test suite for WithSimilarityScore functionality."""

  def setUp(self):
    super(TestWithSimilarityScore, self).setUp()
    self.client.get("/login")

    self.assessment = factories.AssessmentFactory()
    self.audit = factories.AuditFactory()
    self.control = factories.ControlFactory()
    self.regulation = factories.RegulationFactory()

    self.make_relationships(
        self.assessment, (
            self.audit,
            self.control,
            self.regulation,
        ),
    )

    self.other_assessments, self.id_weight_map = self.make_assessments()

  @staticmethod
  def make_relationships(source, destinations):
    for destination in destinations:
      factories.RelationshipFactory(
          source=source,
          destination=destination,
      )

  def make_assessments(self):
    """Create six assessments and map them to audit, control, regulation.

    Each of the created assessments is mapped to its own subset of {audit,
    control, regulation} so each of them has different similarity weight.

    Returns: the six generated assessments and their weights in a dict.
    """

    assessment_mappings = (
        (self.audit,),
        (self.control,),
        (self.regulation,),
        (self.audit, self.control),
        (self.audit, self.regulation),
        (self.control, self.regulation),
        (self.audit, self.control, self.regulation),
    )
    weights = (5, 10, 3, 15, 8, 13, 18)

    assessments = [factories.AssessmentFactory()
                   for _ in range(len(assessment_mappings))]
    for assessment, mappings in zip(assessments, assessment_mappings):
      self.make_relationships(assessment, mappings)

    id_weight_map = {assessment.id: weight
                     for assessment, weight in zip(assessments, weights)}

    return assessments, id_weight_map

  def test_get_similar_objects_weights(self):  # pylint: disable=invalid-name
    """Check weights counted for similar objects."""
    similar_objects = Assessment.get_similar_objects_query(
        id_=self.assessment.id,
        types=["Assessment"],
        threshold=0,  # to include low weights too
    ).all()

    # casting to int from Decimal to prettify the assertion method output
    id_weight_map = {obj.id: int(obj.weight) for obj in similar_objects}

    self.assertDictEqual(id_weight_map, self.id_weight_map)

  def test_similarity_for_request(self):
    """Check special case for similarity for Request by Audit."""
    request1 = factories.RequestFactory(audit_id=self.audit.id)
    request2 = factories.RequestFactory(audit_id=self.audit.id)

    self.make_relationships(request1, [self.control, self.regulation])

    requests_by_request = Request.get_similar_objects_query(
        id_=request1.id,
        types=["Request"],
        threshold=0,
    ).all()

    self.assertSetEqual(
        {(obj.type, obj.id, obj.weight) for obj in requests_by_request},
        {("Request", request2.id, 5)},
    )

    requests_by_assessment = Assessment.get_similar_objects_query(
        id_=self.assessment.id,
        types=["Request"],
        threshold=0,
    ).all()

    self.assertSetEqual(
        {(obj.type, obj.id, obj.weight) for obj in requests_by_assessment},
        {("Request", request1.id, 18),
         ("Request", request2.id, 5)},
    )

    assessments_by_request = Request.get_similar_objects_query(
        id_=request1.id,
        types=["Assessment"],
        threshold=0,
    ).all()

    other_assessments = {
        ("Assessment", assessment.id, self.id_weight_map[assessment.id])
        for assessment in self.other_assessments
    }
    self.assertSetEqual(
        {(obj.type, obj.id, obj.weight) for obj in assessments_by_request},
        {("Assessment", self.assessment.id, 18)}.union(other_assessments),
    )

  def test_get_similar_objects(self):
    """Check similar objects manually and via Query API."""
    similar_objects = Assessment.get_similar_objects_query(
        id_=self.assessment.id,
        types=["Assessment"],
    ).all()
    expected_ids = {id_ for id_, weight in self.id_weight_map.items()
                    if weight >= Assessment.similarity_options["threshold"]}

    self.assertSetEqual(
        {obj.id for obj in similar_objects},
        expected_ids,
    )

    query = [{
        "object_name": "Assessment",
        "type": "ids",
        "filters": {
            "expression": {
                "op": {"name": "similar"},
                "object_name": "Assessment",
                "ids": [str(self.assessment.id)],
            },
        },
    }]
    response = self.client.post(
        "/query",
        data=json.dumps(query),
        headers={"Content-Type": "application/json"},
    )
    self.assertSetEqual(
        set(json.loads(response.data)[0]["Assessment"]["ids"]),
        expected_ids,
    )

  def test_sort_by_similarity(self):
    """Check sorting by __similarity__ value with query API."""
    expected_ids = [id_ for id_, weight in sorted(self.id_weight_map.items(),
                                                  key=lambda item: item[1])
                    if weight >= Assessment.similarity_options["threshold"]]

    query = [{
        "object_name": "Assessment",
        "type": "ids",
        "order_by": [{"name": "__similarity__"}],
        "filters": {
            "expression": {
                "op": {"name": "similar"},
                "object_name": "Assessment",
                "ids": [str(self.assessment.id)],
            },
        },
    }]
    response = self.client.post(
        "/query",
        data=json.dumps(query),
        headers={"Content-Type": "application/json"},
    )

    # note that in our test data every similar object has a different weight;
    # the order of objects with same weight is undefined after sorting
    self.assertListEqual(
        json.loads(response.data)[0]["Assessment"]["ids"],
        expected_ids,
    )

  def test_empty_similar_results(self):
    """Check empty similarity result."""
    query = [{
        "object_name": "Assessment",
        "type": "ids",
        "filters": {
            "expression": {
                "op": {"name": "similar"},
                "object_name": "Assessment",
                "ids": ["-1"],
            },
        },
    }]
    response = self.client.post(
        "/query",
        data=json.dumps(query),
        headers={"Content-Type": "application/json"},
    )

    self.assertListEqual(
        response.json[0]["Assessment"]["ids"],
        [],
    )

  def test_invalid_sort_by_similarity(self):
    """Check sorting by __similarity__ with query API when it is impossible."""

    # no filter by similarity but order by similarity
    query = [{
        "object_name": "Assessment",
        "order_by": [{"name": "__similarity__"}],
        "filters": {"expression": {}},
    }]

    self.assert400(self.client.post(
        "/query",
        data=json.dumps(query),
        headers={"Content-Type": "application/json"},
    ))

    # filter by similarity in one query and order by similarity in another
    query = [
        {
            "object_name": "Assessment",
            "filters": {
                "expression": {
                    "op": {"name": "similar"},
                    "object_name": "Assessment",
                    "ids": [1],
                },
            },
        },
        {
            "object_name": "Assessment",
            "order_by": [{"name": "__similarity__"}],
            "filters": {"expression": {}},
        },
    ]

    self.assert400(self.client.post(
        "/query",
        data=json.dumps(query),
        headers={"Content-Type": "application/json"},
    ))
