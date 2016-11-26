# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for snapshot model."""

from ggrc import db
from ggrc.app import app
from ggrc.services import common
from ggrc.models import all_models
from integration.ggrc.converters import TestCase
from integration.ggrc.models import factories


class TestSnapshot(TestCase):
  """Basic tests for /query api."""

  def setUp(self):
    """Set up test cases for all tests."""
    TestCase.clear_data()
    self._create_cas()
    self._import_file("all_snapshottable_objects.csv")

  @staticmethod
  def _create_cas():
    """Create custom attribute definitions."""
    for type_ in ["facility", "control", "market", "section"]:
      with app.app_context():
        factories.CustomAttributeDefinitionFactory(
            title="CA dropdown",
            definition_type=type_,
            attribute_type="Dropdown",
            multi_choice_options="one,two,three,four,five",
        )
        factories.CustomAttributeDefinitionFactory(
            title="CA text",
            definition_type=type_,
            attribute_type="Text",
        )
        factories.CustomAttributeDefinitionFactory(
            title="CA date",
            definition_type=type_,
            attribute_type="Date",
        )

  def test_revision_conent(self):
    """Test that revision contains all content needed."""

    facility_revision = all_models.Revision.query.filter(
        all_models.Revision.resource_type == "Facility").order_by(
        all_models.Revision.id.desc()).first()

    self.assertIn("custom_attributes", facility_revision.content)
    self.assertNotEqual(facility_revision.content["custom_attributes"], [])

