# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, Base, Hyperlinked

class Evidence(Hyperlinked, Base, db.Model):
  __tablename__ = 'evidence'

  response_id = deferred(
      db.Column(db.Integer, db.ForeignKey('responses.id'), nullable=False),
      'Evidence')

  _publish_attrs = [
    'response',
  ]
  _sanitize_html = [
  ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Evidence, cls).eager_query()
    return query.options()
        #orm.joinedload('response'))
