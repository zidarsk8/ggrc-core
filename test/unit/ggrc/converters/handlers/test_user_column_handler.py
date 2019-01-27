# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for the UserColumnHandler class"""

import unittest

import ddt
import mock

from ggrc.converters.handlers import handlers


@ddt.ddt
class UserColumnHandlerTestCase(unittest.TestCase):
  """Base class for UserColumnHandler tests."""

  def setUp(self):
    row_converter = mock.MagicMock()
    self.handler = handlers.UserColumnHandler(row_converter, "key")

  @ddt.data(
      ("", []),
      ("aa@a.com", ["aa@a.com"]),
      ("aa@a.com ", ["aa@a.com"]),
      ("aa@a.com,", ["aa@a.com"]),
      ("aa@a.com;", ["aa@a.com"]),
      ("aa@a.com\n", ["aa@a.com"]),
      ("   aa@a.com,,,", ["aa@a.com"]),
      ("\n\n\naa@a.com;;;", ["aa@a.com"]),
      (",;aa@a.com;\n,", ["aa@a.com"]),
      ("aa@a.com, bb@b.com ", ["aa@a.com", "bb@b.com"]),
      ("; \n \n;;;aa@a.com,\n;,;bb@b.com     \n", ["aa@a.com", "bb@b.com"]),
      ("aa@a.com\nbb@b.com;, dd@d.com; , cc@c.com", ["aa@a.com", "bb@b.com",
                                                     "cc@c.com", "dd@d.com"]),
  )
  @ddt.unpack
  def test_email_parse(self, data_to_parse, expected_result):
    """Tests multiply emails parse correctly."""
    self.handler.raw_value = data_to_parse
    # pylint: disable=protected-access
    result = self.handler._parse_raw_data_to_emails()
    self.assertEquals(result, expected_result)
