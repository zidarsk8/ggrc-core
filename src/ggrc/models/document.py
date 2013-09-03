# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from sqlalchemy.orm import validates
from .mixins import deferred, Base
from .utils import validate_option

class Document(Base, db.Model):
  __tablename__ = 'documents'

  title = deferred(db.Column(db.String), 'Document')
  link = deferred(db.Column(db.String), 'Document')
  description = deferred(db.Column(db.Text), 'Document')
  type_id = deferred(db.Column(db.Integer), 'Document')
  kind_id = deferred(db.Column(db.Integer), 'Document')
  year_id = deferred(db.Column(db.Integer), 'Document')
  language_id = deferred(db.Column(db.Integer), 'Document')

  object_documents = db.relationship('ObjectDocument', backref='document', cascade='all, delete-orphan')
  population_worksheets_documented = db.relationship(
      'PopulationSample',
      foreign_keys='PopulationSample.population_document_id',
      backref='population_document',
      )
  sample_worksheets_documented = db.relationship(
      'PopulationSample',
      foreign_keys='PopulationSample.sample_worksheet_document_id',
      backref='sample_worksheet_document',
      )
  sample_evidences_documented = db.relationship(
      'PopulationSample',
      foreign_keys='PopulationSample.sample_evidence_document_id',
      backref='sample_evidence_document',
      )
  type = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Document.type_id) == Option.id, '\
                       'Option.role == "document_type")',
      uselist=False,
      )
  kind = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Document.kind_id) == Option.id, '\
                       'Option.role == "reference_type")',
      uselist=False,
      )
  year = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Document.year_id) == Option.id, '\
                       'Option.role == "document_year")',
      uselist=False,
      )
  language = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Document.language_id) == Option.id, '\
                       'Option.role == "language")',
      uselist=False,
      )

  _publish_attrs = [
      'title',
      'link',
      'description',
      'object_documents',
      'population_worksheets_documented',
      'sample_worksheets_documented',
      'sample_evidences_documented',
      'type',
      'kind',
      'year',
      'language',
      ]
  _sanitize_html = [
      'title',
      'description',
      ]

  @validates('type', 'kind', 'year', 'language')
  def validate_document_options(self, key, option):
    if key in ('type', 'year'):
      desired_role  = 'document_' + key
    elif key == 'kind':
      desired_role = 'reference_type'
    else:
      desired_role = key
    return validate_option(self.__class__.__name__, key, option, desired_role)

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Document, cls).eager_query()
    return query.options(
        orm.joinedload('type'),
        orm.joinedload('kind'),
        orm.joinedload('year'),
        orm.joinedload('language'),
        orm.subqueryload('object_documents'),
        orm.subqueryload('population_worksheets_documented'),
        orm.subqueryload('sample_worksheets_documented'),
        orm.subqueryload('sample_evidences_documented'));
