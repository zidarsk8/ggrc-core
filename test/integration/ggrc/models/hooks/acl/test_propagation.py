# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Access Control Propagation for Audit Roles like
   Auditor & Audit Captains"""

from collections import defaultdict

import ddt
import sqlalchemy as sa
import flask
from sqlalchemy.orm.session import Session

from ggrc import app
from ggrc import db
from ggrc.models import all_models
from ggrc.models.hooks import acl
from ggrc.models.hooks.acl import propagation
from integration.ggrc import TestCase
from integration.ggrc.models import factories


@ddt.ddt
class TestPropagation(TestCase):
  """TestAuditRoleProgation"""

  def setUp(self):
    super(TestPropagation, self).setUp()
    sa.event.remove(Session, "after_flush", acl.after_flush)
    self.roles = defaultdict(dict)
    for role in all_models.AccessControlRole.query:
      self.roles[role.object_type][role.name] = role

  def tearDown(self):
    sa.event.listen(Session, "after_flush", acl.after_flush)

  @ddt.data(
      ("source", "destination"),
      ("destination", "source"),
  )
  def test_single_acl(self, rel_order):
    """Test propagation for a single relationship with {}.

    Test propagation of program role to audit through a relationship with both
    options for source and destination.
    """
    with factories.single_commit():
      person = factories.PersonFactory()
      audit = factories.AuditFactory()
      rel_data = {
          rel_order[0]: audit,
          rel_order[1]: audit.program,
      }
      factories.RelationshipFactory(**rel_data)
      acl_entry = factories.AccessControlListFactory(
          ac_role=self.roles["Program"]["Program Editors"],
          object=audit.program,
          person=person,
      )

    self.assertEqual(all_models.AccessControlList.query.count(), 1)
    propagation._handle_acl_step([acl_entry.id])
    db.session.commit()
    self.assertEqual(all_models.AccessControlList.query.count(), 3)

  @ddt.data(0, 2, 3)
  def test_single_acl_to_multiple(self, count):
    """Test propagation of single ACL entry to multiple children."""
    with factories.single_commit():
      person = factories.PersonFactory()
      program = factories.ProgramFactory()
      for i in range(count):
        audit = factories.AuditFactory(program=program)
        factories.RelationshipFactory(
            source=program if i % 2 == 0 else audit,
            destination=program if i % 2 == 1 else audit,
        )
      acl_entry = factories.AccessControlListFactory(
          ac_role=self.roles["Program"]["Program Editors"],
          object=program,
          person=person,
      )

    self.assertEqual(all_models.AccessControlList.query.count(), 1)
    child_ids = propagation._handle_acl_step([acl_entry.id])

    self.assertEqual(
        all_models.AccessControlList.query.count(),
        # 1 original ACL entry, 2*count for objects+relationships
        1 + count * 2
    )
    self.assertEqual(
        db.session.execute(child_ids.alias("counts").count()).scalar(),
        count,
    )

  @ddt.data(1, 2, 3)
  def test_multi_acl_to_multiple(self, people_count):
    """Test multiple ACL propagation to multiple children."""
    audit_count = 3
    program_roles = ["Program Editors", "Program Readers"]
    with factories.single_commit():
      people = [factories.PersonFactory() for _ in range(people_count)]
      program = factories.ProgramFactory()
      for i in range(audit_count):
        audit = factories.AuditFactory(program=program)
        factories.RelationshipFactory(
            source=program if i % 2 == 0 else audit,
            destination=program if i % 2 == 1 else audit,
        )
      acl_ids = []
      for person in people:
        for role_name in program_roles:
          acl_ids.append(
              factories.AccessControlListFactory(
                  ac_role=self.roles["Program"][role_name],
                  object=program,
                  person=person,
              ).id,
          )

    self.assertEqual(
        all_models.AccessControlList.query.count(),
        people_count * len(program_roles)
    )
    child_ids = propagation._handle_acl_step(acl_ids)

    self.assertEqual(
        all_models.AccessControlList.query.count(),
        len(acl_ids) + len(acl_ids) * audit_count * 2
    )
    self.assertEqual(
        db.session.execute(child_ids.alias("counts").count()).scalar(),
        audit_count * len(program_roles) * people_count
    )

  @ddt.data(1, 2, 3)
  def test_partial_acl_to_multiple(self, partial_count):
    """Test propagating only a few acl entries to multiple objects."""
    audit_count = 3
    people_count = 4
    program_roles = ["Program Editors", "Program Readers"]
    with factories.single_commit():
      people = [factories.PersonFactory() for _ in range(people_count)]
      program = factories.ProgramFactory()
      for i in range(audit_count):
        audit = factories.AuditFactory(program=program)
        factories.RelationshipFactory(
            source=program if i % 2 == 0 else audit,
            destination=program if i % 2 == 1 else audit,
        )
      acl_ids = []
      for person in people:
        for role_name in program_roles:
          acl_ids.append(
              factories.AccessControlListFactory(
                  ac_role=self.roles["Program"][role_name],
                  object=program,
                  person=person,
              ).id,
          )

    self.assertEqual(
        all_models.AccessControlList.query.count(),
        people_count * len(program_roles)
    )
    propagate_acl_ids = acl_ids[:partial_count]
    child_ids = propagation._handle_acl_step(propagate_acl_ids)

    self.assertEqual(
        all_models.AccessControlList.query.count(),
        len(acl_ids) + len(propagate_acl_ids) * audit_count * 2
    )
    self.assertEqual(
        db.session.execute(child_ids.alias("counts").count()).scalar(),
        audit_count * len(propagate_acl_ids)
    )

  def test_deep_propagation(self):
    """Test nested propagation from programs to assessments.

    Test 3 people with 2 roles on programs to propagate to assessments
    """
    audit_count = 3
    people_count = 3
    program_roles = ["Program Editors", "Program Readers"]
    with factories.single_commit():
      people = [factories.PersonFactory() for _ in range(people_count)]
      for i in range(audit_count):
        audit = factories.AuditFactory()
        assessment = factories.AssessmentFactory(audit=audit)
        factories.RelationshipFactory(
            source=audit.program if i % 2 == 0 else audit,
            destination=audit.program if i % 2 == 1 else audit,
        )
        factories.RelationshipFactory(
            source=assessment if i % 2 == 0 else audit,
            destination=assessment if i % 2 == 1 else audit,
        )
        acl_ids = []

        for person in people:
          for role_name in program_roles:
            acl_ids.append(
                factories.AccessControlListFactory(
                    ac_role=self.roles["Program"][role_name],
                    object=audit.program,
                    person=person,
                ).id,
            )

    propagation._propagate(acl_ids)

    acl = all_models.AccessControlList
    assessment_acls = acl.query.filter(
        acl.object_type == all_models.Assessment.__name__
    ).all()

    self.assertEqual(
        len(assessment_acls),
        3 * 2  # 3 people each with 2 roles on a program that should be
        # propagated
    )
    for assessment_acl in assessment_acls:
      self.assertIsNotNone(assessment_acl.parent_id)

  def test_relationship_single_layer(self):
    """Test single layer propagation through relationships.

    Test propagation of a new relationship between audit and assessment. Here
    we check that propagation happens both ways on the relationship creation.
    """

    with factories.single_commit():
      person = factories.PersonFactory()
      audit = factories.AuditFactory()
      assessment1 = factories.AssessmentFactory(audit=audit)
      assessment2 = factories.AssessmentFactory(audit=audit)

      # This is excluded from propagation to test for proper filtering
      assessment3 = factories.AssessmentFactory(audit=audit)
      factories.RelationshipFactory(
          source=assessment3,
          destination=audit,
      ).id,

      relationship_ids = [
          factories.RelationshipFactory(
              source=assessment1,
              destination=audit,
          ).id,
          factories.RelationshipFactory(
              source=audit,
              destination=assessment2,
          ).id,
      ]

      factories.AccessControlListFactory(
          ac_role=self.roles["Audit"]["Audit Captains"],
          object=audit,
          person=person,
      )
      factories.AccessControlListFactory(
          ac_role=self.roles["Assessment"]["Assignees"],
          object=assessment1,
          person=person,
      )
      factories.AccessControlListFactory(
          ac_role=self.roles["Assessment"]["Assignees"],
          object=assessment2,
          person=person,
      )

    child_ids = propagation._handle_relationship_step(relationship_ids)

    self.assertEqual(
        all_models.AccessControlList.query.count(),
        3 + 2 + 2 + 4
        # 3 Initial roles
        # 2 roles for assessment 1 propagation to relationship and audit
        # 2 roles for assessment 2 propagation to relationship and audit
        # 4 for audit role propagation to two relationships and assessments
    )
    self.assertEqual(
        db.session.execute(child_ids.alias("counts").count()).scalar(),
        4,  # audit captain to both assessments and both assignees to audit
    )

  def test_propagation_conflict(self):
    """Test propagation conflicts

    When we create a new acl entry and a new relationship in the same commit
    some roles would be propagated twice and would cause unique constraint
    errors. This test checks for the most basic such scenario.
    """
    with factories.single_commit():
      person = factories.PersonFactory()
      audit = factories.AuditFactory()
      relationship = factories.RelationshipFactory(
          source=audit,
          destination=audit.program,
      )
      acl_entry = factories.AccessControlListFactory(
          ac_role=self.roles["Program"]["Program Editors"],
          object=audit.program,
          person=person,
      )

    with app.app.app_context():
      flask.g.new_acl_ids = {acl_entry.id}
      flask.g.new_relationship_ids = {relationship.id}
      flask.g.deleted_objects = set()

      propagation.propagate()

      db.session.commit()

      # This sets 4 propagation entries because it backtracks from the audit to
      # the same relationship. This optimally the assertion should count 3 acl
      # entries but currently that is to much work to implement
      self.assertEqual(all_models.AccessControlList.query.count(), 4)
