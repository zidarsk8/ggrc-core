# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from ggrc.models.all_models import all_models
from ggrc.rbac import permissions
from sqlalchemy import event
from sqlalchemy.schema import DDL
from .sql import SqlIndexer

class MysqlRecordProperty(db.Model):
  __tablename__ = 'fulltext_record_properties'
  __table_args__ = {'mysql_engine': 'myisam'}

  key = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String(64), primary_key=True)
  context_id = db.Column(db.Integer)
  tags = db.Column(db.String)
  property = db.Column(db.String(64), primary_key=True)
  content = db.Column(db.Text)

event.listen(
    MysqlRecordProperty.__table__,
    'after_create',
    DDL('ALTER TABLE {tablename} ADD FULLTEXT INDEX {tablename}_text_idx '
      '(content)'.format(tablename=MysqlRecordProperty.__tablename__))
    )

class MysqlIndexer(SqlIndexer):
  record_type = MysqlRecordProperty

  def search(self, terms):
    type_clauses =[]
    for model in all_models:
      clause = 'type = "{0}"'.format(model.__name__)
      type_permissions = permissions.read_contexts_for(model.__name__)
      if type_permissions is None:
        # can read in all contexts
        type_clauses.append('({0})'.format(clause))
      elif type_permissions:
        # can read in limited contexts
        clause = '{0} and context_id in ({1})'.format(
            clause,
            ','.join(['{0}'.format(id) for id in type_permissions]))
        type_clauses.append('({0})'.format(clause))
      else:
        # else, can't read in any context, don't add a clause for it
        pass
    type_clauses_str = ' or '.join(type_clauses) 
    if len(type_clauses) > 1:
      type_clauses_str = '({0})'.format(type_clauses_str)
    query = db.session.query(self.record_type).filter(
      '(match (content) against (:terms)) and {0}'.format(type_clauses_str))\
          .params(terms=terms).all()
    return query

Indexer = MysqlIndexer

