# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com

"""
 GGRC notification SQLAlchemy layer data model extensions
"""

from sqlalchemy.orm import backref

from ggrc.app import db
from .mixins import Base, Stateful 


class NotificationConfig(Base, db.Model):
  __tablename__ = 'notification_configs'
  name = db.Column(db.String, nullable=True)
  enable_flag = db.Column(db.Boolean)
  notif_type = db.Column(db.String)
  person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
  person = db.relationship(
      'Person',
      backref=backref('notification_configs', cascade='all, delete-orphan'))

  _publish_attrs = [
    'person_id',
    'notif_type',
    'enable_flag',
  ]

  VALID_TYPES = [
    'Email_Now',
    'Email_Digest',
    'Calendar',
  ]


class Notification(Base, db.Model):
  __tablename__ = 'notifications'
  name = db.Column(db.String, nullable=True)
  notif_date = db.Column(db.DateTime)
  notif_pri = db.Column(db.Integer)
  content = db.Column(db.Text)
  subject = db.Column(db.String)
  sender_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
  recipients = db.relationship(
      'NotificationRecipient', backref='notification', cascade='all, delete-orphan')
  notification_object = db.relationship(
      'NotificationObject', backref='notification', cascade='all, delete-orphan')


class NotificationObject(Base, Stateful, db.Model):
  __tablename__ = 'notification_objects'

  VALID_STATES = [
    None, 
    "InProgress", 
    "Assigned", 
    "Finished", 
    "Declined", 
    "Verified",
  ]

  name = db.Column(db.String, nullable=True)
  notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'), nullable=False)
  object_id = db.Column(db.Integer, nullable=False)
  object_type = db.Column(db.String, nullable=False)

class NotificationRecipient(Base, Stateful, db.Model):
  __tablename__ = 'notification_recipients'

  VALID_STATES = [
    "InProgress",
    "Successful",
    "NotificationDisabled",
    "Skipped",
    "Failed",
  ]

  name = db.Column(db.String, nullable=True)
  notif_type = db.Column(db.String)
  notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'), nullable=False)
  recipient_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
  error_text = db.Column(db.Text)
  content = db.Column(db.Text)

class CalendarEntry(Base, db.Model):
  __tablename__='calendar_entries'
  name=db.Column(db.String, nullable=True)
  calendar_id = db.Column(db.String, nullable=True)
  owner_id=db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
