# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for user generator"""

import json
import mock

from integration.ggrc.services import TestCase
from ggrc.integrations.client import PersonClient
from ggrc.models import Person
from ggrc_basic_permissions.models import UserRole


class TestUserGenerator(TestCase):
  """Test user generation."""

  def setUp(self):
    super(TestUserGenerator, self).setUp()
    self.clear_data()
    self.client.get("/login")

  def _post(self, data):
    return self.client.post(
        '/api/people',
        content_type='application/json',
        data=data,
        headers=[('X-Requested-By', 'Unit Tests')],
    )

  @staticmethod
  def _mock_post(*args, **kwargs):
    """Mock of IntegrationService _post"""
    # pylint: disable=unused-argument
    payload = kwargs["payload"]
    res = []
    for name in payload["usernames"]:
      res.append({'firstName': name,
                  'lastName': name,
                  'username': name})
    return {'persons': res}

  @mock.patch('ggrc.settings.INTEGRATION_SERVICE_URL', new='endpoint')
  @mock.patch('ggrc.settings.AUTHORIZED_DOMAIN', new='example.com')
  def test_user_generation(self):
    """Test user generation."""
    with mock.patch.multiple(
        PersonClient,
        _post=self._mock_post
    ):
      data = json.dumps([{'person': {
          'name': 'Alan Turing',
          'email': 'aturing@example.com',
          'context': None,
          'external': True
      }}])
      response = self._post(data)
      self.assertStatus(response, 200)

      user = Person.query.filter_by(email='aturing@example.com').one()
      self.assertEqual(user.name, 'Alan Turing')

      roles = UserRole.query.filter_by(person_id=user.id)
      self.assertEqual(roles.count(), 1)

  @mock.patch('ggrc.settings.INTEGRATION_SERVICE_URL', new='endpoint')
  @mock.patch('ggrc.settings.AUTHORIZED_DOMAIN', new='example.com')
  def test_user_creation(self):
    """Test user creation."""
    with mock.patch.multiple(
        PersonClient,
        _post=self._mock_post
    ):
      data = json.dumps([{'person': {
          'name': 'Alan Turing',
          'email': 'aturing@example.com',
          'context': None
      }}])
      response = self._post(data)
      self.assertStatus(response, 200)

      user = Person.query.filter_by(email='aturing@example.com').one()
      self.assertEqual(user.name, 'Alan Turing')

      roles = UserRole.query.filter_by(person_id=user.id)
      self.assertEqual(roles.count(), 0)

  @mock.patch('ggrc.settings.INTEGRATION_SERVICE_URL', new='endpoint')
  @mock.patch('ggrc.settings.AUTHORIZED_DOMAIN', new='example.com')
  def test_wrong_user_creation(self):
    """Test wrong user creation."""
    with mock.patch.multiple(
        PersonClient,
        _post=mock.MagicMock(return_value={'persons': []})
    ):
      data = json.dumps([{'person': {
          'name': 'Alan Turing',
          'email': 'aturing@example.com',
          'context': None,
          'external': True
      }}])
      response = self._post(data)
      self.assertStatus(response, 406)

      user = Person.query.filter_by(email='aturing@example.com').first()
      self.assertIsNone(user)
