# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from os.path import abspath, dirname, join
from flask.json import dumps
from flask.json import loads

from tests.ggrc import TestCase
from tests.ggrc.generator import ObjectGenerator

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'test_csvs/')


class TestExportEmptyTemplate(TestCase):

  def setUp(self):
    self.client.get("/login")
    self.headers = {
        'Content-Type': 'application/json',
        "X-Requested-By": "gGRC",
        "X-export-view": "blocks",
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
    self.generator = ObjectGenerator()
    self.client.get("/login")
    self.headers = {
        'Content-Type': 'application/json',
        "X-Requested-By": "gGRC",
        "X-export-view": "blocks",
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
    }, {
        "object_name": "Contract",
        "filters": {
            "relevant_filters": [[
                {"object_name": "Program",
                 "slugs": ["prog-1", "prog2"]},
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
    self.assertIn("con 15", response.data)
    self.assertIn("con 5", response.data)

  def test_object_filters(self):
    data = [{
        "object_name": "Program",
        "filters": {
            "relevant_filters": None,
            "object_filters": {
                "expression": {
                    "left": "title",
                    "op": {"name": "~"},
                    "right": "cat ipsum 1"
                },
                "keys": ["title"],
                "order_by":{"keys": [], "order":"", "compare":None}
            }
        },
        "fields": ["Code", "title", "description"],
    }]

    response = self.client.post("/_service/export_csv",
                                data=dumps(data), headers=self.headers)

    self.assertIn("Cat ipsum 1", response.data)
    self.assertIn("Cat ipsum 11", response.data)
    self.assertIn("Cat ipsum 12", response.data)
    self.assertNotIn("Cat ipsum 2", response.data)
    self.assertNotIn("Cat ipsum 5", response.data)
    self.assertIn("prog-1", response.data)

    data = [{
        "object_name": "Program",
        "filters": {
            "relevant_filters": None,
            "object_filters": {
                "expression": {
                    "left": "title",
                    "op": {"name": "!~"},
                    "right": "1"
                },
                "keys": ["title"],
                "order_by":{"keys": [], "order":"", "compare":None}
            }
        },
        "fields": ["Code", "title", "description"],
    }]

    response = self.client.post("/_service/export_csv",
                                data=dumps(data), headers=self.headers)

    self.assertNotIn("Cat ipsum 1", response.data)
    self.assertNotIn("Cat ipsum 11", response.data)
    self.assertNotIn("Cat ipsum 12", response.data)
    self.assertIn("Cat ipsum 2", response.data)
    self.assertIn("Cat ipsum 5", response.data)

    data = [{
        "object_name": "Program",
        "filters": {
            "relevant_filters": None,
            "object_filters": {
                "expression": {
                    "left": "title",
                    "op": {"name": "="},
                    "right": "cat ipsum 1"
                },
                "keys": ["title"],
                "order_by":{"keys": [], "order":"", "compare":None}
            }
        },
        "fields": ["Code", "title", "description"],
    }]

    response = self.client.post("/_service/export_csv",
                                data=dumps(data), headers=self.headers)

    self.assertIn("Cat ipsum 1", response.data)
    self.assertNotIn("Cat ipsum 11", response.data)
    self.assertNotIn("Cat ipsum 12", response.data)
    self.assertNotIn("Cat ipsum 2", response.data)
    self.assertNotIn("Cat ipsum 5", response.data)
    self.assertIn("prog-1", response.data)

    data = [{
        "object_name": "Program",
        "filters": {
            "relevant_filters": None,
            "object_filters": {
                "expression": {
                    "left": {
                        "left": "title",
                        "op": {"name": "="},
                        "right": "cat ipsum 1"
                    },
                    "op": {"name": "OR"},
                    "right": {
                        "left": "title",
                        "op": {"name": "~"},
                        "right": "cat ipsum 2"
                    }
                },
                "keys": ["title"],
                "order_by":{"keys": [], "order":"", "compare":None}
            }
        },
        "fields": ["Code", "title", "description"],
    }]

    response = self.client.post("/_service/export_csv",
                                data=dumps(data), headers=self.headers)

    self.assertIn("Cat ipsum 1", response.data)
    self.assertIn("Cat ipsum 2", response.data)
    self.assertIn("Cat ipsum 21", response.data)
    self.assertIn("Cat ipsum 22", response.data)
    self.assertIn("Cat ipsum 23", response.data)
    self.assertNotIn("Cat ipsum 11", response.data)
    self.assertNotIn("Cat ipsum 12", response.data)
    self.assertNotIn("Cat ipsum 5", response.data)
