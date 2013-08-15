# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, Base
from .object_document import Documentable
from .object_person import Personable

class Response(Documentable, Personable, Base, db.Model):
  __tablename__ = 'responses'

  request_id = deferred(
      db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False),
      'Response')
  system_id = deferred(
      db.Column(db.Integer, db.ForeignKey('systems.id'), nullable=False),
      'Response')
  status = deferred(db.Column(db.String), 'Response')

  meetings = db.relationship('Meeting', backref='response', cascade='all, delete-orphan')
  population_sample = db.relationship(
      'PopulationSample', backref='response', uselist=False, cascade='all, delete-orphan')

  __table_args__ = (
    db.UniqueConstraint('request_id', 'system_id'),
  )

  _publish_attrs = [
      'request',
      'system',
      'status',
      'meetings',
      'population_sample',
      ]
  _sanitize_html = [
      'status',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Response, cls).eager_query()
    return query.options(
        orm.joinedload('request'),
        orm.joinedload('system'),
        orm.subqueryload('meetings'),
        orm.subqueryload('population_sample'))

  def _display_name(self):
    return self.system.display_name + '<->' + self.request.display_name
