# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: vraj@reciprocitylabs.com
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import Base, created_at_args

class Event(Base, db.Model):
  __tablename__ = 'events'

  http_method = db.Column(db.Enum(u'POST', u'PUT', u'DELETE'), nullable = False)
  resource_id = db.Column(db.Integer, nullable = False)
  resource_type = db.Column(db.String, nullable = False)

  revisions = db.relationship('Revision', backref='event', lazy='subquery') # We always need the revisions

  _publish_attrs = [
      'http_method',
      'resource_id',
      'resource_type',
      'revisions',
  ]

