# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com

"""
 GGRC notification SQLAlchemy layer data model extensions
"""

from sqlalchemy.orm import backref
from sqlalchemy import event

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


