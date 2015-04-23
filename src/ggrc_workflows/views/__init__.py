# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc import db
from ggrc_workflows import start_recurring_cycles
from ggrc import notification
from ggrc.login import login_required
from ggrc.notification import email
from jinja2 import Environment, PackageLoader
from datetime import date, datetime
from ggrc.rbac import permissions
from werkzeug.exceptions import Forbidden


env = Environment(loader=PackageLoader('ggrc_workflows', 'templates'))

# TODO: move these views to ggrc_views and all the functions to notifications
# module.


def modify_data(data):
  """
  for easyer use in templates, it joins the due_in and due today fields
  together
  """

  data["due_soon"] = {}
  if "due_in" in data:
    data["due_soon"].update(data["due_in"])
  if "due_today" in data:
    data["due_soon"].update(data["due_today"])

  # combine "my_tasks" from multiple cycles
  data["cycle_started_tasks"] = {}
  if "cycle_started" in data:
    for cycle in data["cycle_started"].values():
      if "my_tasks" in cycle:
        data["cycle_started_tasks"].update(cycle["my_tasks"])

  return data


def do_start_recurring_cycles():
  start_recurring_cycles()
  return 'Ok'


def show_pending_notifications():
  if not permissions.is_admin():
    raise Forbidden()
  _, notif_data = notification.get_pending_notifications()

  for day, day_notif in notif_data.iteritems():
    for user_email, data in day_notif.iteritems():
      data = modify_data(data)
  pending = env.get_template("notifications/view_pending_digest.html")
  return pending.render(data=sorted(notif_data.iteritems()))


def show_todays_digest_notifications():
  if not permissions.is_admin():
    raise Forbidden()
  _, notif_data = notification.get_todays_notifications()
  for user_email, data in notif_data.iteritems():
    data = modify_data(data)
  todays = env.get_template("notifications/view_todays_digest.html")
  return todays.render(data=notif_data)


def set_notification_sent_time(notifications):
  for notif in notifications:
    notif.sent_at = datetime.now()
  db.session.commit()


def send_pending_notifications():
  digest_template = env.get_template("notifications/email_digest.html")
  notifications, notif_data = notification.get_pending_notifications()
  sent_emails = []
  for day, day_notif in notif_data.iteritems():
    subject = "gGRC daily digest for {}".format(day.strftime("%b %d"))
    for user_email, data in day_notif.iteritems():
      data = modify_data(data)
      email_body = digest_template.render(digest=data)
      email.send_email(user_email, subject, email_body)
      sent_emails.append(user_email)
  set_notification_sent_time(notifications)
  return "emails sent to: <br> {}".format("", "<br>".join(sent_emails))


def send_todays_digest_notifications():
  digest_template = env.get_template("notifications/email_digest.html")
  notifications, notif_data = notification.get_todays_notifications()
  sent_emails = []
  subject = "gGRC daily digest for {}".format(date.today().strftime("%b %d"))
  for user_email, data in notif_data.iteritems():
    data = modify_data(data)
    email_body = digest_template.render(digest=data)
    email.send_email(user_email, subject, email_body)
    sent_emails.append(user_email)
  set_notification_sent_time(notifications)
  return "emails sent to: <br> {}".format("", "<br>".join(sent_emails))


def init_extra_views(app):
  app.add_url_rule(
      "/start_recurring_cycles", "start_recurring_cycles",
      view_func=do_start_recurring_cycles)

  app.add_url_rule(
      "/_notifications/show_pending", "show_pending_notifications",
      view_func=login_required(show_pending_notifications))

  app.add_url_rule(
      "/_notifications/show_todays_digest", "show_todays_digest_notifications",
      view_func=login_required(show_todays_digest_notifications))

  app.add_url_rule(
      "/_notifications/send_pending", "send_pending_notifications",
      view_func=login_required(send_pending_notifications))

  app.add_url_rule(
      "/_notifications/send_todays_digest", "send_todays_digest_notifications",
      view_func=send_todays_digest_notifications)
