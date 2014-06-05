# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com

"""
 GGRC notification SQLAlchemy layer data model extensions
"""

from ggrc.app import db
from .mixins import Base, Stateful


class NotificationConfig(Base, db.Model):
  __tablename__ = 'notification_configs'
  notif_type = db.Column(db.String)
  person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)


class Notification(Base, db.Model):
  __tablename__ = 'notifications'
  notif_date = db.Column(db.DateTime)
  content = db.Column(db.Text)
  subject = db.Column(db.String)
  sender_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
  recipients = db.relationship(
      'NotificationRecipient', backref='notification', cascade='all, delete-orphan')
  notification_object = db.relationship(
      'NotificationObject', backref='notification', cascade='all, delete-orphan')


class NotificationObject(Base, db.Model):
  __tablename__ = 'notification_objects'
  notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'), nullable=False)
  object_id = db.Column(db.Integer, nullable=False)
  object_type = db.Column(db.String, nullable=False)


class NotificationRecipient(Base, Stateful, db.Model):
  __tablename__ = 'notification_recipients'

  VALID_STATES = [
    "Progress",
    "Successful",
    "Failure",
  ]

  notif_type = db.Column(db.String)
  notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'), nullable=False)
  recipient_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
  error_text = db.Column(db.Text)

