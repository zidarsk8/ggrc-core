# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc.models import Audit
from ggrc.models import Program
from ggrc.models import Person
from ggrc.models import all_models
from integration.ggrc import TestCase


class TestSpecialObjects(TestCase):

  """
  testing object with special columns such as workflows, audits, requirements

  """

  def setUp(self):
    super(TestSpecialObjects, self).setUp()
    self.client.get("/login")

  def tearDown(self):
    pass

  def test_audit_imports(self):
    """ this tests if the audit gets imported with a mapped program """

    filename = "program_audit.csv"
    self.import_file(filename)
    self.assertEqual(2, Audit.query.count())
    audit = Audit.query.filter(Audit.slug == "Aud-1").first()
    program = Program.query.filter(Program.slug == "prog-1").first()
    self.assertEqual(audit.program_id, program.id)

  def test_program_roles_imports(self):
    """ this tests if the audit gets imported with a mapped program """

    self.import_file("program_audit.csv")
    self.assertEqual(2, Program.query.count())
    program = Program.query.filter(Program.slug == "prog-1").first()
    p1_acls = all_models.AccessControlList.query.filter(
        all_models.AccessControlList.object_id == program.id,
        all_models.AccessControlList.object_type == "Program").all()
    # 2 Program Managers, 1 Primary Contact, 1 Secondary Contact,
    # 1 Program Editors, 1 Program Readers
    self.assertEqual(5, len(p1_acls))
    manager_ids = [acp.person_id
                   for acl in p1_acls
                   for acp in acl.access_control_people
                   if acl.ac_role.name == "Program Managers"]
    editor_ids = [acp.person_id
                  for acl in p1_acls
                  for acp in acl.access_control_people
                  if acl.ac_role.name == "Program Editors"]
    reader_ids = [acp.person_id
                  for acl in p1_acls
                  for acp in acl.access_control_people
                  if acl.ac_role.name == "Program Readers"]
    manager_emails = [p.email for p in
                      Person.query.filter(Person.id.in_(manager_ids)).all()]
    editor_emails = [p.email for p in
                     Person.query.filter(Person.id.in_(editor_ids)).all()]
    reader_emails = [p.email for p in
                     Person.query.filter(Person.id.in_(reader_ids)).all()]
    expected_owners = set(["user1@example.com", "user11@example.com"])
    expected_editors = set(["user11@example.com"])
    expected_readers = set(["user12@example.com"])
    self.assertEqual(set(manager_emails), expected_owners)
    self.assertEqual(set(editor_emails), expected_editors)
    self.assertEqual(set(reader_emails), expected_readers)
