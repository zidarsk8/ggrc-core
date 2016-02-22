# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: miha@reciprocitylabs.com

from collections import defaultdict
from sqlalchemy import and_
from datetime import date, datetime
from jinja2 import Environment, PackageLoader

from ggrc.rbac import permissions
from werkzeug.exceptions import Forbidden
from ggrc.extensions import get_extension_modules
from ggrc.models import Notification, NotificationConfig
from ggrc.utils import merge_dict
from ggrc import db
from ggrc.notifications import common

ENV = Environment(loader=PackageLoader('ggrc', 'templates'))


class Services():

  services = []

  @classmethod
  def all_notifications(cls):
    services = {}
    for extension_module in get_extension_modules():
      contributions = getattr(
          extension_module, 'contributed_notifications', None)
      if contributions:
        if callable(contributions):
          contributions = contributions()
        services.update(contributions)
    return services

  @classmethod
  def get_service_function(cls, name):
    if not cls.services:
      cls.services = cls.all_notifications()
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
    if should_receive(notification,
                      user_data["force_notifications"][notification.id],
                      user_data["user"]["id"]):
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
      Notification.sent_at == None).all()  # noqa

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
           Notification.sent_at == None  # noqa
           )).all()
  return notifications, get_notification_data(notifications)


def generate_notification_email(data):
  pass


def dispatch_notifications():
  pass


def should_receive(notif, force_notif, person_id, nightly_cron=True):
  def is_enabled(notif_type):
    result = NotificationConfig.query.filter(
        and_(NotificationConfig.person_id == person_id,
             NotificationConfig.notif_type == notif_type))
    # TODO: create_user function should make entries in the notification
    # config table. The code below should not make sure we have default
    # values for new users.
    if result.count() == 0:
      # If we have no results, we need to use the default value, which is
      # true for digest emails.
      return notif_type == "Email_Digest"
    return result.one().enable_flag

  # TODO: has_instant is not used at the moment but will be used when we
  # implement instant notifications
  # has_instant = force_notif or is_enabled("Email_Now")
  has_digest = force_notif or is_enabled("Email_Digest")

  return has_digest


def send_todays_digest_notifications():
  digest_template = ENV.get_template("notifications/email_digest.html")
  notif_list, notif_data = get_todays_notifications()
  sent_emails = []
  subject = "gGRC daily digest for {}".format(date.today().strftime("%b %d"))
  for user_email, data in notif_data.iteritems():
    data = common.modify_data(data)
    email_body = digest_template.render(digest=data)
    common.send_email(user_email, subject, email_body)
    sent_emails.append(user_email)
  set_notification_sent_time(notif_list)
  return "emails sent to: <br> {}".format("<br>".join(sent_emails))


def set_notification_sent_time(notif_list):
  for notif in notif_list:
    notif.sent_at = datetime.now()
  db.session.commit()


def show_pending_notifications():
  if not permissions.is_admin():
    raise Forbidden()
  _, notif_data = get_pending_notifications()

  for day, day_notif in notif_data.iteritems():
    for user_email, data in day_notif.iteritems():
      data = common.modify_data(data)
  pending = ENV.get_template("notifications/view_pending_digest.html")
  return pending.render(data=sorted(notif_data.iteritems()))


def show_todays_digest_notifications():
  if not permissions.is_admin():
    raise Forbidden()
  _, notif_data = get_todays_notifications()
  for user_email, data in notif_data.iteritems():
    data = common.modify_data(data)
  todays = ENV.get_template("notifications/view_todays_digest.html")
  return todays.render(data=notif_data)
