# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import random
from tests.ggrc import TestCase

import os
from ggrc import db
from ggrc import notification
from nose.plugins.skip import SkipTest


class TestOneTimeWorkflowNotification(TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_merge_dict(self):
    dict1 = {
        "a": {
            "b": {
                "c": 1,
                "d": {
                    "e": 2
                }
            }
        }
    }
    dict2 = {
        "a": {
            "b": {
                "c": 1,
                "f": {
                    "e": 2
                }
            },
            "g": 3
        },
        "h": 4
    }

    dict1 = notification.merge_dict(dict1, dict2)

    self.assertTrue(dict1["h"] == 4)
    self.assertTrue(dict1["a"]["b"]["c"] == 1)
    self.assertTrue(dict1["a"]["b"]["d"]["e"] == 2)
    self.assertTrue(dict1["a"]["b"]["f"]["e"] == 2)
