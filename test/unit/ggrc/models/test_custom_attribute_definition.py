# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Custom Attribute Definition validation"""

import unittest
import ddt
from mock import MagicMock, Mock, patch

from ggrc import views
from ggrc.models import all_models
from ggrc.access_control import role as acr


@ddt.ddt
class TestCustomAttributeDefinition(unittest.TestCase):
  """Test Custom Attribute Definition validation"""

  def setUp(self):
    # pylint: disable=protected-access
    self.cad = all_models.CustomAttributeDefinition()
    self.cad._get_reserved_names = MagicMock(return_value=frozenset({'title'}))
    self.cad._get_global_cad_names = MagicMock(return_value={'reg url': 1})
    acr.get_custom_roles_for = MagicMock(return_value=dict())

  @ddt.data("title with asterisk*",
            "map:person",
            "unmap:person",
            "delete",
            "  map:    Market",
            "mAP:    CONTROL",
            "UNMAP:  NOTHING",
            "DeLeTe",
            )
  def test_title_with_asterisk_throws(self, title):
    """Test if raises if title invalid"""
    with self.assertRaises(ValueError):
      self.cad.validate_title("title", title)


@ddt.ddt
class TestCustomAttributeDefinitionViews(unittest.TestCase):
  # pylint: disable=protected-access
  """Test cads title modification functions in ggrc.views.__init__"""
  @ddt.data(
      (True, "program", "person", False),
      (True, "program", "program", False),
      (False, "program", "person", False),
      (False, "program", "program", True),
  )
  @ddt.unpack
  def test_is_cad_definition(self, is_none, definition_type,
                             expected_definition_type, expected):
    """Test _is_cad_definition function"""
    cad = None if is_none else Mock()
    if cad:
      cad.definition_type = definition_type

    result = bool(views._is_cad_definition_type(cad, expected_definition_type))
    self.assertEqual(result, expected)

  @ddt.data(
      (1, 1, [(None, {'custom_attribute_definitions': [
          {
              'id': 1,
              'title': 'new title'
          }]})]),
      (1, 2, []),
  )
  @ddt.unpack
  def test_modify_revision_content(self, cad_id, expected_cad_id, expected):
    """Test _get_modified_revision_content function"""
    cad = Mock(id=cad_id, title="new title")
    content = {
        "custom_attribute_definitions": [{
            "id": expected_cad_id,
            "title": "title"
        }]
    }

    obj = Mock(resource_type="Program")
    revision = all_models.Revision(obj, MagicMock(),
                                   MagicMock(), content)

    with patch("ggrc.views._get_revisions_by_type", return_value=[revision]):
      result = [c for c in views._get_modified_revision_content(
          cad, revision.resource_type)]
      self.assertEqual(result, expected)
