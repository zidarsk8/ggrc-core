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
    self.create_people()
    self.client.get("/login")
    pass

  def tearDown(self):
    pass

  def test_policy_basic_import(self):

    filename = "comprehensive_sheet1.csv"
    self.import_file(filename)

    # import ipdb; ipdb.set_trace()
    # from ggrc import db
    # from ggrc.models import Control
    # from ggrc.models import CustomAttributeValue
    # control = Control.query.first()
    # cav = CustomAttributeValue()
    # cav.custom_attribute_id = control.custom_attribute_definitions[0].id
    # cav.attributable_type = "Control"
    # cav.attributable_id = control.id
    # cav.attribute_value = "Control your self"
    # db.session.add(cav)
    # db.session.commit()

    # print control.title

  def create_custom_attributes(self):
    gen = self.generator.generate_custom_attribute
    gen("control", title="my custom text", mandatory=True)
    gen("program", title="my_text", mandatory=True)
    gen("program", title="my_date", attribute_type="Date")
    gen("program", title="my_date", attribute_type="Checkbox")
    gen("program", title="my_dropdown", attribute_type="Dropdown",
        options="a,b,c,d")
    # gen("program", title="my_description", attribute_type="Rich Text")

  def create_people(self):
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
    self.assert200(response)
    return json.loads(response.data)
