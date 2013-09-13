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

  # description
  VALID_STATES = (u'Assigned', u'Accepted', u'Completed')
  request_id = deferred(
      db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False),
      'Response')
  status = deferred(db.Column(db.Enum(VALID_STATES), nullable = False), 'Response')
  population_worksheet = deferred(db.Column(db.String, nullable=True), 'PopulationSampleResponse')
  population_count = deferred(db.Column(db.Integer, nullable=True), 'PopulationSampleResponse')
  sample_worksheet = deferred(db.Column(db.String, nullable=True), 'PopulationSampleResponse')
  sample_count = deferred(db.Column(db.Integer, nullable=True), 'PopulationSampleResponse')
  sample_evidence = deferred(db.Column(db.String, nullable=True), 'PopulationSampleResponse')

  _publish_attrs = [
      'request',
      'status',
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
      'polymorphic_identity': 'DocumentationResponse'
      }
  _table_plural = 'documentation_responses'
  _publish_attrs = [
    #'evidences',
      ]
  _sanitize_html = [
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Response, cls).eager_query()
    return query.options()
        #orm.subqueryload('evidences'))

class InterviewResponse(Documentable, Personable, Response):
  __mapper_args__ = {
      'polymorphic_identity': 'InterviewResponse'
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

    query = super(Response, cls).eager_query()
    return query.options()
        #orm.subqueryload('meetings'))

class PopulationSampleResponse(Documentable, Personable, Response):
  __mapper_args__ = {
      'polymorphic_identity': 'PopulationSampleResponse'
      }
  _table_plural = 'population_sample_responses'


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

