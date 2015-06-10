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
