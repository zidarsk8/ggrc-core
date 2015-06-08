# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from os.path import abspath, dirname, join
from flask.json import dumps

from tests.ggrc import TestCase

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'example_csvs/')


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
