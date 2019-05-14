# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests import of comments."""

import ddt

from integration.ggrc import TestCase
from ggrc.models import Assessment


@ddt.ddt
class TestCommentsImport(TestCase):
  """Test comments import"""

  @classmethod
  def setUpClass(cls):
    TestCase.clear_data()
    cls.response1 = TestCase._import_file("import_comments.csv")
    cls.response2 = TestCase._import_file(
        "import_comments_without_assignee_roles.csv")

  def setUp(self):
    """Log in before performing queries."""
    self._check_csv_response(self.response1, {})
    self._check_csv_response(self.response2, {})
    self.client.get("/login")

  @ddt.data(("Assessment 1", ["comment", "new_comment1", "new_comment2"]),
            ("Assessment 2", ["some comment"]),
            ("Assessment 3", ["<a href=\"goooge.com\">link</a>"]),
            ("Assessment 4", ["comment1", "comment2", "comment3"]),
            ("Assessment 5", ["one;two", "three;", "four", "hello"]),
            ("Assessment 6", ["a normal comment with {} characters"]))
  @ddt.unpack
  def test_assessment_comments(self, slug, expected_comments):
    """Test assessment comments import"""
    asst = Assessment.query.filter_by(slug=slug).first()
    comments = [comment.description for comment in asst.comments]
    self.assertEqual(comments, expected_comments)
    for comment in asst.comments:
      assignee_roles = comment.assignee_type
      self.assertIn("Assignees", assignee_roles)
      self.assertIn("Creators", assignee_roles)
