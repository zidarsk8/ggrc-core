# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Custom Attribute Definition validation"""

import unittest
from mock import MagicMock

from ggrc.models import all_models
from ggrc.access_control import role as acr


class TestCustomAttributeDefinition(unittest.TestCase):
  """Test Custom Attribute Definition validation"""

  def setUp(self):
    # pylint: disable=protected-access
    self.cad = all_models.CustomAttributeDefinition()
    self.cad._get_reserved_names = MagicMock(return_value=frozenset({'title'}))
    self.cad._get_global_cad_names = MagicMock(return_value={'reg url': 1})
    acr.get_custom_roles_for = MagicMock(return_value=dict())

  def test_title_with_asterisk_throws(self):
    """Test if raises if title contains * symbol"""
    with self.assertRaises(ValueError):
      title = "Title with asterisk *"
      self.cad.definition_type = "assessment_template"
      self.cad.validate_title("title", title)

  def test_map_in_title_throws(self):
    """Test if raises if title starts with 'map:'"""
    with self.assertRaises(ValueError):
      title = "map:person"
      self.cad.definition_type = "assessment_template"
      self.cad.validate_title("title", title)

  def test_unmap_in_title_throws(self):
    """Test if raises if title starts with 'unmap:'"""
    with self.assertRaises(ValueError):
      title = "unmap:assessment"
      self.cad.definition_type = "assessment_template"
      self.cad.validate_title("title", title)
