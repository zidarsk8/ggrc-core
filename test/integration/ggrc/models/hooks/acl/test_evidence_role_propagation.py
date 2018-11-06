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
  def test_assessment_role_propagation_edit(self, role):
    """Asses user with role '{0}' should be able to edit related evidence"""

    _, reader = self.generator.generate_person(user_role="Creator")
    assignees_role = all_models.AccessControlRole.query.filter_by(
        object_type=all_models.Assessment.__name__, name=role
    ).first()

    with factories.single_commit():
      assessment = factories.AssessmentFactory()
      factories.AccessControlListFactory(
          ac_role=assignees_role,
          object=assessment,
          person=reader
      )
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

  @ddt.data(
      ("Creator", "Audit Captains", 200),
      ("Creator", "Auditors", 403),
      ("Reader", "Audit Captains", 200),
      ("Reader", "Auditors", 403),
      ("Editor", "Audit Captains", 200),
      ("Editor", "Auditors", 200),
  )
  @ddt.unpack
  def test_audit_role_propagation_edit(self, user_role, audit_role,
                                       status_code):
    """'{0}' assigned as '{1}' should get '{2}' when editing audit evidence"""
    _, user = self.generator.generate_person(user_role=user_role)
    assignees_role = all_models.AccessControlRole.query.filter_by(
        object_type=all_models.Audit.__name__, name=audit_role
    ).first()
    with factories.single_commit():
      audit = factories.AuditFactory()
      factories.AccessControlListFactory(
          ac_role=assignees_role,
          object=audit,
          person=user
      )
      evidence = factories.EvidenceFactory()
      evidence_id = evidence.id

    factories.RelationshipFactory(source=audit, destination=evidence)

    self.api.set_user(user)

    evidence = all_models.Evidence.query.get(evidence_id)
    new_description = 'new description'
    resp = self.api.modify_object(evidence, {'description': new_description})
    evidence = self.refresh_object(evidence)

    if status_code == 200:
      self.assert200(resp)
      self.assertEquals(new_description, evidence.description)
      self.assertEquals(user.id, evidence.modified_by_id)
    else:
      self.assertStatus(resp, status_code)

  def test_audit_role_propagation_not_delete(self, role="Auditors"):
    """Audit user with role Auditors can NOT delete related evidence"""

    _, reader = self.generator.generate_person(user_role="Reader")
    assignees_role = all_models.AccessControlRole.query.filter_by(
        object_type=all_models.Audit.__name__, name=role
    ).first()
    with factories.single_commit():
      audit = factories.AuditFactory()
      factories.AccessControlListFactory(
          ac_role=assignees_role,
          object=audit,
          person=reader
      )
      evidence = factories.EvidenceFactory()
      evidence_id = evidence.id

    factories.RelationshipFactory(source=audit, destination=evidence)

    self.api.set_user(reader)
    evidence = all_models.Evidence.query.get(evidence_id)

    resp = self.api.delete(evidence)
    self.assertStatus(resp, 403)
    evidence = all_models.Evidence.query.get(evidence_id)
    self.assertTrue(evidence)
