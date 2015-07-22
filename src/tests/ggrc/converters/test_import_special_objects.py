# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import random
import os
from os.path import abspath
from os.path import dirname
from os.path import join
from flask import json

from ggrc.models import Audit
from ggrc.models import Program
from ggrc.models import Person
from ggrc_basic_permissions.models import UserRole
from tests.ggrc import TestCase

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'test_csvs/')


if os.environ.get("TRAVIS", False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestSpecialObjects(TestCase):

  """
  testing all object with special columns such as workflows, audits, sections

  """

  def setUp(self):
    TestCase.setUp(self)
    self.client.get("/login")
    pass

  def tearDown(self):
    pass

  def test_audit_imports(self):
    """ this tests if the audit gets imported with a mapped program """

    filename = "program_audit.csv"
    self.import_file(filename)
    self.assertEquals(2, Audit.query.count())
    audit = Audit.query.filter(Audit.slug == "Aud-1").first()
    program = Program.query.filter(Program.slug == "prog-1").first()
    self.assertEquals(audit.program_id, program.id)

  def test_program_roles_imports(self):
    """ this tests if the audit gets imported with a mapped program """

    filename = "program_audit.csv"
    self.import_file(filename)
    self.assertEquals(2, Program.query.count())
    program = Program.query.filter(Program.slug == "prog-1").first()
    p1_roles = UserRole.query.filter_by(context_id=program.context_id).all()
    self.assertEquals(4, len(p1_roles))
    owner_ids = [r.person_id for r in p1_roles if r.role_id == 1]
    editor_ids = [r.person_id for r in p1_roles if r.role_id == 2]
    reader_ids = [r.person_id for r in p1_roles if r.role_id == 3]
    owner_emails = [p.email for p in
                    Person.query.filter(Person.id.in_(owner_ids)).all()]
    editor_emails = [p.email for p in
                     Person.query.filter(Person.id.in_(editor_ids)).all()]
    reader_emails = [p.email for p in
                     Person.query.filter(Person.id.in_(reader_ids)).all()]
    expected_owners = set(["user1@example.com", "user11@example.com"])
    expected_editors = set(["user11@example.com"])
    expected_readers = set(["user12@example.com"])
    self.assertEqual(set(owner_emails), expected_owners)
    self.assertEqual(set(editor_emails), expected_editors)
    self.assertEqual(set(reader_emails), expected_readers)

  def import_file(self, filename, dry_run=False):
    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {
        "X-test-only": "true" if dry_run else "false",
        "X-requested-by": "gGRC",
    }
    response = self.client.post("/_service/import_csv",
                                data=data, headers=headers)
    self.assert200(response)
    return json.loads(response.data)
