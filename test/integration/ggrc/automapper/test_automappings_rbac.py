# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test automappings"""

import ddt

from ggrc.models import all_models
from integration.ggrc import TestCase
from integration.ggrc import api_helper
from integration.ggrc.access_control import acl_helper
from integration.ggrc.models import factories


@ddt.ddt
class TestAutomappings(TestCase):
  """Test automappings"""

  def setUp(self):
    super(TestAutomappings, self).setUp()
    self.api = api_helper.Api()
    # Using import for the setup for forward-compatibility with Assessment ACL
    self.import_file("issue_automapping_setup.csv")
    self.issue_admin_role = all_models.AccessControlRole.query.filter_by(
        name="Admin",
        object_type="Issue",
    ).one()

  def _login_as(self, user_email):
    """Helper function to send all further requests as given user."""
    user = all_models.Person.query.filter(
        all_models.Person.email == user_email,
    ).one()
    self.api.set_user(user)
    return user

  def _create_audit(self, program, extra_data=None):
    """Helper function to create audit for given program."""
    audit_data = {
        "title": "Some title",
        "program": {
            "id": program.id,
            "type": program.type,
        },
        "status": "Planned",
        "context": None,
    }
    if extra_data is not None:
      audit_data.update(extra_data)
    response = self.api.post(
        all_models.Audit, {"audit": audit_data}
    )
    self.assertStatus(response, 201)
    return all_models.Audit.query.get(
        response.json["audit"]["id"],
    )

  def _autogenerate_assessment(self, audit, snapshot, extra_data=None):
    """Helper function to autogenerate assessment on audit from snapshot."""
    assessment_data = {
        "_generated": True,
        "audit": {
            "id": audit.id,
            "type": audit.type,
        },
        "object": {
            "id": snapshot.id,
            "type": snapshot.type,
        },
        "context": {
            "id": audit.context.id,
            "type": audit.context.type,
        },
        "title": "Some title",
    }
    if extra_data is not None:
      assessment_data.update(extra_data)
    response = self.api.post(
        all_models.Assessment, {"assessment": assessment_data}
    )
    self.assertStatus(response, 201)
    return all_models.Assessment.query.get(
        response.json["assessment"]["id"],
    )

  def _raise_issue(self, assessment, extra_data=None):
    """Helper function to raise an issue on assessment."""
    issue_data = {
        "status": "Draft",
        "assessment": {
            "type": assessment.type,
            "id": assessment.id,
        },
        "title": "aa",
        "context": None,
    }
    if extra_data is not None:
      issue_data.update(extra_data)
    response = self.api.post(
        all_models.Issue, {"issue": issue_data}
    )
    self.assertStatus(response, 201)
    return all_models.Issue.query.get(
        response.json["issue"]["id"],
    )

  @ddt.data(
      "user@example.com",
      "Creator_and_ProgramManager@example.com",
      "Creator_and_Auditor@example.com",
      "Reader_and_ProgramManager@example.com",
      "Reader_and_Auditor@example.com",
  )
  def test_issue_audit_creator(self, user_email):
    """Test automapping issue to audit for {}.

    This test should check if the issue is automapped to an audit when a
    creator raises an issue on an assessment that belongs to the given audit.
    """
    user = all_models.Person.query.filter_by(email=user_email).one()
    self.api.set_user(user)
    assessment = all_models.Assessment.query.first()
    response = self.api.post(all_models.Issue, data=[{
        "issue": {
            "status": "Draft",
            "access_control_list": [
                acl_helper.get_acl_json(self.issue_admin_role.id, user.id)],
            "assessment": {
                "type": assessment.type,
                "id": assessment.id,
                # Fields sent by the request but not actually needed.
                # "title": "assessment",
                # "title_singular": "Assessment",
                # "table_singular": "assessment"
            },
            "title": "aa",
            "context": None,
            # Setting the context would make the test match the front-end
            # change that was reverted in 577afd6686
            # "context": {
            #     "type": assessment.context.type,
            #     "id": assessment.context.id,
            # },
        }
    }])
    self.assert200(response)
    issue = all_models.Issue.query.first()
    audit = all_models.Audit.query.first()
    relationship = all_models.Relationship.find_related(issue, audit)
    self.assertIsNotNone(relationship)
    self.assertEqual(audit.context_id, issue.context_id)
