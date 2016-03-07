# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Views for email notifications."""

from ggrc.notifications import common
from ggrc.login import login_required


def init_notification_views(app):
  """Add url rules for all notification views.

  Args:
    app: current flask app.
  """
  app.add_url_rule(
      "/_notifications/send_todays_digest", "send_todays_digest_notifications",
      view_func=common.send_todays_digest_notifications)

  app.add_url_rule(
      "/_notifications/show_pending", "show_pending_notifications",
      view_func=login_required(common.show_pending_notifications))

  app.add_url_rule(
      "/_notifications/show_todays_digest", "show_todays_digest_notifications",
      view_func=login_required(common.show_todays_digest_notifications))
