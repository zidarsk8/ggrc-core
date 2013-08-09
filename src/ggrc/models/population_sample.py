# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, Base

class PopulationSample(Base, db.Model):
  __tablename__ = 'population_samples'

  response_id = deferred(
      db.Column(db.Integer, db.ForeignKey('responses.id'), nullable=False),
      'PopulationSample')
  population_document_id = deferred(
      db.Column(db.Integer, db.ForeignKey('documents.id')), 'PopulationSample')
  population = deferred(db.Column(db.Integer), 'PopulationSample')
  sample_worksheet_document_id = deferred(
      db.Column(db.Integer, db.ForeignKey('documents.id')), 'PopulationSample')
  samples = deferred(db.Column(db.Integer), 'PopulationSample')
  sample_evidence_document_id = deferred(
      db.Column(db.Integer, db.ForeignKey('documents.id')), 'PopulationSample')

  _publish_attrs = [
      'response',
      'population_document',
      'population',
      'sample_worksheet_document',
      'sample_evidence_document',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(PopulationSample, cls).eager_query()
    return query.options(
        orm.subqueryload('response'),
        orm.subqueryload('population_document'),
        orm.subqueryload('sample_worksheet_document'),
        orm.subqueryload('sample_evidence_document'))
