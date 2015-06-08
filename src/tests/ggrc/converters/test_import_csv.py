# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import random
import os
from os.path import abspath
from os.path import dirname
from os.path import join
from nose.plugins.skip import SkipTest

from ggrc.models import CustomAttributeDefinition
from tests.ggrc.api_helper import Api
from tests.ggrc import TestCase


THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'test_csvs/')


if os.environ.get("TRAVIS", False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestCsvImport(TestCase):

  def setUp(self):
    TestCase.setUp(self)

  def tearDown(self):
    pass

  def test_valid_imports(self):
    response = self.client.get("/login")
    filename = "policy_basic_import.csv"

    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {
      "X-test-only": "false",
      "X-requested-by": "gGRC",
    }

    response = self.client.post("/_service/import_csv",
                                data=data, headers=headers)
    self.assertEqual("OK", response.data)
    self.assertEqual(response.status_code, 200)
