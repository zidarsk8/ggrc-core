# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Access Control Propagation for Audit Roles like
   Auditor & Audit Captains"""

from collections import defaultdict

from ggrc import db
from ggrc.models import all_models
from integration.ggrc import TestCase
from integration.ggrc.models import factories
from integration.ggrc_basic_permissions.models \
    import factories as rbac_factories


class TestAuditRoleProgation(TestCase):
  """TestAuditRoleProgation"""

  def setup_people(self):
    """Setup people and global roles"""
    creator_role = all_models.Role.query.filter(
        all_models.Role.name == 'Creator'
    ).one()

    for person in [
        ("created_captain", "createdcaptain@example.com"),
        ("created_auditor", "createdauditor@example.com"),
        ("updated_captain", "updatedcaptain@example.com"),
        ("updated_auditor", "updatedauditor@example.com"),
    ]:
      self.people[person[0]] = factories.PersonFactory(
          email=person[1])
      rbac_factories.UserRoleFactory(
          role=creator_role,
          person=self.people[person[0]]
      )

  def setup_objects(self):
    """Sets up all the objects needed by the tests"""
    objects = self.objects
    # Program
    objects['program'] = factories.ProgramFactory(title="A Program")
    # Controls
    objects['controls'] = controls = [
        factories.ControlFactory(title="My First Control"),
        factories.ControlFactory(title="My Second Control")
    ]

    # Audit
    objects['audit'] = audit = factories.AuditFactory(
        program=objects['program'],
        access_control_list=[{
            "ac_role": self.audit_roles['Auditors'],
            "person": self.people['created_auditor']
        }, {
            "ac_role": self.audit_roles['Audit Captains'],
            "person": self.people['created_captain']
        }]
    )
    # Assessment template
    objects['assessment_template'] = factories.AssessmentTemplateFactory()

    # Assessment
    objects['assessment'] = factories.AssessmentFactory(audit=audit)

    # Snapshot
    objects['snapshots'] = self._create_snapshots(audit, controls)

    # Issues
    objects['issue'] = factories.IssueFactory()

    # Comments
    objects['comment'] = factories.CommentFactory()

    # Documents
    objects['document'] = factories.DocumentFactory()

  def setup_mappings(self):
    """Sets up all the mappings needed by the tests"""
    objects = self.objects
    audit = self.objects['audit']

    # Control <-> program mappings:
    for control in objects['controls']:
      factories.RelationshipFactory(
          source=objects['program'],
          destination=control)

    # Audit mappings:
    for obj in [
        objects['assessment_template'],
        objects['assessment'],
        objects['issue']
    ]:
      factories.RelationshipFactory(
          source=audit,
          destination=obj)

    # Assessment mappings:
    for obj in [
        objects['comment'],
        objects['document']
    ]:
      factories.RelationshipFactory(
          source=objects['assessment'],
          destination=obj)

  def setUp(self):
    super(TestAuditRoleProgation, self).setUp()
    self.audit_roles = {
        role.name: role for role in all_models.AccessControlRole.query.filter(
            # Using like `Audit%` because all audit roles start with `Audit`
            # e.g. Auditors, Audit Captains, Audit Captains Mapped
            all_models.AccessControlRole.name.like("Audit%")
        ).all()
    }
    self.people = {}
    self.objects = {}
    with factories.single_commit():
      self.setup_people()
      self.setup_objects()
      self.setup_mappings()

  def test_audit_captain_handler(self):
    """Test Audit captain

    This tests hooks.acl.audit_roles.test_audit_captain_handler and makes sure
    that the roles are propagated to all mapped objects when a new audit
    captain is added
    """
    # Fetch all created Audit Captains Mapped roles:
    objects = self.objects
    audit = objects['audit']
    audit.access_control_list = [{
        "ac_role": self.audit_roles['Audit Captains'],
        "person": self.people['updated_captain']
    }, {
        "ac_role": self.audit_roles['Auditors'],
        "person": self.people['updated_auditor']
    }]
    db.session.add(audit)
    db.session.commit()

    roles_type_map = {
        self.audit_roles['Audit Captains']: defaultdict(
            lambda: self.audit_roles['Audit Captains Mapped']),
        self.audit_roles['Auditors']: defaultdict(
            lambda: self.audit_roles['Auditors Mapped'], {
                "Assessment": self.audit_roles['Auditors Assessment Mapped'],
                "Document": self.audit_roles['Auditors Document Mapped'],
                "Snapshot": self.audit_roles['Auditors Snapshot Mapped'],
                "Issue": self.audit_roles['Auditors Issue Mapped'],
            }),
    }

    for acl in audit.access_control_list:
      all_acls = all_models.AccessControlList.query.filter(
          all_models.AccessControlList.parent_id == acl.id).all()
      acl_map = {(acl.object_id, acl.object_type, acl.person): acl
                 for acl in all_acls}

      self.assertNotEqual(
          len(all_acls), 0,
          "No propagated acls created for {}".format(acl.ac_role.name))

      # Check if all objects have the Audit Captain Mapped role
      for obj in objects['snapshots'] + [
          objects['assessment'],
          objects['assessment_template'],
          objects['issue'],
          objects['document'],
          objects['comment'],
      ]:
        key = (obj.id, obj.type, acl.person)
        self.assertIn(key, acl_map)
        self.assertEqual(acl_map[key].ac_role.name,
                         roles_type_map[acl.ac_role][obj.type].name)
