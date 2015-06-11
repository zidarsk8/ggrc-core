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
from ggrc.converters import errors
from tests.ggrc import TestCase

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'test_csvs/')


if os.environ.get("TRAVIS", False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestCsvImport(TestCase):

  def setUp(self):
    TestCase.setUp(self)
    self.client.get("/login")

  def tearDown(self):
    pass

  def test_policy_basic_import(self):
    filename = "policy_basic_import.csv"

    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {
        "X-test-only": "false",
        "X-requested-by": "gGRC",
    }

    response = self.client.post("/_service/import_csv",
                                data=data, headers=headers)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Policy.query.count(), 3)

  def test_policy_import_working_with_warnings_dry_run(self):
    filename = "policy_import_working_with_warnings.csv"

    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {
        "X-test-only": "true",
        "X-requested-by": "gGRC",
    }

    response = self.client.post("/_service/import_csv",
                                data=data, headers=headers)
    self.assertEqual(response.status_code, 200)
    response_json = json.loads(response.data)

    expected_warnings = set([
        errors.UNKNOWN_USER_WARNING.format(line=3, email="miha@policy.com"),
        errors.UNKNOWN_OBJECT.format(
            line=3, object_type="Program", slug="P753"),
        errors.OWNER_MISSING.format(line=4),
        errors.UNKNOWN_USER_WARNING.format(line=6, email="not@a.user"),
        errors.OWNER_MISSING.format(line=6)
    ])
    self.assertEqual(expected_warnings, set(response_json["warnings"]))
    self.assertEqual([], response_json["errors"])
    self.assertIn("4 objects will be inserted.", response_json["info"])
    self.assertIn("0 objects will be updated.", response_json["info"])
    self.assertIn("0 objects will fail.", response_json["info"])

  def test_policy_import_working_with_warnings(self):
    def test_instance(policy):
      self.assertNotEqual([], policy.owners)
      self.assertEqual("user@example.com", policy.owners[0].email)
    filename = "policy_import_working_with_warnings.csv"

    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {
        "X-test-only": "false",
        "X-requested-by": "gGRC",
    }

    response = self.client.post("/_service/import_csv",
                                data=data, headers=headers)
    self.assertEqual(response.status_code, 200)
    json.loads(response.data)

    policies = Policy.query.all()
    self.assertEqual(len(policies), 4)
    for policy in policies:
      test_instance(policy)

  def test_policy_same_titles(self):
    def test_instance(policy):
      self.assertNotEqual([], policy.owners)
      self.assertEqual("user@example.com", policy.owners[0].email)
    filename = "policy_same_titles.csv"

    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {
        "X-test-only": "false",
        "X-requested-by": "gGRC",
    }

    response = self.client.post("/_service/import_csv",
                                data=data, headers=headers)
    self.assertEqual(response.status_code, 200)
    response_json = json.loads(response.data)

    info_set = set([
        "3 objects will be inserted.",
        "0 objects will be updated.",
        "6 objects will fail.",
    ])
    self.assertEqual(info_set, set(response_json["info"]))

    expected_warnings = set([
        errors.DUPLICATE_VALUE_IN_CSV.format(
            line_list="3, 4, 6, 10, 11", column_name="Title",
            value="A title", s="s", ignore_lines="4, 6, 10, 11"),
        errors.DUPLICATE_VALUE_IN_CSV.format(
            line_list="5, 7", column_name="Title", value="A different title",
            s="", ignore_lines="7"),
        errors.DUPLICATE_VALUE_IN_CSV.format(
            line_list="8, 9, 10, 11", column_name="Code", value="code",
            s="s", ignore_lines="9, 10, 11"),
    ])
    self.assertEqual(expected_warnings, set(response_json["warnings"]))

    policies = Policy.query.all()
    self.assertEqual(len(policies), 3)
    for policy in policies:
      test_instance(policy)
