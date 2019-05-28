# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# pylint: disable=missing-docstring,invalid-name

import json
from random import random

from flask_testing import TestCase

from ggrc import db
from ggrc.app import app
from ggrc.models.person import Person

from integration.ggrc.views.saved_searches.initializers import (
    setup_user_role,
    get_client_and_headers,
)


class TestSavedSearchPost(TestCase):

  @staticmethod
  def create_app():
    return app

  @classmethod
  def setUpClass(cls):
    """
      Set up read-only test data to test GET requests.
    """

    super(TestSavedSearchPost, cls).setUpClass()

    email_0 = "aniki_baniki_{}@test.com".format(random())
    cls._person_0 = Person(name="Aniki", email=email_0)
    db.session.add(cls._person_0)
    db.session.flush()

    cls._user_role = setup_user_role(cls._person_0)
    db.session.commit()

    cls._client, cls._headers = get_client_and_headers(
        app, cls._person_0,
    )

  def setUp(self):
    self._client.get("/login", headers=self._headers)

  def tearDown(self):
    self._client.get("/logout", headers=self._headers)

  @classmethod
  def tearDownClass(cls):
    """
      Clean up created user and related saved searches.
    """

    super(TestSavedSearchPost, cls).tearDownClass()

    db.session.delete(cls._user_role)
    db.session.delete(cls._person_0)
    db.session.commit()

  def test_0_successful_creation_of_saved_search(self):
    response = self._client.post(
        "/api/saved_searches",
        data=json.dumps({
            "name": "test_ss_3",
            "object_type": "Assessment",
        }),
        headers=self._headers,
    )

    self.assertEqual(response.status, "200 OK")

    response = self._client.get(
        "/api/saved_searches/Assessment?limit=1",
        headers=self._headers,
    )

    data = json.loads(response.data)

    self.assertEqual(len(data["values"]), 1)
    self.assertEqual(data["values"][0]["name"], "test_ss_3")

  def test_1_saved_search_creation_failure_due_not_unique_name(self):
    response = self._client.post(
        "/api/saved_searches",
        data=json.dumps({
            "name": "test_ss_3",
            "object_type": "Assessment",
        }),
        headers=self._headers,
    )

    data = json.loads(response.data)

    self.assertEqual(
        data["message"],
        u"Saved search with name 'test_ss_3' already exists",
    )
    self.assertEqual(data["code"], 400)

  def test_2_saved_search_creation_failure_due_to_empty_name(self):
    response = self._client.post(
        "/api/saved_searches",
        data=json.dumps({
            "name": "",
            "object_type": "Assessment",
        }),
        headers=self._headers,
    )

    data = json.loads(response.data)

    self.assertEqual(data["message"], "Saved search name can't be blank")
    self.assertEqual(data["code"], 400)

  def test_3_saved_search_creation_failure_due_invalid_object_type(self):
    response = self._client.post(
        "/api/saved_searches",
        data=json.dumps({
            "name": "test_ss_1",
            "object_type": "Overwatch",
        }),
        headers=self._headers,
    )

    data = json.loads(response.data)

    self.assertEqual(
        data["message"],
        u"Object of type 'Overwatch' does not support search saving",
    )
    self.assertEqual(data["code"], 400)

  def test_4_successful_creation_of_saved_search_with_filters(self):
    """Test that we able to write and read values to filters field"""
    _filter = {"expression":
               {"left":
                {"left": "Title",
                 "op": {"name": "~"},
                 "right": "one"
                 },
                "op": {"name": "AND"},
                "right": {"left": "Status",
                          "op": {"name": "IN"},
                          "right": ["Active", "Draft", "Deprecated"]
                          }
                }
               }
    response = self._client.post(
        "/api/saved_searches",
        data=json.dumps({
            "name": "test_ss_4",
            "object_type": "Assessment",
            "filters": _filter
        }),
        headers=self._headers,
    )

    self.assertEqual(response.status, "200 OK")

    response = self._client.get(
        "/api/saved_searches/Assessment",
        headers=self._headers,
    )

    data = json.loads(response.data)

    for saved_search in data["values"]:
      if saved_search["name"] == "test_ss_4":
        self.assertEqual(json.loads(saved_search["filters"]), _filter)
