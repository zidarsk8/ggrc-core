# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test import and export of objects with custom attributes."""

import itertools
from collections import OrderedDict

import ddt

from ggrc import models
from ggrc.access_control.roleable import Roleable
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
    acl = models.AccessControlList.query.filter_by(
        ac_role_id=role_id,
        object_id=market.id,
        object_type="Market"
    )
    self.assertEqual(acl.count(), 1)
    self.assertEqual(acl.first().ac_role_id, role_id)
    self.assertEqual(acl.first().person.email, "user@example.com")

  def test_acl_multiple_entries(self):
    """Test ACL column import with multiple emails."""
    with factories.single_commit():
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
        emails | {"user@example.com"},
    )

  def test_acl_update(self):
    """Test ACL column import with multiple emails."""
    with factories.single_commit():
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
    with factories.single_commit():
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
        emails | {"user@example.com"},
    )

  def test_acl_export(self):
    """Test ACL field export."""
    with factories.single_commit():
      role_name = factories.AccessControlRoleFactory(object_type="Market").name
      empty_name = factories.AccessControlRoleFactory(
          object_type="Market",
      ).name
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

  @staticmethod
  def _generate_role_import_dict(roles, object_type="Market"):
    """Generate simple import dict with all roles and emails."""
    import_dict = OrderedDict([
        ("object_type", object_type),
        ("code", "{}-1".format(object_type.lower())),
        ("title", "Title"),
        ("Admin", "user@example.com"),
    ])
    if object_type == "Control":
      import_dict["Assertions*"] = "Privacy"
    for role_name, emails in roles.items():
      import_dict[role_name] = "\n".join(emails)
    return import_dict

  @ddt.data({
      "role_name_1": set(),
      "role_name_2": set(_random_emails[2:]),
  }, {
      "role_name_1": set(_random_emails[:3]),
      "role_name_2": set(_random_emails[2:]),
      "role_name_3": set(_random_emails),
  })
  def test_multiple_acl_roles_add(self, roles):
    """Test importing new object with multiple ACL roles."""
    with factories.single_commit():
      for email in self._random_emails:
        factories.PersonFactory(email=email)

      for role_name in roles.keys():
        factories.AccessControlRoleFactory(
            object_type="Market",
            name=role_name + "  ",
        )

    import_dict = self._generate_role_import_dict(roles)
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
    """Test updating objects via import with multiple ACL roles."""
    with factories.single_commit():
      for email in self._random_emails:
        factories.PersonFactory(email=email)

      for role_name in first_roles.keys():
        factories.AccessControlRoleFactory(
            object_type="Market",
            name=role_name,
        )

    import_dict = self._generate_role_import_dict(first_roles)
    self.import_data(import_dict)
    market = models.Market.query.first()

    stored_roles = {}
    for role_name in first_roles.keys():
      stored_roles[role_name] = {
          acl.person.email for acl in market.access_control_list
          if acl.ac_role.name == role_name
      }

    self.assertEqual(stored_roles, first_roles)

    import_dict = self._generate_role_import_dict(edited_roles)
    self.import_data(import_dict)
    market = models.Market.query.first()

    stored_roles = {}
    for role_name in edited_roles.keys():
      stored_roles[role_name] = {
          acl.person.email for acl in market.access_control_list
          if acl.ac_role.name == role_name
      }

    self.assertEqual(stored_roles, edited_roles)

  @ddt.data({
      "Market": {"role name": set(_random_emails[:2])},
      "Facility": {"role name": set(_random_emails[2:])},
  }, {
      "Control": {"role name": set(_random_emails[:3])},
      "Market": {"role name": set(_random_emails[2:])},
      "System": {"role name": set(_random_emails)},
      "Objective": {"role name": set()},
      "Product": {"role name": set(_random_emails[:1])},
      "Policy": {"other role name": set(_random_emails[:1])},
  })
  def test_same_name_roles(self, model_dict):
    """Test role with the same names on different objects."""
    with factories.single_commit():
      for email in self._random_emails:
        factories.PersonFactory(email=email)

      import_dicts = []
      for object_type, roles in model_dict.items():
        for role_name in roles.keys():
          factories.AccessControlRoleFactory(
              object_type=object_type,
              name=role_name,
          )

        import_dicts.append(
            self._generate_role_import_dict(roles, object_type)
        )

    response = self.import_data(*import_dicts)
    self._check_csv_response(response, {})
    stored_roles = {}
    for object_type, roles in model_dict.items():
      model = getattr(models, object_type)
      obj = model.query.first()
      stored_roles[object_type] = {}
      for role_name in roles.keys():
        stored_roles[object_type][role_name] = {
            acl.person.email for acl in obj.access_control_list
            if acl.ac_role.name == role_name and
            acl.ac_role.object_type == object_type
        }
    self.assertEqual(stored_roles, model_dict)

  def test_acl_revision_on_import(self):
    """Test creation of separate revision for ACL in import"""
    with factories.single_commit():
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
    market_revisions = models.Revision.query.filter_by(
        resource_type="Market"
    ).count()
    self.assertEqual(market_revisions, 1)

    acr_revisions = models.Revision.query.filter_by(
        resource_type="AccessControlRole"
    ).count()
    self.assertEqual(acr_revisions, 1)

    acl_revisions = models.Revision.query.filter_by(
        resource_type="AccessControlList"
    ).count()
    self.assertEqual(acl_revisions, 4)

  def test_acl_roles_clear(self):
    """Test clearing ACL roles for Program with '--' value"""
    with factories.single_commit():
      program = factories.ProgramFactory()
      for role in ["Program Editors", "Program Editors", "Program Readers"]:
        person = factories.PersonFactory()
        ac_role = models.all_models.AccessControlRole.query.filter_by(
            object_type=program.type,
            name=role,
        ).first()
        factories.AccessControlListFactory(
            ac_role=ac_role,
            object=program,
            person=person,
        )

    for role in {"Program Editors", "Program Readers"}:
      response = self.import_data(OrderedDict([
          ("object_type", program.type),
          ("code", program.slug),
          (role, "--"),
      ]))
      self._check_csv_response(response, {})
      program = models.all_models.Program.query.first()
      for acl in program.access_control_list:
        self.assertNotEqual(acl.ac_role.name, role)

  @ddt.data("Assignee", "Verifier")
  def test_import_acl_validation(self, role):
    """Test import object with {} roles exceeding max limit"""
    role_max = getattr(Roleable, "MAX_{}_NUM".format(role.upper()))
    with factories.single_commit():
      for i in range(role_max + 1):
        factories.PersonFactory(email="user{}@example.com".format(i))
    roles = "\n".join(
        "user{}@example.com".format(i) for i in range(role_max + 1)
    )
    response = self.import_data(OrderedDict([
        ("object_type", "OrgGroup"),
        ("Code*", "OrgGroup-1"),
        ("Admin", "user@example.com"),
        ("title", "Test OrgGroup"),
        (role, roles),
    ]))
    self.assertIn(
        "{} role must have only {} person(s) assigned".format(
            role,
            role_max
        ),
        response[0]["row_errors"][0]
    )
