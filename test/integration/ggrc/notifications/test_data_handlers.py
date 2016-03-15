# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Tests for notifications for models with assignable mixin."""

from sqlalchemy import and_

from ggrc import db
from ggrc.notifications import data_handlers
from ggrc.models import Request
from ggrc.models import Notification
from ggrc.models import NotificationType
from integration.ggrc import converters
from integration.ggrc import api_helper


class TestRequestDataHandlers(converters.TestCase):
  """Test data handlers for various request notifications."""

  def setUp(self):
    converters.TestCase.setUp(self)
    self.client.get("/login")
    self.api_helper = api_helper.Api()
    self.import_file("request_full_no_warnings.csv")
    self.request1 = Request.query.filter_by(slug="Request 1").one()
    self.request3 = Request.query.filter_by(slug="Request 3").one()

  def _get_notification(self, obj, notif_type):
    return db.session.query(Notification).join(NotificationType).filter(and_(
        Notification.object_id == obj.id,
        Notification.object_type == obj.type,
        NotificationType.name == notif_type,
    ))

  def test_open_request(self):
    """Test data handlers for opened requests."""
    notif = self._get_notification(self.request1, "request_open").first()
    open_data = data_handlers.get_assignable_data(notif)
    request_1_expected_keys = set([
        "user1@a.com",
        "user2@a.com",
        "user3@a.com",
        "user4@a.com",
        "user5@a.com",
    ])

    self.assertEqual(set(open_data.keys()), request_1_expected_keys)

    notif = self._get_notification(self.request3, "request_open").first()
    open_data = data_handlers.get_assignable_data(notif)
    request_3_expected_keys = set([
        "user1@a.com",
        "user2@a.com",
        "user@example.com",
    ])

    self.assertEqual(set(open_data.keys()), request_3_expected_keys)

  def test_declined_request(self):
    """Test data handlers for declined requests"""

    # decline request 1
    self.api_helper.modify_object(self.request1, {"status": "Finished"})
    self.api_helper.modify_object(self.request1, {"status": "In Progress"})

    notif = self._get_notification(self.request1, "request_declined").first()
    declined_data = data_handlers.get_assignable_data(notif)
    requester_emails = set([
        "user2@a.com",
        "user3@a.com",
    ])

    self.assertEqual(set(declined_data.keys()), requester_emails)
