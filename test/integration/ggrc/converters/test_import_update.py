# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from integration.ggrc.converters import TestCase

from ggrc import models


class TestImportUpdates(TestCase):

  """ Test importing of already existing objects """

  def setUp(self):
    TestCase.setUp(self)
    self.client.get("/login")

  def test_policy_basic_update(self):
    """ Test simple policy title update """

    messages = ("block_errors", "block_warnings", "row_errors", "row_warnings")

    filename = "policy_basic_import.csv"
    response = self.import_file(filename)
    for block in response:
      for message in messages:
        self.assertEqual(set(), set(block[message]))

    policy = models.Policy.query.filter_by(slug="p1").first()
    self.assertEqual(policy.title, "some weird policy")

    filename = "policy_basic_import_update.csv"
    response = self.import_file(filename)
    for block in response:
      for message in messages:
        self.assertEqual(set(), set(block[message]))

    policy = models.Policy.query.filter_by(slug="p1").first()
    self.assertEqual(policy.title, "Edited policy")
