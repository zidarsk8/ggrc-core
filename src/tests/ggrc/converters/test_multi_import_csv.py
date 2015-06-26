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
from sqlalchemy import or_, and_

from ggrc.models import Policy
from ggrc.models import OrgGroup
from ggrc.models import Product
from ggrc.models import Relationship
from ggrc.converters import errors
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

    filename = "multi_basic_policy_orggroup_product.csv"
    response_json = self.import_file(filename)

    object_counts = [(4, 0, 0), (4, 0, 0), (5, 0, 0)]
    for i, (created, updated, ignored) in enumerate(object_counts):
      self.assertEqual(created, response_json[i]["created"])
      self.assertEqual(updated, response_json[i]["updated"])
      self.assertEqual(ignored, response_json[i]["ignored"])
      self.assertEqual(set(), set(response_json[i]["row_warnings"]))

    self.assertEqual(Policy.query.count(), 4)
    self.assertEqual(OrgGroup.query.count(), 4)
    self.assertEqual(Product.query.count(), 5)

  def test_multi_basic_policy_orggroup_product_with_warnings(self):

    filename = "multi_basic_policy_orggroup_product_with_warnings.csv"
    response_json = self.import_file(filename)

    row_messages = []
    object_counts = [(3, 0, 2), (0, 0, 4), (5, 0, 2)]
    for i, (created, updated, ignored) in enumerate(object_counts):
      self.assertEqual(created, response_json[i]["created"])
      self.assertEqual(updated, response_json[i]["updated"])
      self.assertEqual(ignored, response_json[i]["ignored"])
      row_messages.extend(response_json[i]["row_warnings"])
      row_messages.extend(response_json[i]["row_errors"])

    expected_warnings = set([
        errors.DUPLICATE_VALUE_IN_CSV.format(
            line_list="5, 6", column_name="Title", value="dolor",
            s="", ignore_lines="6"),
        errors.DUPLICATE_VALUE_IN_CSV.format(
            line_list="6, 7", column_name="Code", value="p-4",
            s="", ignore_lines="7"),
        errors.DUPLICATE_VALUE_IN_CSV.format(
            line_list="21, 26", column_name="Title", value="meatloaf",
            s="", ignore_lines="26"),
        errors.DUPLICATE_VALUE_IN_CSV.format(
            line_list="21, 26, 27", column_name="Code", value="pro 1",
            s="s", ignore_lines="26, 27"),
        errors.OWNER_MISSING.format(line=26),
        errors.MISSING_COLUMN.format(line=13, column_names="owners", s=""),
        errors.MISSING_COLUMN.format(line=14, column_names="owners", s=""),
        errors.MISSING_COLUMN.format(line=15, column_names="owners", s=""),
        errors.MISSING_COLUMN.format(line=16, column_names="owners", s=""),
    ])

    self.assertEqual(expected_warnings, set(row_messages))
    self.assertEqual(Policy.query.count(), 3)
    self.assertEqual(OrgGroup.query.count(), 0)
    self.assertEqual(Product.query.count(), 5)

  def test_multi_basic_policy_orggroup_product_with_mappings(self):

    def get_relationships_for(obj):
      return Relationship.query.filter(or_(
          and_(Relationship.source_id == obj.id,
               Relationship.source_type == obj.type),
          and_(Relationship.destination_id == obj.id,
               Relationship.destination_type == obj.type),
      ))

    filename = "multi_basic_policy_orggroup_product_with_mappings.csv"
    response_json = self.import_file(filename)

    object_counts = [(4, 0, 0), (4, 0, 0), (5, 0, 0)]
    for i, (created, updated, ignored) in enumerate(object_counts):
      self.assertEqual(created, response_json[i]["created"])
      self.assertEqual(updated, response_json[i]["updated"])
      self.assertEqual(ignored, response_json[i]["ignored"])
      self.assertEqual(set(), set(response_json[i]["row_warnings"]))

    self.assertEqual(Policy.query.count(), 4)
    self.assertEqual(OrgGroup.query.count(), 4)
    self.assertEqual(Product.query.count(), 5)
    p1 = Policy.query.filter_by(slug="p-1").first()
    org1 = OrgGroup.query.filter_by(slug="org-1").first()

    self.assertEqual(get_relationships_for(p1).count(), 3)
    self.assertEqual(get_relationships_for(org1).count(), 5)

  def test_big_import_with_mappings(self):
    response = self.import_file("data_for_export_testing.csv")
    for block in response:
      self.assertEquals(set(), set(block["row_warnings"]),
                        json.dumps(block, indent=2, sort_keys=True))
      self.assertEquals(set(), set(block["row_errors"]),
                        json.dumps(block, indent=2, sort_keys=True))

  def test_big_import_with_mappings_dry_run(self):
    response = self.import_file("data_for_export_testing.csv", dry_run=True)
    for block in response:
      self.assertEquals(set(), set(block["row_warnings"]),
                        json.dumps(block, indent=2, sort_keys=True))
      self.assertEquals(set(), set(block["row_errors"]),
                        json.dumps(block, indent=2, sort_keys=True))
