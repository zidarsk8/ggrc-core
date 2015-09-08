# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import and_, or_
from .mixins import deferred, Base, Described, Titled, Slugged
from ggrc.models.person import Person
from ggrc.models.audit import Audit
from ggrc.models.audit_object import AuditObject

class Request(Titled, Slugged, Described, Base, db.Model):
  __tablename__ = 'requests'
  _title_uniqueness = False

  VALID_TYPES = (u'documentation', u'interview')
  VALID_STATES = (u'Draft', u'Requested', u'Responded', u'Amended Request',
    u'Updated Response', u'Accepted')
  requestor_id = db.Column(db.Integer, db.ForeignKey('people.id'))
  requestor = db.relationship('Person', foreign_keys=[requestor_id])
  assignee_id = db.Column(db.Integer, db.ForeignKey('people.id'),
    nullable=False)
  assignee = db.relationship('Person', foreign_keys=[assignee_id])
  request_type = deferred(db.Column(db.Enum(*VALID_TYPES), nullable=False),
    'Request')
  status = deferred(db.Column(db.Enum(*VALID_STATES), nullable=False),
    'Request')
  requested_on = deferred(db.Column(db.Date, nullable=False), 'Request')
  due_on = deferred(db.Column(db.Date, nullable=False), 'Request')
  audit_id = db.Column(db.Integer, db.ForeignKey('audits.id'), nullable=False)
  audit_object_id = db.Column(db.Integer, db.ForeignKey('audit_objects.id'),
    nullable=True)
  gdrive_upload_path = deferred(db.Column(db.String, nullable=True),
    'Request')
  test = deferred(db.Column(db.Text, nullable=True), 'Request')
  notes = deferred(db.Column(db.Text, nullable=True), 'Request')
  responses = db.relationship('Response', backref='request',
    cascade='all, delete-orphan')

  # workaround for title being attached to slug
  @declared_attr
  def title(cls):
    return deferred(db.Column(db.String, nullable=True), cls.__name__)

  _publish_attrs = [
    'assignee',
    'requestor',
    'request_type',
    'gdrive_upload_path',
    'requested_on',
    'due_on',
    'status',
    'audit',
    'audit_object',
    'responses',
    'test',
    'notes',
  ]
  _sanitize_html = [
    'gdrive_upload_path',
    'test',
    'notes',
    'description',
  ]

  _aliases = {
    "assignee": {
      "display_name": "Assignee",
      "filter_by": "_filter_by_assignee",
    },
    "audit_object": {
      "display_name": "Request Object",
      "filter_by": "_filter_by_audit_object",
    },
    "request_audit": {
      "display_name": "Audit",
      "filter_by": "_filter_by_request_audit",
    },
    "due_on": "Due On",
    "notes": "Notes",
    "request_type": "Request Type",
    "requested_on": "Requested On",
    "status": "Status",
    "test": "Test",
    "title": None,
  }

  def _display_name(self):
    if len(self.description) > 32:
      description_string = self.description[:32] + u'...'
    else:
      description_string = self.description
    return u'Request with id {0} "{1}" for Audit "{2}"'.format(
        self.id,
        description_string,
        self.audit.display_name
    )

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Request, cls).eager_query()
    return query.options(
      orm.joinedload('audit'),
      orm.joinedload('audit_object'),
      orm.subqueryload('responses'))

  @classmethod
  def _filter_by_assignee(cls, predicate):
    return cls.query.filter(
      (Person.id == cls.assignee_id) &
      (predicate(Person.name) | predicate(Person.email))
    ).exists()

  @classmethod
  def _filter_by_request_audit(cls, predicate):
    return cls.query.filter(
      (Audit.id == cls.audit_id) &
      (predicate(Audit.slug) | predicate(Audit.title))
    ).exists()

  @classmethod
  def _filter_by_audit_object(cls, predicate):
    from ggrc.models import all_models
    queries = []
    for model_name in all_models.__all__:
      model = getattr(all_models, model_name)
      if not hasattr(model, "query"):
        continue
      fields = []
      for field_name in ["slug", "title", "name", "email"]:
        if hasattr(model, field_name):
          fields.append(getattr(model, field_name))
      if len(fields) > 0:
        queries.append(model.query.filter(
            (AuditObject.auditable_type == model.__name__) &
            or_(*map(predicate, fields))
        ).exists())
    return AuditObject.query.filter(
        (AuditObject.id == cls.audit_object_id) &
        or_(*queries)
    ).exists()

