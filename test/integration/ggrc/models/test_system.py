# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for System model."""
import mock

from ggrc import db
from ggrc.models import all_models
from integration.ggrc import TestCase
from integration.ggrc.models import factories
from integration.ggrc import api_helper


@mock.patch(
    'ggrc.settings.EXTERNAL_APP_USER',
    new='External App <external_app@example.com>'
)
class TestSoxSystem(TestCase):
  """Tests for Sox System model."""

  def setUp(self):
    """Test setup method."""
    super(TestSoxSystem, self).setUp()
    self.api = api_helper.Api()

    self.app_user_email = "external_app@example.com"
    self.ext_user_email = "external@example.com"

    custom_headers = {
        'X-GGRC-user': '{"email": "%s"}' % self.app_user_email,
        'X-external-user': '{"email": "%s"}' % self.ext_user_email
    }

    self.api.headers.update(custom_headers)
    self.api.client.get("/login", headers=self.api.headers)

  def test_system_acl_create(self):
    """Test creation of SOX system with non empty acl."""
    response = self.api.post(all_models.System, {
        "system": {
            "title": "new_system",
            "context": None,
            "access_control_list": {"Admin": [
                {
                    "email": "user1@example.com",
                    "name": "user1",
                },
            ]}
        }
    })

    self.assertEqual(201, response.status_code)

    system = all_models.System.query.get(response.json["system"]["id"])
    actual_people = system.get_persons_for_rolename("Admin")
    expected_people = all_models.Person.query.filter_by(
        email="user1@example.com"
    ).all()
    self.assertItemsEqual(actual_people, expected_people)

  def test_system_acl_update(self):
    """Test updating of SOX system with non empty acl."""
    with factories.single_commit():
      system = factories.SystemFactory()
      person = factories.PersonFactory()
      system.add_person_with_role_name(person, "Admin")

    response = self.api.put(system, {
        "access_control_list": {
            "Admin": [
                {
                    "email": "user1@example.com",
                    "name": "user1",
                },
                {
                    "email": "user2@example.com",
                    "name": "user2",
                },
            ]
        },
    })
    self.assert200(response)
    system = all_models.System.query.get(system.id)
    actual_people_ids = system.get_person_ids_for_rolename("Admin")
    expected_people_ids = db.session.query(all_models.Person.id).filter(
        all_models.Person.email.in_(("user1@example.com", "user2@example.com"))
    ).all()
    self.assertItemsEqual(
        actual_people_ids,
        [i[0] for i in expected_people_ids]
    )
