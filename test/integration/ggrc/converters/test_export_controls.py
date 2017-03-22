# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Tests for task group task specific export."""
from ggrc import db
from integration.ggrc.models import factories
from integration.ggrc import TestCase


class TestExportControls(TestCase):
  """Test imports for basic control objects."""

  def setUp(self):
    super(TestExportControls, self).setUp()
    self.client.get("/login")
    self.headers = {
        'Content-Type': 'application/json',
        "X-Requested-By": "GGRC",
        "X-export-view": "blocks",
    }
    self.basic_owner = factories.PersonFactory(name="basic owner")
    self.control = factories.ControlFactory()
    self.owner_object = factories.OwnerFactory(person=self.basic_owner,
                                               ownable=self.control)

  # pylint: disable=invalid-name
  def assertSlugs(self, field, value, slugs):
    """Assert slugs for selected search"""
    search_request = [{
        "object_name": "Control",
        "filters": {
            "expression": {
                "left": field,
                "op": {"name": "="},
                "right": value,
            },
        },
        "fields": ["slug"],
    }]

    parsed_data = self.export_parsed_csv(search_request)["Control"]
    self.assertEqual(sorted(slugs),
                     sorted([i["Code*"] for i in parsed_data]))

  def test_search_by_owner_email(self):
    self.assertSlugs("owners",
                     self.basic_owner.email,
                     [self.control.slug])

  def test_search_by_owner_name(self):
    self.assertSlugs("owners",
                     self.basic_owner.name,
                     [self.control.slug])

  def test_search_by_new_owner(self):
    """Filter by added new owner and old owner"""
    basic_email, basic_name = self.basic_owner.email, self.basic_owner.name
    new_owner = factories.PersonFactory(name="new owner")
    factories.OwnerFactory(person=new_owner, ownable=self.control)
    self.assertSlugs("owners",
                     new_owner.email,
                     [self.control.slug])
    self.assertSlugs("owners",
                     new_owner.name,
                     [self.control.slug])
    self.assertSlugs("owners",
                     basic_email,
                     [self.control.slug])
    self.assertSlugs("owners",
                     basic_name,
                     [self.control.slug])

  def test_search_by_deleted_owner(self):
    """Filter by deleted owner"""
    db.session.delete(self.owner_object)
    db.session.commit()
    self.assertSlugs("owners", self.basic_owner.email, [])
    self.assertSlugs("owners", self.basic_owner.name, [])
