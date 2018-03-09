# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for relevant operator."""

import collections

import ddt

from ggrc.models import all_models

from integration.ggrc import TestCase
from integration.ggrc.query_helper import WithQueryApi
from integration.ggrc.models import factories


@ddt.ddt
class TestRelevant(TestCase, WithQueryApi):
  """Tests for relevant queries.

  The relevant query is an extension of the related operation in the way that
  it also includes special mappings not just the relationships table.
  """

  PEOPLE = {
      "auditor": "auditor@example.com",
      "program_editor": "program_editor@example.com",
      "assignee": "assignee@example.com",
  }

  ASSESSMENT_ROLES = {
      "assignee"
  }

  def setUp(self):
    super(TestRelevant, self).setUp()
    self.client.get("/login")
    roles = collections.defaultdict(dict)
    roles_query = all_models.AccessControlRole.query.filter(
        all_models.AccessControlRole.object_type.in_([
            all_models.Assessment.__name__,
            all_models.Audit.__name__,
            all_models.Program.__name__,
        ])
    )

    for role in roles_query:
      roles[role.object_type][role.name] = role

    with factories.single_commit():
      assessment = factories.AssessmentFactory()
      factories.RelationshipFactory(
          source=assessment.audit,
          destination=assessment,
      )
      auditor = factories.PersonFactory(email=self.PEOPLE["auditor"])
      editor = factories.PersonFactory(email=self.PEOPLE["program_editor"])
      assignee = factories.PersonFactory(email=self.PEOPLE["assignee"])
      # Correct roles and propagation for a given assessment
      factories.AccessControlListFactory(
          ac_role=roles["Assessment"]["Assignees"],
          person=assignee,
          object=assessment,
      )
      factories.AccessControlListFactory(
          ac_role=roles["Audit"]["Auditors"],
          person=auditor,
          object=assessment.audit,
      )
      factories.AccessControlListFactory(
          ac_role=roles["Program"]["Program Editors"],
          person=editor,
          object=assessment.audit.program,
      )

  @ddt.data(*PEOPLE.items())
  @ddt.unpack
  def test_person_relevant(self, role, email):
    """Check that only assessment roles can see relevant assessments"""
    person = all_models.Person.query.filter(
        all_models.Person.email == email
    ).one()

    ids = self._get_first_result_set(
        {
            "object_name": "Assessment",
            "type": "ids",
            "filters": {
                "expression": {
                    "object_name": "Person",
                    "op": {"name": "relevant"},
                    "ids": [person.id]
                }
            }
        },
        "Assessment", "ids"
    )
    if role in self.ASSESSMENT_ROLES:
      self.assertEqual(len(ids), 1)
    else:
      self.assertEqual(len(ids), 0)
