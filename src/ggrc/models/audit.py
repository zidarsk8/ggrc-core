# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: vraj@reciprocitylabs.com
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import (
    deferred, Timeboxed, Noted, Described, Hyperlinked, WithContact,
    Titled, Slugged, CustomAttributable
)
from ggrc.models.relationship import Relatable
from ggrc.models.object_person import Personable
from ggrc.models.context import HasOwnContext
from ggrc.models.reflection import AttributeInfo
from ggrc.models.reflection import PublishOnly
from ggrc.models.program import Program
from ggrc.models.person import Person


class Audit(
        CustomAttributable, Personable, HasOwnContext, Relatable,
        Timeboxed, Noted, Described, Hyperlinked, WithContact, Titled, Slugged,
        db.Model):
  __tablename__ = 'audits'
  _slug_uniqueness = False

  VALID_STATES = (
      u'Planned', u'In Progress', u'Manager Review',
      u'Ready for External Review', u'Completed'
  )

  report_start_date = deferred(db.Column(db.Date), 'Audit')
  report_end_date = deferred(db.Column(db.Date), 'Audit')
  audit_firm_id = deferred(
      db.Column(db.Integer, db.ForeignKey('org_groups.id')), 'Audit')
  audit_firm = db.relationship('OrgGroup', uselist=False)
  # TODO: this should be stateful mixin
  status = deferred(db.Column(db.Enum(*VALID_STATES), nullable=False),
                    'Audit')
  gdrive_evidence_folder = deferred(db.Column(db.String), 'Audit')
  program_id = deferred(
      db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False),
      'Audit')
  requests = db.relationship(
      'Request', backref='audit', cascade='all, delete-orphan')
  audit_objects = db.relationship(
      'AuditObject', backref='audit', cascade='all, delete-orphan')
  object_type = db.Column(
      db.String(length=250), nullable=False, default='Control')

  _publish_attrs = [
      'report_start_date',
      'report_end_date',
      'audit_firm',
      'status',
      'gdrive_evidence_folder',
      'program',
      'requests',
      'object_type',
      PublishOnly('audit_objects')
  ]

  _sanitize_html = [
      'gdrive_evidence_folder',
      'description',
  ]

  _include_links = []

  _aliases = {
      "program": {
          "display_name": "Program",
          "filter_by": "_filter_by_program",
          "mandatory": True,
      },
      "user_role:Auditor": {
          "display_name": "Auditors",
          "type": AttributeInfo.Type.USER_ROLE,
          "filter_by": "_filter_by_auditor",
      },
      "status": "Status",
      "start_date": "Planned Start Date",
      "end_date": "Planned End Date",
      "report_start_date": "Planned Report Period from",
      "report_end_date": "Planned Report Period to",
      "contact": {
          "display_name": "Internal Audit Lead",
          "mandatory": True,
          "filter_by": "_filter_by_contact",
      },
      "secondary_contact": None,
      "notes": None,
      "url": None,
      "reference_url": None,
  }

  @classmethod
  def _filter_by_program(cls, predicate):
    return Program.query.filter(
        (Program.id == Audit.program_id) &
        (predicate(Program.slug) | predicate(Program.title))
    ).exists()

  @classmethod
  def _filter_by_auditor(cls, predicate):
    from ggrc_basic_permissions.models import Role, UserRole
    return UserRole.query.join(Role, Person).filter(
        (Role.name == "Auditor") &
        (UserRole.context_id == cls.context_id) &
        (predicate(Person.name) | predicate(Person.email))
    ).exists()

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Audit, cls).eager_query()
    return query.options(
        orm.joinedload('program'),
        orm.subqueryload('requests'),
        orm.subqueryload('object_people').joinedload('person'))
