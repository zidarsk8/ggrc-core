# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, BusinessObject
from .object_document import Documentable
from .object_person import Personable

class Response(BusinessObject, db.Model):
  __tablename__ = 'responses'
  __mapper_args__ = {
      'polymorphic_on': 'response_type',
      }

  VALID_STATES = (u'Assigned', u'Accepted', u'Completed')
  VALID_TYPES = (u'documentation', u'interview', u'population sample')
  request_id = deferred(
      db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False),
      'Response')
  response_type = db.Column(db.Enum(*VALID_TYPES), nullable=False)
  status = deferred(db.Column(db.Enum(*VALID_STATES), nullable=False),
    'Response')

  _publish_attrs = [
      'request',
      'status',
      'response_type',
      ]
  _sanitize_html = [
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Response, cls).eager_query()
    return query.options(
        orm.joinedload('request'))

class DocumentationResponse(Documentable, Personable, Response):
  __mapper_args__ = {
      'polymorphic_identity': 'documentation'
      }
  _table_plural = 'documentation_responses'

  evidence = db.relationship('Evidence', backref='response',
    cascade='all, delete-orphan')

  _publish_attrs = [
    'evidence',
      ]
  _sanitize_html = [
      ]


  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(DocumentationResponse, cls).eager_query()
    return query.options(
        orm.subqueryload('evidence'))

class InterviewResponse(Documentable, Personable, Response):
  __mapper_args__ = {
      'polymorphic_identity': 'interview'
      }
  _table_plural = 'interview_responses'
  _publish_attrs = [
    #'meetings',
      ]
  _sanitize_html = [
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(InterviewResponse, cls).eager_query()
    return query.options()
        #orm.subqueryload('meetings'))

class PopulationSampleResponse(Documentable, Personable, Response):
  __mapper_args__ = {
      'polymorphic_identity': 'population sample'
      }
  _table_plural = 'population_sample_responses'

  population_worksheet = deferred(db.Column(db.String, nullable=True),
    'Response')
  population_count = deferred(db.Column(db.Integer, nullable=True),
    'Response')
  sample_worksheet = deferred(db.Column(db.String, nullable=True), 'Response')
  sample_count = deferred(db.Column(db.Integer, nullable=True), 'Response')
  sample_evidence = deferred(db.Column(db.String, nullable=True), 'Response')

  _publish_attrs = [
      'population_worksheet',
      'population_count',
      'sample_worksheet',
      'sample_count',
      'sample_evidence',
      ]
  _sanitize_html = [
      'population_worksheet',
      'population_count',
      'sample_worksheet',
      'sample_count',
      'sample_evidence',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(PopulationSampleResponse, cls).eager_query()
    return query.options()
