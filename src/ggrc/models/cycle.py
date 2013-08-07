# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, Base, Described
from .object_document import Documentable
from .object_person import Personable

class Cycle(Documentable, Personable, Base, Described, db.Model):
  __tablename__ = 'cycles'

  start_at = deferred(db.Column(db.Date), 'Cycle')
  complete = deferred(db.Column(db.Boolean, default=False, nullable=False), 'Cycle')
  title = deferred(db.Column(db.String), 'Cycle')
  audit_firm = deferred(db.Column(db.String), 'Cycle')
  audit_lead = deferred(db.Column(db.String), 'Cycle')
  status = deferred(db.Column(db.String), 'Cycle')
  notes = deferred(db.Column(db.Text), 'Cycle')
  end_at = deferred(db.Column(db.Date), 'Cycle')
  program_id = deferred(
      db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False), 'Cycle')
  report_due_at = deferred(db.Column(db.Date), 'Cycle')

  pbc_lists = db.relationship(
        'PbcList', backref='audit_cycle', cascade='all, delete-orphan')

  _publish_attrs = [
      'start_at',
      'complete',
      'title',
      'audit_firm',
      'audit_lead',
      'status',
      'notes',
      'end_at',
      'program',
      'report_due_at',
      'pbc_lists',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Cycle, cls).eager_query()
    return query.options(
        orm.joinedload('program'),
        orm.subqueryload('pbc_lists'))
