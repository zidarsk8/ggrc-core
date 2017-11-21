# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test automappings"""


from ggrc.models import all_models
from integration.ggrc import TestCase
from integration.ggrc import api_helper


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

  def test_issue_audit_creator(self):
    """Test automapping issue to audit for a creator.

    This test should check if the issue is automapped to an audit when a
    creator raises an issue on an assessment that belongs to the given audit.
    """
    creator = all_models.Person.query.filter_by(name="creator").first()
    self.api.set_user(creator)
    assessment = all_models.Assessment.query.first()
    response = self.api.post(all_models.Issue, data=[{
        "issue": {
            "status": "Draft",
            "access_control_list": [{
                "ac_role_id": self.issue_admin_role.id,
                "person": {
                    "type": creator.type,
                    "id": creator.id
                }
            }],
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
    self.assertIsNotNone(issue)
    relationship = all_models.Relationship.find_related(issue, audit)
    self.assertIsNotNone(relationship)
    self.assertEqual(audit.context_id, issue.context_id)
