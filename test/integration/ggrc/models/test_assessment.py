# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from collections import OrderedDict

from ggrc.models import Assessment
from ggrc.converters import errors
from integration.ggrc import TestCase
from integration.ggrc.api_helper import Api
from integration.ggrc.models import factories


class TestAssessment(TestCase):
  # pylint: disable=invalid-name

  def setUp(self):
    super(TestAssessment, self).setUp()
    self.api = Api()

  def test_auto_slug_generation(self):
    factories.AssessmentFactory(title="Some title")
    ca = Assessment.query.first()
    self.assertEqual("ASSESSMENT-{}".format(ca.id), ca.slug)

  def test_enabling_comment_notifications_by_default(self):
    """New Assessments should have comment notifications enabled by default."""
    asmt = factories.AssessmentFactory()

    self.assertTrue(asmt.send_by_default)
    recipients = asmt.recipients.split(",") if asmt.recipients else []
    self.assertEqual(sorted(recipients), ["Assessor", "Creator", "Verifier"])

  def test_audit_changes_api(self):
    """Test that users can't change the audit mapped to an assessment."""
    audit_id = factories.AuditFactory().id
    asmt = factories.AssessmentFactory()
    correct_audit_id = asmt.audit_id
    response = self.api.put(asmt, {"audit": {"type": "Audit", "id": audit_id}})
    self.assert400(response)
    assessment = Assessment.query.first()
    self.assertEqual(assessment.audit_id, correct_audit_id)

  def test_put_no_audit_change(self):
    """Test that put requests works without audit changes"""
    factories.AuditFactory().id
    asmt = factories.AssessmentFactory()
    correct_audit_id = asmt.audit_id
    response = self.api.put(asmt, {"audit": {
        "type": "Audit", "id": correct_audit_id
    }})
    self.assert200(response)
    assessment = Assessment.query.first()
    self.assertEqual(assessment.audit_id, correct_audit_id)

  def test_audit_changes_import(self):
    """Test that users can't change the audit mapped to an assessment."""
    audit = factories.AuditFactory()
    asmt = factories.AssessmentFactory()
    correct_audit_id = asmt.audit_id
    response = self.import_data(OrderedDict([
        ("object_type", "Assessment"),
        ("Code*", asmt.slug),
        ("audit", audit.slug),
    ]))
    self._check_csv_response(response, {
        "Assessment": {
            "row_warnings": {
                errors.UNMODIFIABLE_COLUMN.format(line=3, column_name="Audit")
            }
        }
    })
    assessment = Assessment.query.first()
    self.assertEqual(assessment.audit_id, correct_audit_id)

  def test_no_audit_change_imports(self):
    """Test that imports work if audit field does not contain changes."""
    factories.AuditFactory()
    asmt = factories.AssessmentFactory()
    correct_audit_id = asmt.audit_id
    response = self.import_data(OrderedDict([
        ("object_type", "Assessment"),
        ("Code*", asmt.slug),
        ("audit", asmt.audit.slug),
    ]))
    self._check_csv_response(response, {})
    assessment = Assessment.query.first()
    self.assertEqual(assessment.audit_id, correct_audit_id)

  def test_empty_audit_import(self):
    factories.AuditFactory()
    asmt = factories.AssessmentFactory()
    correct_audit_id = asmt.audit_id
    response = self.import_data(OrderedDict([
        ("object_type", "Assessment"),
        ("Code*", asmt.slug),
        ("audit", ""),
    ]))
    self._check_csv_response(response, {})
    assessment = Assessment.query.first()
    self.assertEqual(assessment.audit_id, correct_audit_id)
