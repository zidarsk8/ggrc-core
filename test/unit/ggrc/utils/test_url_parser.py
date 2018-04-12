# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Unit test suite for util url_parser."""

import unittest
from ggrc.utils import url_parser


class TestUrlParser(unittest.TestCase):
  """Unittests for user generator module."""

  # pylint: disable=invalid-name

  def test_url_parser_should_wrap_raw_url(self):
    """Url parser should wrap urls (http or hhtps)."""
    test_cases = [
        "https://www.google.com/",
        "http://www.google.com/",
        "http://www.google.com"
    ]
    expected_results = [
       '<a href="https://www.google.com/">https://www.google.com/</a>',
       '<a href="http://www.google.com/">http://www.google.com/</a>',
       '<a href="http://www.google.com">http://www.google.com</a>'
        ]
    self._assert_results(test_cases, expected_results)

  def test_url_parser_should_not_wrap_links(self):
    """Url parser should not change wrapped urls."""
    test_cases = [
        '<a href="https://www.google.com/">https://www.google.com/</a>',
        '<a href="http://www.google.com/">http://www.google.com/</a>'
        ]
    self._assert_results(test_cases, test_cases)

  def test_url_parser_should_parse_mixed_urls(self):
    """ Url parser should parse a string with both
        wrapped and not wrapped urls.
    """
    test_case = 'test <a href="https://www.google.com/">' \
                'https://www.google.com/</a> link http://www.google.com/'
    expected_result = 'test <a href="https://www.google.com/">' \
        'https://www.google.com/</a> link ' \
        '<a href="http://www.google.com/">http://www.google.com/</a>'
    self._assert_results([test_case], [expected_result])

  def test_url_parser_should_parse_broken_tags(self):
    """Url parser should work with invalid tags."""
    test_cases = ["<a>https://www.google.com/", "http://www.google.com/</a>"]
    expected_result = [
        "<a>https://www.google.com/",
        '<a href="http://www.google.com/">http://www.google.com/</a></a>'
        ]
    self._assert_results(test_cases, expected_result)

  def test_url_parser_should_not_generate_exception(self):
    """Url parser should ignore None values and empty strings."""
    test_cases = [None, ""]
    expected_results = [None, ""]
    self._assert_results(test_cases, expected_results)

  def _assert_results(self, test_cases, expected_results):
    for test, expected_result in zip(test_cases, expected_results):
      self.assertEqual(url_parser.parse(test), expected_result)
