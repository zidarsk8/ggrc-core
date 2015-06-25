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

from ggrc.models import Person
from ggrc.converters import errors
from tests.ggrc import TestCase
from tests.ggrc.generator import GgrcGenerator

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'test_csvs/')


if os.environ.get("TRAVIS", False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestBasicCsvImport(TestCase):

  def setUp(self):
    TestCase.setUp(self)
    self.generator = GgrcGenerator()
    self.client.get("/login")

  def import_file(self, filename, dry_run=False):
    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {
        "X-test-only": "true" if dry_run else "false",
        "X-requested-by": "gGRC",
    }
    response = self.client.post("/_service/import_csv",
                                data=data, headers=headers)
    self.assertEqual(response.status_code, 200)
    return json.loads(response.data)

  def test_people_import_order(self):
    filename = "people_basic_import.csv"
    response = self.import_file(filename)
    from flask import json
    print json.dumps(response, indent=2, sort_keys=True)
    self.assertEquals(5, Person.query.count())

