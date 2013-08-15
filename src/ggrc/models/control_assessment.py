# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, Base

class ControlAssessment(Base, db.Model):
  __tablename__ = 'control_assessments'

  pbc_list_id = db.Column(
      db.Integer, db.ForeignKey('pbc_lists.id'), nullable=False)
  control_id = db.Column(
      db.Integer, db.ForeignKey('controls.id'), nullable=False)
  control_version = deferred(db.Column(db.String), 'ControlAssessment')
  internal_tod = deferred(db.Column(db.Boolean), 'ControlAssessment')
  internal_toe = deferred(db.Column(db.Boolean), 'ControlAssessment')
  external_tod = deferred(db.Column(db.Boolean), 'ControlAssessment')
  external_toe = deferred(db.Column(db.Boolean), 'ControlAssessment')
  notes = deferred(db.Column(db.Text), 'ControlAssessment')

  requests = db.relationship('Request', backref='control_assessment')

  __table_args__ = (
    db.UniqueConstraint('pbc_list_id', 'control_id'),
  )

  _publish_attrs = [
      'pbc_list',
      'control',
      'control_version',
      'internal_tod',
      'internal_toe',
      'external_tod',
      'external_toe',
      'notes',
      'requests',
      ]
  _sanitize_html = [
      'control_version',
      'notes',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(ControlAssessment, cls).eager_query()
    return query.options(
        orm.joinedload('pbc_list'),
        orm.joinedload('control'),
        orm.subqueryload('requests'))

  def _display_name(self):
    return self.pbc_list.display_name + '<->' + self.control.display_name
