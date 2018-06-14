# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from sqlalchemy import orm

from ggrc import db
from ggrc.models.mixins import Base
from ggrc.models import reflection


class Event(Base, db.Model):
  __tablename__ = 'events'

  action = db.Column(
      db.Enum(u'POST', u'PUT', u'DELETE', u'BULK', u'GET'),
      nullable=False,
  )
  resource_id = db.Column(db.Integer)
  resource_type = db.Column(db.String)

  revisions = db.relationship(
      'Revision',
      backref='event',
      cascade='all, delete-orphan',
  )

  _api_attrs = reflection.ApiAttributes(
      'action',
      'resource_id',
      'resource_type',
      'revisions',
  )

  _include_links = [
      'revisions',
  ]

  @staticmethod
  def _extra_table_args(class_):
    return (
        db.Index('events_modified_by', 'modified_by_id'),
    )

  @classmethod
  def eager_query(cls):
    query = super(Event, cls).eager_query()
    return query.options(
        orm.subqueryload('revisions').undefer_group('Revision_complete'),
    )
