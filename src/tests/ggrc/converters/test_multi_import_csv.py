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

from ggrc.models import Policy
from ggrc.models import OrgGroup
from ggrc.models import Product
from tests.ggrc import TestCase
from tests.ggrc.generator import GgrcGenerator

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, "test_csvs/")


if os.environ.get("TRAVIS", False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestCsvImport(TestCase):

  def setUp(self):
    TestCase.setUp(self)
    self.generator = GgrcGenerator()
    self.client.get("/login")

  def tearDown(self):
    pass

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
    return json.loads(response.data)

  def test_multi_basic_policy_orggroup_product(self):
    self.generate_people(["miha", "predrag", "vladan", "ivan"])

    filename = "multi_basic_policy_orggroup_product.csv"
    response_json = self.import_file(filename)

    info_set = set([
        "4 org groups were inserted.",
        "4 policies were inserted.",
        "5 products were inserted.",
    ])
    self.assertEqual(info_set, set(response_json["info"]))
    self.assertEqual(set(), set(response_json["warnings"]))
    self.assertEqual(Policy.query.count(), 4)
    self.assertEqual(OrgGroup.query.count(), 4)
    self.assertEqual(Product.query.count(), 5)
