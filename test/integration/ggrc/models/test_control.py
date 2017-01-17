# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for control model."""

from ggrc import db
from ggrc.models import Control
from integration.ggrc import TestCase
from integration.ggrc.models import factories


class TestControl(TestCase):

  def test_simple_categorization(self):
    category = factories.ControlCategoryFactory(scope_id=100)
    control = factories.ControlFactory()
    control.categories.append(category)
    db.session.commit()
    self.assertIn(category, control.categories)
    # be really really sure
    control = db.session.query(Control).get(control.id)
    self.assertIn(category, control.categories)

  def test_has_test_plan(self):
    control = factories.ControlFactory(test_plan="This is a test text")
    control = db.session.query(Control).get(control.id)
    self.assertEqual(control.test_plan, "This is a test text")
