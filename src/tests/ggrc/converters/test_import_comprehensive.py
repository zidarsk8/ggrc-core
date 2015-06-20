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
# from ggrc.converters import errors
from tests.ggrc import TestCase
from tests.ggrc.generator import GgrcGenerator

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'test_csvs/')


if os.environ.get("TRAVIS", False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestComprehensiveSheets(TestCase):

  """
  test sheet from:
    https://docs.google.com/spreadsheets/d/1Jg8jum2eQfvR3kZNVYbVKizWIGZXvfqv3yQpo2rIiD8/edit#gid=0

  """

  def setUp(self):
    TestCase.setUp(self)
    self.generator = GgrcGenerator()
    self.create_custom_attributes()

  def test_policy_basic_import(self):

    self.generator.generate_custom_attribute(
        "policy",
        title="Custom text")
    self.generator.generate_custom_attribute(
        "policy",
        title="cuStom Mandatory Text",
        mandatory=True)

    filename = "policy_basic_custom_attributes.csv"

  def create_custom_attributes(self):
    self.generator.generate_custom_attribute(
        "control",
        title="my custom text",
        mandatory=True)
    self.generator.generate_custom_attribute(
        "policy",
        title="Custom text")
    self.client.get("/login")

  def tearDown(self):
    pass

  def create_people(self, people):
    emails = [
      "user1@ggrc.com",
      "miha@policy.com",
      "someone.else@ggrc.com",
      "another@user.com",

    ]
    for email in emails:
      self.generator.generate_person({
        "name": email.split("@")[0].title(),
        "email": email,
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

