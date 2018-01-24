# -*- coding: utf-8 -*-

# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for the ggrc.notifications.notification_handlers module."""

import unittest
from datetime import datetime

from ggrc.notifications.data_handlers import as_user_time


class TestAsUserTime(unittest.TestCase):
  """Tests for the as_user_time() helper function."""
  # pylint: disable=invalid-name

  def test_converting_dst_timestamp(self):
    """Test converting timestamps in daylight saving time part of the year."""
    timestamp = datetime(2017, 6, 13, 15, 40, 37)
    result = as_user_time(timestamp)
    self.assertEqual(result, "06/13/2017 08:40:37 PDT")

  def test_converting_non_dst_timestamp(self):
    """Test converting timestamps in non-daylight saving time part of the year.
    """
    timestamp = datetime(2017, 2, 13, 15, 40, 37)
    result = as_user_time(timestamp)
    self.assertEqual(result, "02/13/2017 07:40:37 PST")
