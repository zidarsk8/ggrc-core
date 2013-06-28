# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import Base
from .object_document import Documentable
from .object_person import Personable

class Response(Documentable, Personable, Base, db.Model):
  __tablename__ = 'responses'

  request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)
  system_id = db.Column(db.Integer, db.ForeignKey('systems.id'), nullable=False)
  status = db.Column(db.String)
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
