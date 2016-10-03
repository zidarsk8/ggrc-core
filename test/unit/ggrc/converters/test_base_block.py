# -*- coding: utf-8 -*-

# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for the BlockConverter class"""

import unittest
from mock import MagicMock


class TestBlockConverter(unittest.TestCase):
  """Class for BlockConverter class' test cases."""

  def setUp(self):
    """Setups BaseBlock converter tests."""
    from ggrc.converters import base_block
    self.base_block = base_block
    self.block_converter = self.base_block.BlockConverter(None)

  # pylint: disable=invalid-name
  def setup_clean_headers_multibute_cases(self, header_names):
    """Setups mocks for clean_headers/multi_byte issues."""
    self.block_converter.get_header_names = MagicMock(
        return_value=header_names)
    self.block_converter.object_headers = MagicMock()
    self.block_converter.add_errors = MagicMock()

  # pylint: disable=invalid-name
  def test_clean_headers_no_multi_byte_symbols_in_field_name(self):
    """Tests if field name doesn't have multi-byte characters."""
    header_names = {"header_title": "title_name", "header_date": u"date_name"}
    self.setup_clean_headers_multibute_cases(header_names)
    result = self.block_converter.clean_headers(header_names.keys())
    self.assertItemsEqual(result.keys(), header_names.values())
    self.block_converter.add_errors.assert_not_called()

  # pylint: disable=invalid-name
  def test_clean_headers_multi_byte_symbols_in_unicode_field_name(self):
    """Tests if field name in unicode has multi-byte characters."""
    header_names = {"header_title": u"title_näme", "header_date": "date_name"}
    self.setup_clean_headers_multibute_cases(header_names)
    result = self.block_converter.clean_headers(header_names.keys())
    self.assertEqual(result.keys(), [])
    self.block_converter.add_errors.assert_called_once()

  # pylint: disable=invalid-name
  def test_clean_headers_multi_byte_symbols_in_ascii_field_name(self):
    """Tests if field name in ASCII has multi-byte characters.

    In such case UnicodeDecodeError exception will be raised in sources.
    """
    header_names = {"header_title": "title_näme", "header_date": "date_name"}
    self.setup_clean_headers_multibute_cases(header_names)
    result = self.block_converter.clean_headers(header_names.keys())
    self.assertEqual(result.keys(), [])
    self.block_converter.add_errors.assert_called_once()
