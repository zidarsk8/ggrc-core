# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, Base

class Meeting(Base, db.Model):
  __tablename__ = 'meetings'

  response_id = deferred(
      db.Column(db.Integer, db.ForeignKey('responses.id'), nullable=False),
      'Meeting')
  start_at = deferred(db.Column(db.DateTime), 'Meeting')
  calendar_url = deferred(db.Column(db.String), 'Meeting')

  _publish_attrs = [
      'response',
      'start_at',
      'calendar_url',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Meeting, cls).eager_query()
    return query.options(
        orm.joinedload('response'))
