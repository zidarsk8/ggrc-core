# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc import notifications


def init_notification_views(app):
  app.add_url_rule(
      "/_notifications/send_todays_digest", "send_todays_digest_notifications",
      view_func=notifications.send_todays_digest_notifications)
