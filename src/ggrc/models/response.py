# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from ggrc.models.document import Document
from ggrc.models.mixins import Described
from ggrc.models.mixins import Hyperlinked
from ggrc.models.mixins import Noted
from ggrc.models.mixins import Slugged
from ggrc.models.mixins import Titled
from ggrc.models.mixins import WithContact
from ggrc.models.mixins import deferred
from ggrc.models.object_document import Documentable
from ggrc.models.object_document import ObjectDocument
from ggrc.models.object_person import Personable
from ggrc.models.reflection import AttributeInfo
from ggrc.models.relationship import Relatable
from ggrc.models.request import Request


class Response(Noted, Described, Documentable, Hyperlinked, WithContact,
               Titled, Slugged, db.Model):
  __tablename__ = 'responses'
  __mapper_args__ = {
      'polymorphic_on': 'response_type',
  }
  _title_uniqueness = False
  _slug_uniqueness = False

  # Override `Titled.title` to provide default=""
  title = deferred(
      db.Column(db.String, nullable=False, default=""), 'Response')

  VALID_STATES = (u'Assigned', u'Submitted', u'Accepted', u'Rejected')
  VALID_TYPES = (u'documentation', u'interview', u'population sample')
  request_id = deferred(
      db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False),
      'Response')
  response_type = db.Column(db.Enum(*VALID_TYPES), nullable=False)
  status = deferred(db.Column(db.String, nullable=False), 'Response')

  population_worksheet_id = deferred(
      db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True),
      'Response')
  population_count = deferred(db.Column(db.Integer, nullable=True), 'Response')
  sample_worksheet_id = deferred(
      db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True),
      'Response')
  sample_count = deferred(db.Column(db.Integer, nullable=True), 'Response')
  sample_evidence_id = deferred(
      db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True),
      'Response')

  population_worksheet = db.relationship(
      "Document",
      foreign_keys="PopulationSampleResponse.population_worksheet_id"
  )
  sample_worksheet = db.relationship(
      "Document",
      foreign_keys="PopulationSampleResponse.sample_worksheet_id"
  )
  sample_evidence = db.relationship(
      "Document",
      foreign_keys="PopulationSampleResponse.sample_evidence_id"
  )

  @staticmethod
  def _extra_table_args(cls):
    return (
        db.Index('population_worksheet_document', 'population_worksheet_id'),
        db.Index('sample_evidence_document', 'sample_evidence_id'),
        db.Index('sample_worksheet_document', 'sample_worksheet_id'),
    )

  _publish_attrs = [
      'request',
      'status',
      'response_type',
  ]
  _sanitize_html = [
      'description',
  ]

  _aliases = {
      "description": "Response",
      "request": {
          "display_name": "Request",
          "mandatory": True,
          "filter_by": "_filter_by_request",
      },
      "response_type": {
          "display_name": "Response Type",
          "mandatory": True,
      },
      "status": "Status",
      "title": None,
      "secondary_contact": None,
      "notes": None,
      "documents": {
          "display_name": "Documents",
          "type": AttributeInfo.Type.SPECIAL_MAPPING,
          "filter_by": "_filter_by_documents"
      },
      "mapped_objects": {
          "display_name": "Mapped Objects",
          "type": AttributeInfo.Type.SPECIAL_MAPPING,
          "filter_by": "_filter_by_mapped_objects",
      }

  }

  def _display_name(self):
    return u'Response with id={0} for Audit "{1}"'.format(
        self.id, self.request.audit.display_name)

  @classmethod
  def _filter_by_documents(cls, predicate):
    types = ["Response", "DocumentationResponse", "InterviewResponse",
             "PopulationSampleResponse"]
    return ObjectDocument.query.filter(
        (ObjectDocument.documentable_type.in_(types)) &
        (ObjectDocument.documentable_id == cls.id)
    ).join(Document).filter(
        predicate(Document.title)
    ).exists()

  @classmethod
  def _filter_by_mapped_objects(cls, predicate):
    # ignore this since response is going away soon
    return True

  @classmethod
  def _filter_by_request(cls, predicate):
    return Request.query.filter(
        (Request.id == cls.request_id) &
        predicate(Request.slug)
    ).exists()

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Response, cls).eager_query()
    return query.options(
        orm.joinedload('request'))


class DocumentationResponse(Relatable, Personable, Response):

  __mapper_args__ = {
      'polymorphic_identity': 'documentation'
  }
  _table_plural = 'documentation_responses'

  _publish_attrs = []
  _sanitize_html = []


class InterviewResponse(Relatable, Personable, Response):

  __mapper_args__ = {
      'polymorphic_identity': 'interview'
  }
  _table_plural = 'interview_responses'

  meetings = db.relationship(
      'Meeting',
      backref='response',
      cascade='all, delete-orphan'
  )
  _publish_attrs = [
      'meetings',
  ]
  _sanitize_html = []

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(InterviewResponse, cls).eager_query()
    return query.options(
        orm.subqueryload('meetings'))


class PopulationSampleResponse(Relatable, Personable, Response):

  __mapper_args__ = {
      'polymorphic_identity': 'population sample'
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
      'population_count',
      'sample_count',
  ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(PopulationSampleResponse, cls).eager_query()
    return query.options(
        orm.joinedload('population_worksheet'),
        orm.joinedload('sample_worksheet'),
        orm.joinedload('sample_evidence'))
