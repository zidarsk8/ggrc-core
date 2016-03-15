# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: miha@reciprocitylabs.com


"""
 GGRC email notification module hook to prepares email, email digest, notify
 email to recipients
"""


from collections import defaultdict
from datetime import date
from datetime import datetime
from flask import current_app
from sqlalchemy import and_
from werkzeug.exceptions import Forbidden

import jinja2
from google.appengine.api import mail

from ggrc import db
from ggrc import extensions
from ggrc import settings
from ggrc.models import Notification
from ggrc.models import NotificationConfig
from ggrc.rbac import permissions
from ggrc.utils import merge_dict

ENV = jinja2.Environment(loader=jinja2.PackageLoader('ggrc', 'templates'))


class Services(object):
  """Helper class for notification services.

  This class is is a helper class for calling a notification service for a
  given object. The first call get_service_function must be done after all
  modules have been initialized.
  """

  services = []

  @classmethod
  def get_service_function(cls, name):
    if not cls.services:
      cls.services = extensions.get_module_contributions(
          "contributed_notifications")
    if name not in cls.services:
      raise ValueError("unknown service name: %s" % name)
    return cls.services[name]

  @classmethod
  def call_service(cls, name, notification):
    service = cls.get_service_function(name)
    return service(notification)


def get_filter_data(notification):
  result = {}
  data = Services.call_service(notification.object_type, notification)

  for user, user_data in data.iteritems():
    if should_receive(notification, user_data):
      result[user] = user_data
  return result


def get_notification_data(notifications):
  if not notifications:
    return {}
  aggregate_data = {}

  for notification in notifications:
    filtered_data = get_filter_data(notification)
    aggregate_data = merge_dict(aggregate_data, filtered_data)

  # Remove notifications for objects without a contact (such as task groups)
  aggregate_data.pop("", None)

  return aggregate_data


def get_pending_notifications():
  notifications = db.session.query(Notification).filter(
      Notification.sent_at.is_(None)).all()

  notif_by_day = defaultdict(list)
  for notification in notifications:
    notif_by_day[notification.send_on].append(notification)

  data = defaultdict(dict)
  today = datetime.combine(date.today(), datetime.min.time())
  for day, notif in notif_by_day.iteritems():
    current_day = max(day, today)
    data[current_day] = merge_dict(data[current_day],
                                   get_notification_data(notif))

  return notifications, data


def get_todays_notifications():
  notifications = db.session.query(Notification).filter(
      and_(Notification.send_on <= date.today(),
           Notification.sent_at.is_(None)
           )).all()
  return notifications, get_notification_data(notifications)


def should_receive(notif, user_data):
  """Check if a user should receive a notification or not.

  Args:
    notif (Notification): A notification entry that we are checking.
    user_data (dict): A dictionary containing data about user notifications.

  Returns:
    True if user should receive the given notification, or False otherwise.
  """
  force_notif = user_data.get("force_notifications", {}).get(notif.id, False)
  person_id = user_data["user"]["id"]

  def is_enabled(notif_type):
    """Check user notification settings.

    Args:
      notif_type (string): can be "Email_Digest" or "Email_Now" based on what
        we wish to check.

    Returns:
      Boolean based on what settings users has stored or what the default
      setting is for the given notification.
    """
    result = NotificationConfig.query.filter(
        and_(NotificationConfig.person_id == person_id,
             NotificationConfig.notif_type == notif_type))
    if result.count() == 0:
      # If we have no results, we need to use the default value, which is
      # true for digest emails.
      return notif_type == "Email_Digest"
    return result.one().enable_flag

  has_digest = force_notif or is_enabled("Email_Digest")

  return has_digest


def send_todays_digest_notifications():
  digest_template = ENV.get_template("notifications/email_digest.html")
  notif_list, notif_data = get_todays_notifications()
  sent_emails = []
  subject = "gGRC daily digest for {}".format(date.today().strftime("%b %d"))
  for user_email, data in notif_data.iteritems():
    data = modify_data(data)
    email_body = digest_template.render(digest=data)
    send_email(user_email, subject, email_body)
    sent_emails.append(user_email)
  set_notification_sent_time(notif_list)
  return "emails sent to: <br> {}".format("<br>".join(sent_emails))


def set_notification_sent_time(notif_list):
  """Set sent time to now for all notifications in the list.

  Args:
    notif_list (list of Notification): List of notification for which we want
      to modify sent_at field.
  """
  for notif in notif_list:
    notif.sent_at = datetime.now()
  db.session.commit()


def show_pending_notifications():
  if not permissions.is_admin():
    raise Forbidden()
  _, notif_data = get_pending_notifications()

  for day_notif in notif_data.itervalues():
    for data in day_notif.itervalues():
      data = modify_data(data)
  pending = ENV.get_template("notifications/view_pending_digest.html")
  return pending.render(data=sorted(notif_data.iteritems()))


def show_todays_digest_notifications():
  if not permissions.is_admin():
    raise Forbidden()
  _, notif_data = get_todays_notifications()
  for data in notif_data.itervalu.itervalues():
    data = modify_data(data)
  todays = ENV.get_template("notifications/view_todays_digest.html")
  return todays.render(data=notif_data)


def get_app_engine_email():
  """Get notification sender email.

  Return the email of the user that will be set as sender. This email should be
  authorized to send emails from the server. For more details, see Application
  Settings for email api authorized senders.

  Returns:
    Valid email address if it's set in the app settings.
  """
  email = getattr(settings, 'APPENGINE_EMAIL')
  return email if mail.is_email_valid(email) else None


def send_email(user_email, subject, body):
  """Helper function for sending emails.

  Args:
    user_email (string): Email of the recipient.
    subject (string): Email subject.
    body (basestring): Html body of the email. it can contain unicode
      characters and will be sent as a html mime type.
  """
  sender = get_app_engine_email()
  if not mail.is_email_valid(user_email):
    current_app.logger.error("Invalid email recipient: {}".format(user_email))
    return
  if not sender:
    current_app.logger.error("APPENGINE_EMAIL setting is invalid.")
    return

  message = mail.EmailMessage(sender=sender, subject=subject)

  message.to = user_email
  message.body = "TODO: add email in text mode."
  message.html = body

  message.send()


def modify_data(data):
  """
  for easier use in templates, it joins the due_in and due today fields
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
