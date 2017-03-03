# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for integration tests for Relationship."""

import json

from integration.ggrc import TestCase
from integration.ggrc.models import factories


class TestRelationship(TestCase):
  """Integration test suite for Relationship."""

  def setUp(self):
    """Create a Person, an Assessment, prepare a Relationship json."""
    super(TestRelationship, self).setUp()

    self.client.get("/login")
    self.person = factories.PersonFactory()
    self.assessment = factories.AssessmentFactory()

  def _post_relationship(self, attr, value):
    """POST a Relationship with attr between the Person and the Assessment."""
    headers = {
        "Content-Type": "application/json",
        "X-requested-by": "GGRC",
    }
    relationship_json = [{"relationship": {
        "source": {"id": self.person.id, "type": "Person"},
        "destination": {"id": self.assessment.id, "type": "Assessment"},
        "context": {"id": None},
        "attrs": {attr: value},
    }}]
    return self.client.post("/api/relationships",
                            data=json.dumps(relationship_json),
                            headers=headers)

  def test_attrs_validation_ok(self):
    """Can create a Relationship with valid attrs."""
    response = self._post_relationship("AssigneeType", "Creator")
    self.assert200(response)

  def test_attrs_validation_invalid_attr(self):
    """Can not create a Relationship with invalid attr name."""
    response = self._post_relationship("Invalid", "Data")
    self.assert400(response)

  def test_attrs_validation_invalid_value(self):
    """Can not create a Relationship with invalid attr value."""
    response = self._post_relationship("AssigneeType", "Monkey")
    self.assert400(response)
