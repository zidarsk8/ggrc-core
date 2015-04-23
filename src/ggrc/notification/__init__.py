# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: miha@reciprocitylabs.com


from collections import defaultdict
from freezegun import freeze_time
from datetime import date
from ggrc.extensions import get_extension_modules
from ggrc.models import Notification
from ggrc.utils import merge_dict
from ggrc import db
from sqlalchemy import and_


class NotificationServices():

  def __init__(self):
    self.services = self.all_notifications()

  def all_notifications(self):
    services = {}
    for extension_module in get_extension_modules():
      contributions = getattr(
          extension_module, 'contributed_notifications', None)
      if contributions:
        if callable(contributions):
          contributions = contributions()
        services.update(contributions)
    return services

  def get_service_function(self, name):
    if name not in self.services:
      raise ValueError("unknown service name: %s" % name)
    return self.services[name]

  def call_service(self, name, pn):
    service = self.get_service_function(name)
    return service(pn)


services = NotificationServices()


def get_notification_data(notifications):
  if not notifications:
    return {}
  aggregate_data = {}

  def merge_into(destination, source):
    if destination is None:
      return source

  for pn in notifications:
    data = services.call_service(pn.object_type.name, pn)
    aggregate_data = merge_dict(aggregate_data, data)

  return aggregate_data


def get_pending_notifications():
  notifications = db.session.query(Notification).filter(
      Notification.sent_at == None).all()  # noqa

  notif_by_day = defaultdict(list)
  for notification in notifications:
    notif_by_day[notification.send_on].append(notification)

  data = {}
  for day, notif in notif_by_day.iteritems():
    with freeze_time(day):
      data[day] = get_notification_data(notif)

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
