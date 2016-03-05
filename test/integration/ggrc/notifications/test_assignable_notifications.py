# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Tests for notifications for models with assignable mixin."""

from datetime import datetime
from freezegun import freeze_time
from sqlalchemy import and_

from ggrc import db
from ggrc.models import Notification
from ggrc.models import NotificationType
from integration.ggrc import converters
from integration.ggrc import api_helper


class TestAssignableNotification(converters.TestCase):

  """ This class contains simple one time workflow tests that are not
  in the gsheet test grid
  """

  def setUp(self):
    converters.TestCase.setUp(self)
    self.client.get("/login")
    self._fix_notification_init()
    self.api_helper = api_helper.Api()

  def _fix_notification_init(self):
    """Fix Notification object init function.

    This is a fix needed for correct created_at field when using freezgun. By
    default the created_at field is left empty and filed by database, which
    uses system time and not the fake date set by freezugun plugin. This fix
    makes sure that object created in freeze_time block has all dates set with
    the correct date and time.
    """

    def init_decorator(init):
      """Wrapper for Notification init function."""

      def new_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        if hasattr(self, "created_at"):
          self.created_at = datetime.now()
      return new_init

    Notification.__init__ = init_decorator(Notification.__init__)

  @classmethod
  def _get_notifications(cls, sent=False, notif_type=None):
    """Get a notification query.

    Args:
      sent (boolean): flag to filter out only notifications that have been
        sent.
      notif_type (string): name of the notification type.

    Returns:
      sqlalchemy query for selected notifications.
    """
    if sent:
      notif_filter = Notification.sent_at.isnot(None)
    else:
      notif_filter = Notification.sent_at.is_(None)

    if notif_type:
      notif_filter = and_(notif_filter, NotificationType.name == notif_type)

    return db.session.query(Notification).join(NotificationType).filter(
        notif_filter
    )

  def test_request_without_verifiers(self):

    with freeze_time("2015-04-01"):
      self.import_file("request_full_no_warnings.csv")

      self.assertEqual(self._get_notifications().count(), 12)

      self.client.get("/_notifications/send_todays_digest")
      self.assertEqual(self._get_notifications().count(), 0)
