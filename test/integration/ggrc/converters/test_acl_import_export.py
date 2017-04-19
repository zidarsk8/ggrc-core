# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test import and export of objects with custom attributes."""

import itertools
from collections import OrderedDict

import ddt

from ggrc import models
from integration.ggrc import TestCase
from integration.ggrc.models import factories


@ddt.ddt
class TestACLImportExport(TestCase):
  """Test import and export with custom attributes."""
  _random_emails = [
      "user_1@example.com",
      "user_2@example.com",
      "user_3@example.com",
      "user_4@example.com",
  ]

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
    emails = {factories.PersonFactory().email for _ in range(4)}
    update_emails = set(list(emails)[:2]) | {"user@example.com"}

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
        (role_name, "\n".join(update_emails)),
    ]))
    self._check_csv_response(response, {})
    market = models.Market.query.first()
    self.assertEqual(
        {acl.person.email for acl in market.access_control_list},
        update_emails,
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
    self.import_data(OrderedDict([
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

  @ddt.data({
      "role_name_1": set(),
      "role_name_2": set(_random_emails[2:]),
  }, {
      "role_name_1": set(_random_emails[:3]),
      "role_name_2": set(_random_emails[2:]),
      "role_name_3": set(_random_emails),
  })
  def test_multiple_acl_roles_add(self, roles):
    for email in self._random_emails:
      factories.PersonFactory(email=email)

    import_dict = OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
    ])

    for role_name, emails, in roles.items():
      factories.AccessControlRoleFactory(
          object_type="Market",
          name=role_name,
      )
      import_dict[role_name] = "\n".join(emails)

    self.import_data(import_dict)
    market = models.Market.query.first()

    stored_roles = {}
    for role_name in roles.keys():
      stored_roles[role_name] = {
          acl.person.email for acl in market.access_control_list
          if acl.ac_role.name == role_name
      }

    self.assertEqual(stored_roles, roles)

  @ddt.data(*list(itertools.combinations([{
      "role_name_1": set(),
      "role_name_2": set(),
      "role_name_3": set(),
  }, {
      "role_name_1": set(),
      "role_name_2": set(_random_emails[2:]),
      "role_name_3": set(_random_emails),
  }, {
      "role_name_1": set(_random_emails[:3]),
      "role_name_2": set(_random_emails[2:]),
      "role_name_3": set(_random_emails),
  }, {
      "role_name_1": set(_random_emails),
      "role_name_2": set(_random_emails),
      "role_name_3": set(_random_emails),
  }], 2)))
  @ddt.unpack
  def test_multiple_acl_roles_update(self, first_roles, edited_roles):
    for email in self._random_emails:
      factories.PersonFactory(email=email)

    import_dict = OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
    ])

    for role_name, emails, in first_roles.items():
      factories.AccessControlRoleFactory(
          object_type="Market",
          name=role_name,
      )
      import_dict[role_name] = "\n".join(emails)

    self.import_data(import_dict)
    market = models.Market.query.first()

    stored_roles = {}
    for role_name in first_roles.keys():
      stored_roles[role_name] = {
          acl.person.email for acl in market.access_control_list
          if acl.ac_role.name == role_name
      }

    self.assertEqual(stored_roles, first_roles)

    import_dict = OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
    ])

    for role_name, emails, in edited_roles.items():
      import_dict[role_name] = "\n".join(emails)

    self.import_data(import_dict)
    market = models.Market.query.first()

    stored_roles = {}
    for role_name in edited_roles.keys():
      stored_roles[role_name] = {
          acl.person.email for acl in market.access_control_list
          if acl.ac_role.name == role_name
      }

    self.assertEqual(stored_roles, edited_roles)
