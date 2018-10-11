# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for usage of X-external-user header."""


import json
import ddt
import mock

from ggrc.models import all_models

from ggrc.integrations.client import PersonClient
from integration.ggrc import TestCase
from integration.ggrc.models import factories


@ddt.ddt
class TestExternalPermissions(TestCase):
  """Tests for external permissions and modified by."""

  def setUp(self):
    """Set up request mock and mock dependencies."""
    super(TestExternalPermissions, self).setUp()
    self.allowed_appid = "ggrcq-id"
    self.settings_patcher = mock.patch("ggrc.login.appengine.settings")
    self.settings_mock = self.settings_patcher.start()
    self.settings_mock.ALLOWED_QUERYAPI_APP_IDS = [self.allowed_appid]

  @staticmethod
  def _mock_post(*args, **kwargs):
    """IntegrationService post mock."""
    # pylint: disable=unused-argument
    res = []
    for name in kwargs["payload"]["usernames"]:
      res.append({'firstName': name, 'lastName': name, 'username': name})
    return {'persons': res}

  def _post(self, url, data, headers):
    return self.client.post(
        url,
        content_type='application/json',
        data=data,
        headers=headers,
    )

  MODELS = [
      all_models.AccessGroup,
      all_models.Contract,
      all_models.Control,
      all_models.DataAsset,
      all_models.Facility,
      all_models.Issue,
      all_models.Market,
      all_models.Metric,
      all_models.Objective,
      all_models.OrgGroup,
      all_models.Policy,
      all_models.Process,
      all_models.Product,
      all_models.ProductGroup,
      all_models.Program,
      all_models.Project,
      all_models.Regulation,
      all_models.Requirement,
      all_models.Risk,
      all_models.Standard,
      all_models.System,
      all_models.TechnologyEnvironment,
      all_models.Threat,
      all_models.Vendor,
      all_models.Workflow
  ]

  @ddt.data(*MODELS)
  @mock.patch('ggrc.settings.INTEGRATION_SERVICE_URL', new='endpoint')
  @mock.patch('ggrc.settings.AUTHORIZED_DOMAIN', new='example.com')
  def test_post_modifier(self, model):
    """Test modifier of models when working as external user."""
    headers = {
        "Content-Type": "application/json",
        "X-requested-by": "GGRC",
        "X-appengine-inbound-appid": self.allowed_appid,
        "X-ggrc-user": json.dumps({"email": "external_app@example.com"}),
        "X-external-user": json.dumps({"email": "new_ext_user@example.com"})
    }

    model_plural = model._inflector.table_plural
    model_singular = model._inflector.table_singular
    with mock.patch.multiple(PersonClient, _post=self._mock_post):
      self.client.get("/login", headers=headers)
      response = self._post(
          "api/{}".format(model_plural),
          data=json.dumps({
              model_singular: {
                  "title": "{}1".format(model_singular),
                  "context": 0
              }
          }),
          headers=headers)
      self.assertEqual(response.status_code, 201)

    ext_person = all_models.Person.query.filter_by(
        email="new_ext_user@example.com"
    ).first()
    ext_person_id = ext_person.id

    # check that external user has Creator role
    self.assertEqual(ext_person.system_wide_role, "Creator")

    # check model modifier
    model_json = response.json[model_singular]
    self.assertEqual(model_json['modified_by']['id'], ext_person_id)

    # check model revision modifier
    model_revision = all_models.Revision.query.filter(
        all_models.Revision.resource_type == model.__name__).order_by(
        all_models.Revision.id.desc()).first()
    self.assertEqual(model_revision.modified_by_id, ext_person_id)

    # check model event modifier
    event = all_models.Event.query.filter(
        all_models.Event.resource_type == model.__name__).order_by(
        all_models.Event.id.desc()).first()
    self.assertEqual(event.modified_by_id, ext_person_id)

    # check relationship post
    destination = factories.SystemFactory()
    with mock.patch.multiple(PersonClient, _post=self._mock_post):
      response = self._post(
          "/api/relationships",
          data=json.dumps([{
              "relationship": {
                  "source": {"id": model_json['id'],
                             "type": model_json['type']},
                  "destination": {"id": destination.id,
                                  "type": destination.type},
                  "context": {"id": None},
                  "is_external": True
              }
          }]),
          headers=headers)
      self.assert200(response)
    relationship = all_models.Relationship.query.get(
        response.json[0][-1]["relationship"]["id"])
    self.assertEqual(relationship.source_type, model_json['type'])
    self.assertEqual(relationship.source_id, model_json['id'])
    self.assertEqual(relationship.destination_type, "System")
    self.assertEqual(relationship.destination_id, destination.id)
    self.assertTrue(relationship.is_external)
    self.assertEqual(relationship.modified_by_id, ext_person_id)
    self.assertIsNone(relationship.parent_id)
    self.assertIsNone(relationship.automapping_id)
    self.assertIsNone(relationship.context_id)

  @mock.patch('ggrc.settings.INTEGRATION_SERVICE_URL', new='endpoint')
  @mock.patch('ggrc.settings.AUTHORIZED_DOMAIN', new='example.com')
  @ddt.data("new_ext_user@example.com",
            json.dumps({"email": "external_app"}))
  def test_post_invalid_modifier(self, email):
    """Test that validation is working for X-external-user."""
    model = all_models.Market
    headers = {
        "Content-Type": "application/json",
        "X-requested-by": "GGRC",
        "X-appengine-inbound-appid": self.allowed_appid,
        "X-ggrc-user": json.dumps({"email": "external_app@example.com"}),
        "X-external-user": email
    }

    model_plural = model._inflector.table_plural
    model_singular = model._inflector.table_singular

    with mock.patch.multiple(PersonClient, _post=self._mock_post):
      self.client.get("/login", headers=headers)
      response = self._post(
          "api/{}".format(model_plural),
          data=json.dumps({
              model_singular: {
                  "title": "{}_invalid_1".format(model_singular),
                  "context": 0
              }
          }),
          headers=headers)
      self.assertEqual(response.status_code, 400)
