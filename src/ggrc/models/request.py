# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, Base

class Request(Base, db.Model):
  __tablename__ = 'requests'

  pbc_list_id = deferred(
      db.Column(db.Integer, db.ForeignKey('pbc_lists.id'), nullable=False),
      'Request')
  type_id = deferred(db.Column(db.Integer), 'Request')
  pbc_control_code = deferred(db.Column(db.String), 'Request')
  pbc_control_desc = deferred(db.Column(db.Text), 'Request')
  request = deferred(db.Column(db.Text), 'Request')
  test = deferred(db.Column(db.Text), 'Request')
  notes = deferred(db.Column(db.Text), 'Request')
  company_responsible = deferred(db.Column(db.String), 'Request')
  auditor_responsible = deferred(db.Column(db.String), 'Request')
  date_requested = deferred(db.Column(db.DateTime), 'Request')
  status = deferred(db.Column(db.String), 'Request')
  control_assessment_id = deferred(
      db.Column(db.Integer, db.ForeignKey('control_assessments.id')),
      'Request')
  response_due_at = deferred(db.Column(db.Date), 'Request')

  responses = db.relationship('Response', backref='request', cascade='all, delete-orphan')

  _publish_attrs = [
      'pbc_list',
      'type_id',
      'pbc_control_code',
      'pbc_control_desc',
      'request',
      'test',
      'notes',
      'company_responsible',
      'auditor_responsible',
      'date_requested',
      'status',
      'control_assessment',
      'response_due_at',
      'responses',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Request, cls).eager_query()
    return query.options(
        orm.joinedload('pbc_list'),
        orm.joinedload('control_assessment'),
        orm.subqueryload('responses'))
