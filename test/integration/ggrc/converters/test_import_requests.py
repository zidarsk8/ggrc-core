# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc import models
from integration.ggrc import converters


class TestRequesImport(converters.TestCase):

  def setUp(self):
    """ Set up for Request test cases """
    converters.TestCase.setUp(self)
    self.client.get("/login")

  def test_request_full_no_warnings(self):
    """ Test full request import with no warnings

    CSV sheet:
      https://docs.google.com/spreadsheets/d/1Jg8jum2eQfvR3kZNVYbVKizWIGZXvfqv3yQpo2rIiD8/edit#gid=704933240&vpid=A7
    """
    filename = "request_full_no_warnings.csv"
    response = self.import_file(filename)

    messages = ("block_errors", "block_warnings", "row_errors", "row_warnings")

    for response_block in response:
      for message in messages:
        self.assertEqual(set(), set(response_block[message]))

    req = models.Request.query.filter_by(slug="Request 1").first()
    user_1 = models.Person.query.filter_by(name="user 1").first()
    related = models.Relationship.find_related(req, user_1)

    self.assertNotEqual(related, None, "User {} is not mapped to {}".format(
        user_1.email, req.slug))
