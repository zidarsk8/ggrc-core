# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from os.path import abspath, dirname, join
from flask.json import dumps

from ggrc.app import app
from tests.ggrc import TestCase

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


class TestExportSingleObject(TestCase):

  @classmethod
  def setUpClass(cls):
    TestCase.clear_data()
    cls.tc = app.test_client()
    cls.tc.get("/login")
    cls.import_file("data_for_export_testing.csv")

  @classmethod
  def import_file(cls, filename, dry_run=False):
    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {
        "X-test-only": "true" if dry_run else "false",
        "X-requested-by": "gGRC",
    }
    cls.tc.post("/_service/import_csv",
                data=data, headers=headers)

  def setUp(self):
    self.client.get("/login")
    self.headers = {
        'Content-Type': 'application/json',
        "X-Requested-By": "gGRC",
        "X-export-view": "blocks",
    }

  def export_csv(self, data):
    return self.client.post("/_service/export_csv", data=dumps(data),
                            headers=self.headers)

  def test_simple_export_query(self):
    data = [{
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "="},
                "right": "Cat ipsum 1",
            },
        },
        "fields": ["Code", "title", "description"],
    }]
    response = self.export_csv(data)
    expected = set([1])
    for i in range(1, 23):
      if i in expected:
        self.assertIn(",Cat ipsum {},".format(i), response.data)
      else:
        self.assertNotIn(",Cat ipsum {},".format(i), response.data)

    data = [{
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "~"},
                "right": "1",
            },
        },
        "fields": ["Code", "title", "description"],
    }]
    response = self.export_csv(data)
    expected = set([1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21])
    for i in range(1, 23):
      if i in expected:
        self.assertIn(",Cat ipsum {},".format(i), response.data)
      else:
        self.assertNotIn(",Cat ipsum {},".format(i), response.data)

  def test_boolean_query_parameters(self):
    data = [{
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "private",
                "op": {"name": "="},
                "right": "1",
            },
        },
        "fields": ["Code", "title", "description"],
    }]
    response = self.export_csv(data)
    expected = set([10, 17, 18, 19, 20, 21, 22])
    for i in range(1, 23):
      if i in expected:
        self.assertIn(",Cat ipsum {},".format(i), response.data)
      else:
        self.assertNotIn(",Cat ipsum {},".format(i), response.data)

  def test_and_export_query(self):
    data = [{
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": {
                    "left": "title",
                    "op": {"name": "!~"},
                    "right": "2",
                },
                "op": {"name": "AND"},
                "right": {
                    "left": "title",
                    "op": {"name": "~"},
                    "right": "1",
                },
            },
        },
        "fields": ["Code", "title", "description"],
    }]
    response = self.export_csv(data)

    expected = set([1, 10, 11, 13, 14, 15, 16, 17, 18, 19])
    for i in range(1, 23):
      if i in expected:
        self.assertIn(",Cat ipsum {},".format(i), response.data)
      else:
        self.assertNotIn(",Cat ipsum {},".format(i), response.data)

  def test_simple_relevant_query(self):
    data = [{
        "object_name": "Program",
        "filters": {
            "expression": {
                "op": {"name": "relevant"},
                "object_name": "Contract",
                "slugs": ["contract-25", "contract-40"],
            },
        },
        "fields": ["Code", "title", "description"],
    }]
    response = self.export_csv(data)

    expected = set([1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 14, 16])
    for i in range(1, 23):
      if i in expected:
        self.assertIn(",Cat ipsum {},".format(i), response.data)
      else:
        self.assertNotIn(",Cat ipsum {},".format(i), response.data)

  def test_multiple_relevant_query(self):
    data = [{
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": {
                    "op": {"name": "relevant"},
                    "object_name": "Policy",
                    "slugs": ["policy-3"],
                },
                "op": {"name": "AND"},
                "right": {
                    "op": {"name": "relevant"},
                    "object_name": "Contract",
                    "slugs": ["contract-25", "contract-40"],
                },
            },
        },
        "fields": ["Code", "title", "description"],
    }]
    response = self.export_csv(data)

    expected = set([1, 2, 4, 8, 10, 11, 13])
    for i in range(1, 23):
      if i in expected:
        self.assertIn(",Cat ipsum {},".format(i), response.data)
      else:
        self.assertNotIn(",Cat ipsum {},".format(i), response.data)


