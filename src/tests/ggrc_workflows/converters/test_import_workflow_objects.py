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

from tests.ggrc import TestCase

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'test_csvs/')


if os.environ.get("TRAVIS", False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestWorkflowObjectsImport(TestCase):

  """
    Test imports for basic workflow objects
  """

  def setUp(self):
    TestCase.setUp(self)
    self.client.get("/login")
    pass

  def test_full_good_import_no_warnings(self):
    filename = "simple_workflow_test_no_warnings.csv"
    response = self.import_file(filename)
    messages = ("block_errors", "block_warnings", "row_errors", "row_warnings")

    broken_imports = set([
        "Control Assessment",
        "Task Group Task",
    ])

    print(json.dumps(response, indent=2, sort_keys=True))

    for block in response:
      if block["name"] in broken_imports:
        continue
      for message in messages:
        self.assertEquals(set(), set(block[message]))

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
