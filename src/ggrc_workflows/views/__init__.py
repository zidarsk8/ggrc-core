# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc_workflows import start_recurring_cycles
from ggrc import notification
from ggrc.notification import email
from jinja2 import Environment, PackageLoader
from datetime import date

env = Environment(loader=PackageLoader('ggrc_workflows', 'templates'))

# TODO: move these views to ggrc_views and all the functions to notifications
# module.

def do_start_recurring_cycles():
  start_recurring_cycles()
  return 'Ok'


def show_pending_notifications():
  _, notif_data = notification.get_pending_notifications()
  pending = env.get_template("notifications/pending_digest_notifitaitons.html")
  return pending.render(data=sorted(notif_data.iteritems()))


def show_todays_digest_notifications():
  _, notif_data = notification.get_todays_notifications()
  todays = env.get_template("notifications/todays_digest_notifications.html")
  return todays.render(data=notif_data)


def send_pending_notifications():
  digest_template = env.get_template("notifications/email_digest.html")
  notifications, notif_data = notification.get_pending_notifications()
  sent_emails = []
  for day, day_notif in notif_data.iteritems():
    subject = "gGRC daily digest for {}".format(day.strftime("%b %d"))
    for user_email, data in day_notif.iteritems():
      email_body = digest_template.render(digest=data)
      email.send_email(user_email, subject, email_body)
      sent_emails.append(user_email)
  return "emails sent to: <br> {}".format("", "<br>".join(sent_emails))


def send_todays_digest_notifications():
  digest_template = env.get_template("notifications/email_digest.html")
  notifications, notif_data = notification.get_todays_notifications()
  sent_emails = []
  subject = "gGRC daily digest for {}".format(date.today().strftime("%b %d"))
  for user_email, data in notif_data.iteritems():
    email_body = digest_template.render(digest=data)
    email.send_email(user_email, subject, email_body)
    sent_emails.append(user_email)
  return "emails sent to: <br> {}".format("", "<br>".join(sent_emails))


def init_extra_views(app):
  app.add_url_rule(
      "/start_recurring_cycles", "start_recurring_cycles",
      view_func=do_start_recurring_cycles)

  app.add_url_rule(
      "/_notifications/show_pending", "show_pending_notifications",
      view_func=show_pending_notifications)

  app.add_url_rule(
      "/_notifications/show_todays_digest", "show_todays_digest_notifications",
      view_func=show_todays_digest_notifications)

  app.add_url_rule(
      "/_notifications/send_pending", "send_pending_notifications",
      view_func=send_pending_notifications)

  app.add_url_rule(
      "/_notifications/send_todays_digest", "send_todays_digest_notifications",
      view_func=send_todays_digest_notifications)
