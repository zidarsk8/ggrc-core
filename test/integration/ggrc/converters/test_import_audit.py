# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test import of Audit and mapped objects."""

from collections import OrderedDict

from ggrc.models import all_models

from integration.ggrc import TestCase
from integration.ggrc.models import factories


class TestAuditImport(TestCase):
  """Audit import test class."""

  def setUp(self):
    """Set up for Audit test cases."""
    super(TestAuditImport, self).setUp()
    self.client.get("/login")

  def test_audit_import_db_lock(self):
    """Import 2 audits one of them with control"""
    with factories.single_commit():
      program = factories.ProgramFactory()
      control = factories.ControlFactory()
      factories.RelationshipFactory(source=program, destination=control)

    response = self.import_data(*[
        OrderedDict([
            ("object_type", "Audit"),
            ("Code", ""),
            ("Title", "Audit-import-2"),
            ("State", "In Progress"),
            ("Audit Captains", "user@example.com"),
            ("Program", program.slug),
            ("map:control versions", ""),
        ]),
        OrderedDict([
            ("object_type", "Audit"),
            ("Code", ""),
            ("Title", "Audit-import-3"),
            ("State", "Planned"),
            ("Audit Captains", "user@example.com"),
            ("Program", program.slug),
            ("map:control versions", control.slug),
        ])
    ])
    self.assertEquals(2, response[0]["created"])

  def test_update_audit_with_control(self):
    """Test import of existing Audit with mapped Control Snapshot."""
    with factories.single_commit():
      program = factories.ProgramFactory()
      audit = factories.AuditFactory(program=program)
      audit_id = audit.id
      control = factories.ControlFactory()
      factories.RelationshipFactory(source=program, destination=control)
      snapshot = self._create_snapshots(audit, [control])[0]
      factories.RelationshipFactory(source=audit, destination=snapshot)

    response = self.import_data(OrderedDict([
        ("object_type", "Audit"),
        ("Code*", audit.slug),
        ("Title", "New Title"),
        ("Audit Captains", "user@example.com"),
        ("Program", program.slug),
        ("map:control versions", control.slug),
    ]))
    self._check_csv_response(response, {})
    audit = all_models.Audit.query.get(audit_id)
    self.assertEqual(audit.title, "New Title")

  def test_create_audit_with_control(self):
    """Test import of new Audit with mapped Control Snapshot."""
    with factories.single_commit():
      program = factories.ProgramFactory()
      control = factories.ControlFactory()
      factories.RelationshipFactory(source=program, destination=control)

    response = self.import_data(OrderedDict([
        ("object_type", "Audit"),
        ("Code*", ""),
        ("Title", "New Audit"),
        ("State", "Planned"),
        ("Audit Captains", "user@example.com"),
        ("Program", program.slug),
        ("map:control versions", control.slug),
    ]))
    self._check_csv_response(response, {})
    self.assertEqual(all_models.Audit.query.count(), 1)
