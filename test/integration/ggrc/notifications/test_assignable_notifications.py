# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com


from freezegun import freeze_time
from datetime import datetime
from mock import patch

from ggrc.models import Notification
from ggrc.models import Person
from ggrc.models import Request
from integration.ggrc import converters
from integration.ggrc.models import factories
from integration.ggrc.generator import ObjectGenerator


class TestAssignableNotification(converters.TestCase):

  """ This class contains simple one time workflow tests that are not
  in the gsheet test grid
  """

  def setUp(self):
    converters.TestCase.setUp(self)
    self.client.get("/login")
    self._fix_notification_init()

  def _fix_notification_init(self):
    """Fix Notification object init function

    This is a fix needed for correct created_at field when using freezgun. By
    default the created_at field is left empty and filed by database, which
    uses system time and not the fake date set by freezugun plugin. This fix
    makes sure that object created in freeze_time block has all dates set with
    the correct date and time.
    """

    def init_decorator(init):
      def new_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        if hasattr(self, "created_at"):
          self.created_at = datetime.now()
      return new_init

    Notification.__init__ = init_decorator(Notification.__init__)

  def _get_unsent_notifications(self):
    return Notification.query.filter(Notification.sent_at.is_(None))

  @patch("ggrc.notifications.common.send_email")
  def test_request_without_verifiers(self, mock_mail):

    with freeze_time("2015-04-01"):
      self.import_file("request_full_no_warnings.csv")

      self.assertEqual(self._get_unsent_notifications().count(), 12)

      self.client.get("/_notifications/send_todays_digest")
      self.assertEqual(self._get_unsent_notifications().count(), 0)

