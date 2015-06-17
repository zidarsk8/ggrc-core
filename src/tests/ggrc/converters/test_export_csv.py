# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from os.path import abspath, dirname, join
from flask.json import dumps
from flask.json import loads

from ggrc import db
from ggrc.models import Policy
from tests.ggrc import TestCase
from tests.ggrc.converters.test_import_csv import TestBasicCsvImport
from tests.ggrc.generator import GgrcGenerator

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'test_csvs/')


class TestExportEmptyTemplate(TestCase):

  def setUp(self):
    self.client.get("/login")
    self.headers = {
        'Content-Type': 'application/json',
        "X-Requested-By": "gGRC"
    }

  def test_basic_policy_template(self):
    data = {"policy": []}

    response = self.client.post("/_service/export_csv",
                                data=dumps(data), headers=self.headers)
    self.assertEqual(response.status_code, 200)
    self.assertIn("Title*", response.data)
    self.assertIn("Policy", response.data)

  def test_multiple_empty_objects(self):
    data = {
        "policy": [],
        "regulation": [],
        "contract": [],
        "clause": [],
        "org group": [],
    }

    response = self.client.post("/_service/export_csv",
                                data=dumps(data), headers=self.headers)
    self.assertEqual(response.status_code, 200)
    self.assertIn("Title*", response.data)
    self.assertIn("Policy", response.data)
    self.assertIn("Regulation", response.data)
    self.assertIn("Contract", response.data)
    self.assertIn("Clause", response.data)
    self.assertIn("Org Group", response.data)


class TestExportWithObjects(TestCase):

  def setUp(self):
    TestCase.setUp(self)
    self.generator = GgrcGenerator()
    self.client.get("/login")
    self.headers = {
        'Content-Type': 'application/json',
        "X-Requested-By": "gGRC"
    }

  def generate_people(self, people):
    for person in people:
      self.generator.generate_person({
          "name": person,
          "email": "{}@reciprocitylabs.com".format(person),
      }, "gGRC Admin")

  def import_file(self, filename, dry_run=False):
    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {
        "X-test-only": "true" if dry_run else "false",
        "X-requested-by": "gGRC",
    }
    response = self.client.post("/_service/import_csv",
                                data=data, headers=headers)
    self.assertEqual(response.status_code, 200)
    return loads(response.data)

  def test_basic_policy_export(self):
    """
    importing:

      ,"p1",some weird policy,user@example.com,Draft
      ,p2,another weird policy,user@example.com,Draft
      ,,Who let the dogs out,user@example.com,Draft

    """
    self.import_file("policy_basic_import.csv")

    id_tuples = db.session.query(Policy.id).all()
    policy_ids = [pid for (pid,) in id_tuples]

    data = {
        "policy": policy_ids,
    }

    response = self.client.post("/_service/export_csv",
                                data=dumps(data), headers=self.headers)

    print response.data
    self.assertIn("some weird policy", response.data)
    self.assertIn("p2", response.data)
    self.assertIn("another weird policy", response.data)
