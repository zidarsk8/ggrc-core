# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc_workflows import start_recurring_cycles
from ggrc import notification
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('ggrc_workflows', 'templates'))


def do_start_recurring_cycles():
  start_recurring_cycles()
  return 'Ok'


def show_pending_notifications():
  pending_notifications = notification.get_pending_notifications()

  pending = env.get_template("notifications/pending_digest_notifitaitons.html")

  return pending.render(data=sorted(pending_notifications.iteritems()))


def init_extra_views(app):
  app.add_url_rule(
      "/start_recurring_cycles", "start_recurring_cycles",
      view_func=do_start_recurring_cycles)

  app.add_url_rule(
      "/_notifications/show_pending", "show_pending_notifications",
      view_func=show_pending_notifications)
