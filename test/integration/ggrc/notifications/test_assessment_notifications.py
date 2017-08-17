# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests of assessment notifications."""

from ggrc import db
from ggrc.notifications import common
from ggrc.models import Person, Assessment, AccessControlRole
from integration.ggrc import api_helper
from integration.ggrc import TestCase
from integration.ggrc.models import factories


class TestAssessmentNotification(TestCase):
  """Tests of assessment notifications"""

  @classmethod
  def setUpClass(cls):
    """Set up test cases for all tests."""
    cls.primary_role_id = AccessControlRole.query.filter_by(
        object_type="Assessment",
        name="Primary Contacts"
    ).first().id

    cls.secondary_role_id = AccessControlRole.query.filter_by(
        object_type="Assessment",
        name="Secondary Contacts"
    ).first().id

  def setUp(self):
    super(TestAssessmentNotification, self).setUp()
    self.client.get("/login")
    self.api = api_helper.Api()
    self.auditor = Person.query.filter_by(email="user@example.com").one()
    self.api.set_user(self.auditor)
    audit = factories.AuditFactory()

    self.api.post(Assessment, {
        "assessment": {
            "title": "Assessment1",
            "context": None,
            "audit": {
                "id": audit.id,
                "type": "Audit",
            },
            "access_control_list": [{
                "person": {
                    "id": self.auditor.id,
                    "type": "Person",
                },
                "ac_role_id": self.primary_role_id,
                "context": None
            }],
            "status": "In Progress",
        }
    })

    self.assessment = Assessment.query.filter_by(title="Assessment1").one()
    auditor = Person.query.filter_by(email="user@example.com").one()
    assessment_person_rel = factories.RelationshipFactory(
        source=self.assessment,
        destination=auditor
    )

    factories.RelationshipAttrFactory(
        relationship_id=assessment_person_rel.id,
        attr_name="AssigneeType",
        attr_value="Assessor"
    )

    self.cad1 = factories.CustomAttributeDefinitionFactory(
        definition_type="assessment",
        title="ca1",
    )
    factories.CustomAttributeValueFactory(
        custom_attribute=self.cad1,
        attributable=self.assessment
    )

    self.cad2 = factories.CustomAttributeDefinitionFactory(
        definition_type="assessment",
        attribute_type="Map:Person",
        title="ca2",
    )
    factories.CustomAttributeValueFactory(
        custom_attribute=self.cad2,
        attributable=self.assessment
    )

    self.cad3 = factories.CustomAttributeDefinitionFactory(
        definition_type="assessment",
        attribute_type="Checkbox",
        title="ca3",
    )
    factories.CustomAttributeValueFactory(
        custom_attribute=self.cad3,
        attributable=self.assessment
    )

    db.engine.execute(
        """
            UPDATE notifications
               SET sent_at = NOW()
        """
    )

  def test_common_attr_change(self):
    """Test notification when common attribute value is changed"""
    response = self.api.put(self.assessment, {"test_plan": "steps"})
    self.assert200(response)

    notifs, notif_data = common.get_daily_notifications()
    updated = notif_data["user@example.com"]["assessment_updated"]
    self.assertEqual(len(notifs), 1)
    self.assertEqual(updated[self.assessment.id]["updated_fields"],
                     ["TEST PLAN"])

  def test_custom_attr_change(self):
    """Test notification when custom attribute value is changed"""
    custom_attribute_values = [{
        "custom_attribute_id": self.cad1.id,
        "attribute_value": "test value",
    }]
    response = self.api.put(self.assessment, {
        "custom_attribute_values": custom_attribute_values
    })
    self.assert200(response)

    notifs, notif_data = common.get_daily_notifications()
    updated = notif_data["user@example.com"]["assessment_updated"]
    self.assertEqual(len(notifs), 1)
    self.assertEqual(updated[self.assessment.id]["updated_fields"], ["CA1"])

  def test_person_attr_change(self):
    """Test notification when person attribute value is changed"""
    custom_attribute_values = [{
        "custom_attribute_id": self.cad2.id,
        "attribute_value": "Person:" + str(self.auditor.id),
    }]
    response = self.api.put(self.assessment, {
        "custom_attribute_values": custom_attribute_values
    })
    self.assert200(response)

    notifs, notif_data = common.get_daily_notifications()
    updated = notif_data["user@example.com"]["assessment_updated"]
    self.assertEqual(len(notifs), 1)
    self.assertEqual(
        updated[self.assessment.id]["updated_fields"], ["CA2"])

  def test_checkbox_attr_change(self):
    """Test notification when person attribute value is changed"""
    custom_attribute_values = [{
        "custom_attribute_id": self.cad3.id,
        "attribute_value": "1",
    }]
    response = self.api.put(self.assessment, {
        "custom_attribute_values": custom_attribute_values
    })
    self.assert200(response)

    notifs, notif_data = common.get_daily_notifications()
    updated = notif_data["user@example.com"]["assessment_updated"]
    self.assertEqual(len(notifs), 1)
    self.assertEqual(
        updated[self.assessment.id]["updated_fields"], ["CA3"])

  def test_access_conrol_list(self):
    """Test notification when access conrol list is changed"""
    response = self.api.put(self.assessment, {
        "access_control_list": [
            {
                "person": {
                    "id": self.auditor.id,
                    "type": "Person",
                },
                "ac_role_id": self.secondary_role_id,
                "context": None
            }],
    })
    self.assert200(response)

    notifs, notif_data = common.get_daily_notifications()
    updated = notif_data["user@example.com"]["assessment_updated"]
    self.assertEqual(len(notifs), 1)
    self.assertEqual(updated[self.assessment.id]["updated_fields"],
                     ["PRIMARY CONTACTS", "SECONDARY CONTACTS"])

  def test_multiply_updates(self):
    """Test notification for multiply updates"""
    response = self.api.put(self.assessment, {"test_plan": "steps"})
    self.assert200(response)

    response = self.api.put(self.assessment, {"title": "new title"})
    self.assert200(response)

    notifs, notif_data = common.get_daily_notifications()
    updated = notif_data["user@example.com"]["assessment_updated"]
    self.assertEqual(len(notifs), 1)
    self.assertEqual(sorted(updated[self.assessment.id]["updated_fields"]),
                     ["TEST PLAN", "TITLE"])
