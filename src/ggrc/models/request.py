# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import datetime

from ggrc import db
from sqlalchemy import or_
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declared_attr

from ggrc.models.audit import Audit
from ggrc.models.audit_object import AuditObject
from ggrc.models.mixins import Assignable
from ggrc.models.mixins import Base
from ggrc.models.mixins import CustomAttributable
from ggrc.models.mixins import deferred
from ggrc.models.mixins import Described
from ggrc.models.mixins import Slugged
from ggrc.models.mixins import Titled
from ggrc.models.object_document import Documentable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable
from ggrc.services.common import Resource


class Request(Assignable, Documentable, Personable, CustomAttributable,
              Relatable, Titled, Slugged, Described, Base, db.Model):
  __tablename__ = 'requests'
  _title_uniqueness = False

  VALID_TYPES = (u'documentation', u'interview')
  VALID_STATES = (u'Open', u'In Progress', u'Finished', u'Verified', u'Final')
  ASSIGNEE_TYPES = (u'Assignee', u'Requester', u'Verifier')

  # TODO Remove requestor and requestor_id on database cleanup
  requestor_id = db.Column(db.Integer, db.ForeignKey('people.id'))
  requestor = db.relationship('Person', foreign_keys=[requestor_id])

  # TODO Remove request_type on database cleanup
  request_type = deferred(db.Column(db.Enum(*VALID_TYPES), nullable=False),
                          'Request')
  # TODO Make status via Stateful Mixin
  status = deferred(db.Column(db.Enum(*VALID_STATES), nullable=False),
                    'Request')
  requested_on = deferred(db.Column(db.Date, nullable=False), 'Request')
  due_on = deferred(db.Column(db.Date, nullable=False), 'Request')
  # TODO Remove audit_id audit_object_id on database cleanup
  audit_id = db.Column(db.Integer, db.ForeignKey('audits.id'), nullable=True)
  audit_object_id = db.Column(db.Integer, db.ForeignKey('audit_objects.id'),
                              nullable=True)
  gdrive_upload_path = deferred(db.Column(db.String, nullable=True),
                                'Request')
  # TODO Remove test and notes columns on database cleanup
  test = deferred(db.Column(db.Text, nullable=True), 'Request')
  notes = deferred(db.Column(db.Text, nullable=True), 'Request')
  # TODO Remove responses on database cleanup
  responses = db.relationship('Response', backref='request',
                              cascade='all, delete-orphan')

  # workaround for title being attached to slug
  @declared_attr
  def title(cls):
    return deferred(db.Column(db.String, nullable=True), cls.__name__)

  _publish_attrs = [
      'requestor',
      'request_type',
      'gdrive_upload_path',
      'requested_on',
      'due_on',
      'status',
      'audit',
      'test',
      'notes',
      'title',
      'description'
  ]
  _sanitize_html = [
      'gdrive_upload_path',
      'test',
      'notes',
      'description',
      'title'
  ]

  _aliases = {
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
      "title": "Request Title",
  }

  def _display_name(self):
    if len(self.title) > 32:
      display_string = self.description[:32] + u'...'
    elif self.title:
      display_string = self.title
    elif len(self.description) > 32:
      display_string = self.description[:32] + u'...'
    else:
      display_string = self.description
    return u'Request with id {0} "{1}" for Audit "{2}"'.format(
        self.id,
        display_string,
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


def _date_has_changes(attr):
  """Date fields are always interpreted as changed because incoming data is
    of type datetime.datetime, while database field has type datetime.date.
    This function normalises this and performs the correct check.
  """
  added, deleted = attr.history.added[0], attr.history.deleted[0]
  if isinstance(added, datetime.datetime):
    added = added.date()
  return not added == deleted


@Resource.model_put.connect_via(Request)
def handle_request_put(sender, obj=None, src=None, service=None):
  all_attrs = set(Request._publish_attrs)
  non_tracked_attrs = {'status', 'requestor'}
  tracked_date_attrs = {'requested_on', 'due_on'}
  tracked_attrs = all_attrs - non_tracked_attrs - tracked_date_attrs
  has_changes = False

  if any(getattr(inspect(obj).attrs, attr).history.has_changes()
         for attr in tracked_attrs):
    has_changes = True

  if any(_date_has_changes(getattr(inspect(obj).attrs, attr))
         for attr in tracked_date_attrs):
    has_changes = True

  if has_changes:
    obj.status = "In Progress"
