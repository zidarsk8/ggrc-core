# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from os.path import abspath, dirname, join
from flask.json import dumps
from flask.json import loads

from tests.ggrc import TestCase
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
    data = [{"object_name": "Policy"}]

    response = self.client.post("/_service/export_csv",
                                data=dumps(data), headers=self.headers)
    self.assertEqual(response.status_code, 200)
    self.assertIn("Title*", response.data)
    self.assertIn("Policy", response.data)

  def test_multiple_empty_objects(self):
    data = [
        {"object_name": "Policy"},
        {"object_name": "Regulation"},
        {"object_name": "Clause"},
        {"object_name": "OrgGroup"},
        {"object_name": "Contract"},
    ]

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
    self.import_file("data_for_export_testing.csv")

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

  def test_basic_export(self):
    data = [{
        "object_name": "Program",
        "filters": {
            "relevant_filters": [[
                {"object_name": "Contract",
                 "slugs": ["contract-25", "contract-27"]},
                {"object_name": "Policy",
                 "slugs": ["policy-1"]},
            ]]
        },
        "fields": ["Code", "title", "description"],
    }]

    response = self.client.post("/_service/export_csv",
                                data=dumps(data), headers=self.headers)

    self.assertIn("contract-25", response.data)
    self.assertIn("contract-27", response.data)
    self.assertIn("cat ipsum", response.data)
    self.assertIn("prog-1", response.data)
    self.assertIn("prog-2", response.data)
    self.assertIn("prog-4", response.data)
