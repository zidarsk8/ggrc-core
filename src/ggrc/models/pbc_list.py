# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, Base

class PbcList(Base, db.Model):
  __tablename__ = 'pbc_lists'

  audit_cycle_id = deferred(
      db.Column(db.Integer, db.ForeignKey('cycles.id'), nullable=False),
      'PbcList')

  requests = db.relationship(
      'Request', backref='pbc_list', cascade='all, delete-orphan')
  control_assessments = db.relationship(
      'ControlAssessment', backref='pbc_list', cascade='all, delete-orphan')

  _publish_attrs = [
      'audit_cycle',
      'requests',
      'control_assessments',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(PbcList, cls).eager_query()
    return query.options(
        orm.joinedload('audit_cycle'),
        orm.subqueryload('requests'),
        orm.subqueryload('control_assessments'))
