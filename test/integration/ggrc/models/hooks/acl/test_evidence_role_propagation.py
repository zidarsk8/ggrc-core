# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Access Control Propagation for Evidence Roles"""
import ddt


from ggrc.models import all_models
from integration.ggrc import TestCase, Api
from integration.ggrc.generator import ObjectGenerator
from integration.ggrc.models import factories


@ddt.ddt
class TestEvidenceRolePropagation(TestCase):
  """Evidence role propagation test case"""
  # pylint: disable=invalid-name

  def setUp(self):
    super(TestEvidenceRolePropagation, self).setUp()
    self.api = Api()
    self.generator = ObjectGenerator()

  # Propagation isn't work for 'Primary Contacts', 'Secondary Contacts'
  # just add them to data list to check if fix works.

  @ddt.data("Assignees", "Creators", "Verifiers")
  def test_assessment_role_propagation_edit(self, role_name):
    _, reader = self.generator.generate_person(user_role="Creator")
    with factories.single_commit():
      assessment = factories.AssessmentFactory()
      assessment.add_person_with_role_name(reader, role_name)
      evidence = factories.EvidenceFactory()
      evidence_id = evidence.id
      factories.RelationshipFactory(source=assessment, destination=evidence)

    self.api.set_user(reader)

    evidence = all_models.Evidence.query.get(evidence_id)
    new_description = 'new description'
    resp = self.api.modify_object(evidence, {'description': new_description})
    evidence = self.refresh_object(evidence)
    self.assert200(resp)
    self.assertEquals(new_description, evidence.description)
    self.assertEquals(reader.id, evidence.modified_by_id)

  @ddt.data("Audit Captains", "Auditors")
  def test_audit_role_propagation_edit(self, role_name):
    """Audit user with role '{0}' should be able to edit related evidence"""
    _, reader = self.generator.generate_person(user_role="Reader")
    with factories.single_commit():
      audit = factories.AuditFactory()
      audit.add_person_with_role_name(reader, role_name)
      evidence = factories.EvidenceFactory()
      evidence_id = evidence.id

    factories.RelationshipFactory(source=audit, destination=evidence)

    self.api.set_user(reader)

    evidence = all_models.Evidence.query.get(evidence_id)
    new_description = 'new description'
    resp = self.api.modify_object(evidence, {'description': new_description})
    evidence = self.refresh_object(evidence)
    self.assert200(resp)
    self.assertEquals(new_description, evidence.description)
    self.assertEquals(reader.id, evidence.modified_by_id)

  def test_audit_role_propagation_not_delete(self):
    """Audit user with role Auditors can NOT delete related evidence"""
    role_name = "Auditors"
    _, reader = self.generator.generate_person(user_role="Reader")
    with factories.single_commit():
      audit = factories.AuditFactory()
      audit.add_person_with_role_name(reader, role_name)
      evidence = factories.EvidenceFactory()
      evidence_id = evidence.id

    factories.RelationshipFactory(source=audit, destination=evidence)

    self.api.set_user(reader)
    evidence = all_models.Evidence.query.get(evidence_id)

    resp = self.api.delete(evidence)
    self.assertStatus(resp, 403)
    evidence = all_models.Evidence.query.get(evidence_id)
    self.assertTrue(evidence)
