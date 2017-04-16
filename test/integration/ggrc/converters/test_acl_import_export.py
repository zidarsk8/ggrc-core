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
