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
from nose.plugins.skip import SkipTest

from ggrc.models import Person
from ggrc.converters import errors
from tests.ggrc import TestCase
from tests.ggrc.generator import ObjectGenerator

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'test_csvs/')


if os.environ.get("TRAVIS", False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestBasicCsvImport(TestCase):

  def setUp(self):
    TestCase.setUp(self)
    self.generator = ObjectGenerator()
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

  def test_people_import(self):
    filename = "people_basic_import.csv"
    response = self.import_file(filename)
    self.assertEquals(5, Person.query.count())

  def test_people_import_correct_order_dry_run(self):
    filename = "people_import_correct_order.csv"
    response = self.import_file(filename, dry_run=True)
    self.assertEquals(1, Person.query.count())
    self.assertEquals(response[1]["name"], "Org Group")
    self.assertEquals(set(), set(response[1]["row_warnings"]))
    self.assertEquals(set(), set(response[1]["row_errors"]))

  def test_people_import_wrong_order_dry_run(self):
    filename = "people_import_correct_order.csv"
    filename = "people_import_wrong_order.csv"
    response = self.import_file(filename, dry_run=True)
    self.assertEquals(1, Person.query.count())
    self.assertEquals(response[1]["name"], "Org Group")
    self.assertEquals(set(), set(response[1]["row_warnings"]))
    self.assertEquals(set(), set(response[1]["row_errors"]))

  def test_people_import_correct_order(self):
    filename = "people_import_correct_order.csv"
    response = self.import_file(filename)
    self.assertEquals(5, Person.query.count())
    self.assertEquals(response[1]["name"], "Org Group")
    self.assertEquals(set(), set(response[1]["row_warnings"]))
    self.assertEquals(set(), set(response[1]["row_errors"]))

  def test_people_import_wrong_order(self):
    filename = "people_import_correct_order.csv"
    filename = "people_import_wrong_order.csv"
    response = self.import_file(filename)
    self.assertEquals(5, Person.query.count())
    self.assertEquals(response[1]["name"], "Org Group")
    self.assertEquals(set(), set(response[1]["row_warnings"]))
    self.assertEquals(set(), set(response[1]["row_errors"]))

