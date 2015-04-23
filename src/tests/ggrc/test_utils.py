# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from tests.ggrc import TestCase

from ggrc.utils import merge_dict, merge_dicts


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

    result = merge_dict(dict1, dict2)

    self.assertEquals(result["h"], 4)
    self.assertEquals(result["a"]["b"]["c"], 1)
    self.assertEquals(result["a"]["b"]["d"]["e"], 2)
    self.assertEquals(result["a"]["b"]["f"]["e"], 2)

  def test_merge_dicts(self):
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
    dict3 = {
        "a": {
            "eeb": {
                "c": 1,
                "f": {
                    "e": 2
                }
            },
            "g": 3
        },
        "h": 4
    }

    result = merge_dicts(dict1, dict2, dict3)

    self.assertIn("a", result)
    self.assertIn("h", result)
    self.assertIn("eeb", result["a"])
    self.assertIn("g", result["a"])
    self.assertIn("b", result["a"])
    self.assertIn("c", result["a"]["b"])
    self.assertIn("d", result["a"]["b"])
    self.assertIn("e", result["a"]["b"]["d"])
    self.assertEquals(result["a"]["b"]["f"]["e"], 2)
