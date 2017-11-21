# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test automappings"""


from ggrc.models import all_models
from integration.ggrc import TestCase
from integration.ggrc import generator


class TestAutomappings(TestCase):
  """Test automappings"""

  def setUp(self):
    super(TestAutomappings, self).setUp()
    self.gen = generator.ObjectGenerator()
    self.api = self.gen.api

  def test_issue_audit_crator(self):
    """Test automapping issue to audit for a creator.

    This test should check if the issue is automapped to an audit when a
    creator raises an issue on an assessment that belongs to the given audit.
    """
    # Using import for the setup for easier setting of all correct permissions
    # and users.
    self.import_file("issue_automapping_setup.csv")
    creator = all_models.Person.query.filter_by(name="creator").first()
    issue_admin_role = all_models.AccessControlRole.query.filter(
        all_models.AccessControlRole.name == "Admin",
        all_models.AccessControlRole.object_type == "Issue",
    ).one()
    self.api.set_user(creator)
    assessment = all_models.Assessment.query.first()
    response = self.api.post(all_models.Issue, data=[{
        "issue": {
            "status": "Draft",
            "custom_attribute_definitions": [],
            "custom_attributes":{},
            "access_control_list": [{
                "ac_role_id": issue_admin_role.id,
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
            "description": "",
            "test_plan": "",
            "notes": "",
            "slug": "",
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