class TestExportMultipleObjects(TestCase):

  @classmethod
  def setUpClass(cls):
    TestCase.clear_data()
    cls.tc = app.test_client()
    cls.tc.get("/login")
    cls.import_file("data_for_export_testing.csv")

  @classmethod
  def import_file(cls, filename, dry_run=False):
    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {
        "X-test-only": "true" if dry_run else "false",
        "X-requested-by": "gGRC",
    }
    cls.tc.post("/_service/import_csv",
                data=data, headers=headers)

  def setUp(self):
    self.client.get("/login")
    self.headers = {
        'Content-Type': 'application/json',
        "X-Requested-By": "gGRC",
        "X-export-view": "blocks",
    }

  def export_csv(self, data):
    return self.client.post("/_service/export_csv", data=dumps(data),
                            headers=self.headers)

  def test_simple_multi_export(self):
    data = [{
        "object_name": "Program",  # prog-1
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "="},
                "right": "cat ipsum 1"
            },
        },
        "fields": ["Code", "title", "description"],
    }, {
        "object_name": "Regulation",  # regulation-9000
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "="},
                "right": "Hipster ipsum A 1"
            },
        },
        "fields": ["Code", "title", "description"],
    }]
    response = self.export_csv(data)

    self.assertIn(",Cat ipsum 1,", response.data)
    self.assertIn(",Hipster ipsum A 1,", response.data)

  def test_relevant_to_previous_export(self):
    data = [{
        "object_name": "Program",  # prog-1, prog-23
        "filters": {
            "expression": {
                "left": {
                    "left": "title",
                    "op": {"name": "="},
                    "right": "cat ipsum 1"
                },
                "op": {"name": "OR"},
                "right": {
                    "left": "title",
                    "op": {"name": "="},
                    "right": "cat ipsum 23"
                },
            },
        },
        "fields": ["Code", "title", "description"],
    }, {
        "object_name": "Contract",  # contract-25, contract-27, contract-47
        "filters": {
            "expression": {
                "op": {"name": "relevant"},
                "object_name": "__previous__",
                "ids": ["0"],
            },
        },
        "fields": ["Code", "title", "description"],
    }, {
        "object_name": "Control",  # control-3, control-4, control-5
        "filters": {
            "expression": {
                "left": {
                    "op": {"name": "relevant"},
                    "object_name": "__previous__",
                    "ids": ["0"],
                },
                "op": {"name": "AND"},
                "right": {
                    "left": {
                        "left": "code",
                        "op": {"name": "!~"},
                        "right": "1"
                    },
                    "op": {"name": "AND"},
                    "right": {
                        "left": "code",
                        "op": {"name": "!~"},
                        "right": "2"
                    },
                },
            },
        },
        "fields": ["Code", "title", "description"],
    }, {
        "object_name": "Policy",  # policy - 3, 4, 5, 15, 16
        "filters": {
            "expression": {
                "left": {
                    "op": {"name": "relevant"},
                    "object_name": "__previous__",
                    "ids": ["0"],
                },
                "op": {"name": "AND"},
                "right": {
                    "op": {"name": "relevant"},
                    "object_name": "__previous__",
                    "ids": ["2"],
                },
            },
        },
        "fields": ["Code", "title", "description"],
    }
    ]
    response = self.export_csv(data)

    # programs
    self.assertIn(",Cat ipsum 1,", response.data)
    self.assertIn(",Cat ipsum 23,", response.data)
    # contracts
    self.assertIn(",con 5,", response.data)
    self.assertIn(",con 15,", response.data)
    self.assertIn(",con 115,", response.data)
    # controls
    self.assertIn(",Startupsum 117,", response.data)
    self.assertIn(",Startupsum 118,", response.data)
    self.assertIn(",Startupsum 119,", response.data)
    # policies
    self.assertIn(",Cheese ipsum ch 7,", response.data)
    self.assertIn(",Cheese ipsum ch 8,", response.data)
    self.assertIn(",Cheese ipsum ch 9,", response.data)
    self.assertIn(",Cheese ipsum ch 19,", response.data)
    self.assertIn(",Cheese ipsum ch 20,", response.data)
