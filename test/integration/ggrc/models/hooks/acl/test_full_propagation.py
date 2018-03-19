# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Full propagation for all objects.

These tests just check that all ACL entries are propagated, but do not check
correct handling on different events (object creation, or deletion). Those
should be covered in a different test suite.

These tests are not full rbac tests and do not take global roles into
consideration.
"""

import collections

from ggrc import db
from ggrc.models import all_models

from integration.ggrc.models import factories
from integration.ggrc import TestCase


class TestFullPropagation(TestCase):
  """TestAuditRoleProgation"""

  CUSTOM_ROLE_OBJECTS = [
      "Program",
      "Audit",
      "Assessment",
      "Control",
      "Issue",
  ]

  def setUp(self):
    super(TestFullPropagation, self).setUp()

    self.people = {}
    with factories.single_commit():
      self._setup_custom_roles()
      self._setup_people()
      self._setup_objects()

    self.roles = collections.defaultdict(dict)
    for role in all_models.AccessControlRole.query:
      self.roles[role.object_type][role.name] = role

  def _setup_custom_roles(self):
    """Create custom roles for propagated acls."""
    for object_type in self.CUSTOM_ROLE_OBJECTS:
      factories.AccessControlRoleFactory(
          name="{} custom role".format(object_type),
          object_type=object_type,
      )

  def _setup_people(self):
    """Setup people and global roles"""
    with factories.single_commit():
      self.people = {
          "User {}".format(i): factories.PersonFactory(
              email="user_{}@example.com".format(i),
              name="User {}".format(i),
          )
          for i in range(3)
      }

  @classmethod
  def _create_relationships(cls, relationship_pairs):
    """Create relationships for all given object pairs."""
    for source, destination in relationship_pairs:
      factories.RelationshipFactory(
          source=source,
          destination=destination,
      )

  def _setup_objects(self):
    """Sets up all the objects needed by the tests"""
    audit = factories.AuditFactory(folder="0B-xyz")
    assessment1 = factories.AssessmentFactory(audit=audit)
    assessment2 = factories.AssessmentFactory(audit=audit)
    template = factories.AssessmentTemplateFactory()
    control1 = factories.ControlFactory()
    control2 = factories.ControlFactory()
    objective1 = factories.ObjectiveFactory()
    objective2 = factories.ObjectiveFactory()
    snapshots = self._create_snapshots(
        audit,
        [control1, objective1, objective2]
    )
    evidence_files = [factories.EvidenceFactory() for _ in range(6)]
    urls = [factories.UrlFactory() for _ in range(3)]
    comments = [factories.CommentFactory() for _ in range(7)]
    issue1 = factories.IssueFactory()
    issue2 = factories.IssueFactory()
    factories.ProposalFactory(
        instance=control2,
        content='{"access_control_list": {}, "fields": {"description": "e"}}',
    )
    self._create_relationships([

        (audit.program, control1),
        (audit.program, control2),
        (audit.program, objective1),
        (audit.program, objective2),
        (audit.program, urls[0]),
        (audit.program, comments[4]),
        (audit.program, template),

        (control1, evidence_files[5]),
        (control1, urls[2]),
        (control1, comments[6]),

        (audit, assessment1),
        (audit, assessment2),
        (audit, evidence_files[4]),
        (audit, issue2),

        (assessment1, issue1),
        (assessment1, snapshots[0]),
        (assessment1, evidence_files[0]),
        (assessment1, comments[0]),
        (assessment1, urls[1]),

        (assessment2, snapshots[1]),
        (assessment2, evidence_files[1]),
        (assessment2, comments[1]),

        (snapshots[0], snapshots[2]),

        (issue1, evidence_files[2]),
        (issue1, comments[2]),
        (issue1, control1),  # regular object mapped, should not propagate
        (issue1, objective1),  # regular object mapped, should not propagate

        (issue2, comments[3]),
        (issue2, evidence_files[3]),
    ])
    self.audit = audit

  def test_audit_captain(self):
    """Test propagation of audit roles.

    Rules:

        Audit Captains:
            Snapshot RU
            Relationship R
                Assessment RUD
                    Relationship R
                        Comment R
                        Document RU
                Assessment Template RUD
                Document RU
                Issue RUD
                    Relationship R
                        Comment R
                        Document RU
    """
    audit_captains = self.roles["Audit"]["Audit Captains"]

    all_models.AccessControlList(
        object=self.audit,
        person=self.people["User 2"],
        ac_role=audit_captains,
    )
    db.session.commit()
    all_models.AccessControlList(
        object=self.audit,
        person=self.people["User 1"],
        ac_role=audit_captains,
    )

  def test_role_counts(self):
    """Test correct number of propagated ACL entries.

    The ACL propagation must be independent for each person so we must check
    that propagating N ACL entries creates N times as many rows as a single
    ACL entry.

    This test verifies that the select statement works correctly when handling
    multiple entries at once
    """
    all_models.AccessControlList(
        object=self.audit,
        person=self.people["User 0"],
        ac_role=self.roles["Audit"]["Audit Captains"],
    )
    db.session.commit()

    single_propagation_count = all_models.AccessControlList.query.count()

    all_models.AccessControlList(
        object=self.audit,
        person=self.people["User 1"],
        ac_role=self.roles["Audit"]["Audit Captains"],
    )
    all_models.AccessControlList(
        object=self.audit,
        person=self.people["User 2"],
        ac_role=self.roles["Audit"]["Auditors"],
    )
    all_models.AccessControlList(
        object=self.audit,
        person=self.people["User 2"],
        ac_role=self.roles["Audit"]["Audit Captains"],
    )
    db.session.commit()
    self.assertEqual(
        all_models.AccessControlList.query.count(),
        single_propagation_count * 4,
    )

  def test_auditors(self):
    """Test propagation for auditors role.

    Rules:

        Auditors:
            Snapshot RU
            Relationship R
                Assessment RU
                    Relationship R
                        Comment R
                        Document RU
                Assessment Template R
                Comment R
                Document R
                Issue RU
                    Relationship R
                        Comment R
                        Document RU
    """

  def test_audit_custom_role(self):
    """Test propagation for custom roles on Audit."""

  def test_audit_all_roles(self):
    """Test propagation when all audit roles are added at once."""
