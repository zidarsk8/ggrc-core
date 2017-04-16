# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test import and export of objects with custom attributes."""

from collections import OrderedDict

from ggrc import models
from integration.ggrc import TestCase
from integration.ggrc.models import factories


class TestACLImportExport(TestCase):
  """Test import and export with custom attributes."""

  def test_single_acl_entry(self):
    """Test ACL column import with single email."""
    role = factories.AccessControlRoleFactory(object_type="Market")
    role_id = role.id

    response = self.import_data(OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
        (role.name, "user@example.com"),
    ]))
    self._check_csv_response(response, {})
    market = models.Market.query.first()
    self.assertEqual(len(market.access_control_list), 1)
    self.assertEqual(market.access_control_list[0].ac_role_id, role_id)
    self.assertEqual(
        market.access_control_list[0].person.email,
        "user@example.com"
    )

  def test_acl_multiple_entries(self):
    """Test ACL column import with multiple emails."""
    role = factories.AccessControlRoleFactory(object_type="Market")
    emails = {factories.PersonFactory().email for _ in range(3)}

    response = self.import_data(OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
        (role.name, "\n".join(emails)),
    ]))
    self._check_csv_response(response, {})
    market = models.Market.query.first()
    self.assertEqual(
        {acl.person.email for acl in market.access_control_list},
        emails,
    )

  def test_acl_update(self):
    """Test ACL column import with multiple emails."""
    role_name = factories.AccessControlRoleFactory(object_type="Market").name
    emails = {factories.PersonFactory().email for _ in range(3)}

    response = self.import_data(OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
        (role_name, "\n".join(emails)),
    ]))
    self._check_csv_response(response, {})
    response = self.import_data(OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
        (role_name, "user@example.com"),
    ]))
    self._check_csv_response(response, {})
    market = models.Market.query.first()
    self.assertEqual(
        {acl.person.email for acl in market.access_control_list},
        {"user@example.com"},
    )

  def test_acl_empty_update(self):
    """Test ACL column import with multiple emails."""
    role_name = factories.AccessControlRoleFactory(object_type="Market").name
    emails = {factories.PersonFactory().email for _ in range(3)}

    response = self.import_data(OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
        (role_name, "\n".join(emails)),
    ]))
    self._check_csv_response(response, {})
    response = self.import_data(OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
        (role_name, ""),
    ]))
    self._check_csv_response(response, {})
    market = models.Market.query.first()
    self.assertEqual(
        {acl.person.email for acl in market.access_control_list},
        emails,
    )

  def test_acl_export(self):
    """Test ACL field export."""
    role_name = factories.AccessControlRoleFactory(object_type="Market").name
    empty_name = factories.AccessControlRoleFactory(object_type="Market").name
    emails = {factories.PersonFactory().email for _ in range(3)}
    response = self.import_data(OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
        (role_name, "\n".join(emails)),
    ]))

    search_request = [{
        "object_name": "Market",
        "filters": {
            "expression": {}
        },
        "fields": [
          "slug",
         "__acl__:{}".format(role_name),
         "__acl__:{}".format(empty_name),
        ],
    }]
    self.client.get("/login")
    parsed_data = self.export_parsed_csv(
        search_request
    )["Market"]
    self.assertEqual(
        set(parsed_data[0][role_name].splitlines()),
        emails
    )
    self.assertEqual(parsed_data[0][empty_name], "")
