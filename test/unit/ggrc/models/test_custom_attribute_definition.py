# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Custom Attribute Definition validation"""

import unittest

from ggrc.app import app
from ggrc.models import all_models


class TestCustomAttributeDefinition(unittest.TestCase):
  """Test Custom Attribute Definition validation"""

  def setUp(self):
    self.cad = all_models.CustomAttributeDefinition()

  def test_title_with_asterisk_throws(self):
    """Test if raises if title contains * symbol"""
    with self.assertRaises(ValueError):
      with app.app_context():
        title = "Title with asterisk *"
        self.cad.definition_type = "assessment_template"
        self.cad.validate_title("title", title)
