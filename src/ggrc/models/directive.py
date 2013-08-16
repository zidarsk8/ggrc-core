# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .associationproxy import association_proxy
from .mixins import deferred, BusinessObject, Timeboxed
from .object_document import Documentable
from .object_person import Personable
from .reflection import PublishOnly

from sqlalchemy.orm import validates

class Directive(Timeboxed, BusinessObject, db.Model):
  __tablename__ = 'directives'

  version = deferred(db.Column(db.String), 'Directive')
  organization = deferred(db.Column(db.String), 'Directive')
  scope = deferred(db.Column(db.Text), 'Directive')
  kind_id = deferred(db.Column(db.Integer), 'Directive')
  audit_start_date = deferred(db.Column(db.DateTime), 'Directive')
  audit_frequency_id = deferred(db.Column(db.Integer), 'Directive')
  audit_duration_id = deferred(db.Column(db.Integer), 'Directive')
  meta_kind = db.Column(db.String)
  kind = deferred(db.Column(db.String), 'Directive')

  sections = db.relationship(
      'Section', backref='directive', order_by='Section.slug', cascade='all, delete-orphan')
  controls = db.relationship( 'Control', backref='directive', order_by='Control.slug')
  program_directives = db.relationship('ProgramDirective', backref='directive', cascade='all, delete-orphan')
  programs = association_proxy(
      'program_directives', 'program', 'ProgramDirective')
  audit_frequency = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Directive.audit_frequency_id) == Option.id, '\
                       'Option.role == "audit_frequency")',
      uselist=False,
      )
  audit_duration = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Directive.audit_duration_id) == Option.id, '\
                       'Option.role == "audit_duration")',
      uselist=False,
      )

  __mapper_args__ = {
      'polymorphic_on': meta_kind
      }

  _publish_attrs = [
      'audit_start_date',
      'audit_frequency',
      'audit_duration',
      'controls',
      'kind',
      'organization',
      'programs',
      PublishOnly('program_directives'),
      'scope',
      'sections',
      'version',
      ]
  _sanitize_html = [
      'organization',
      'scope',
      'version',
      ]

  @validates('kind')
  def validate_kind(self, key, value):
    assert value in self.valid_kinds
    return value

  @validates('audit_duration', 'audit_frequency')
  def validate_options(self, key, option):
    assert option is None or option.role == key
    return option

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Directive, cls).eager_query()
    return query.options(
        orm.joinedload('audit_frequency'),
        orm.joinedload('audit_duration'),
        orm.subqueryload('controls'),
        orm.subqueryload_all('program_directives.program'),
        orm.subqueryload('sections'))

# FIXME: For subclasses, restrict kind
class Policy(Documentable, Personable, Directive):
  __mapper_args__ = {
      'polymorphic_identity': 'Policy'
      }
  _table_plural = 'policies'
  valid_kinds = (
      "Company Policy", "Org Group Policy", "Data Asset Policy",
      "Product Policy", "Contract-Related Policy", "Company Controls Policy"
      )

  @validates('meta_kind')
  def validates_meta_kind(self, key, value):
    return 'Policy'

class Regulation(Documentable, Personable, Directive):
  __mapper_args__ = {
      'polymorphic_identity': 'Regulation'
      }
  _table_plural = 'regulations'
  valid_kinds = ("Regulation",)

  @validates('meta_kind')
  def validates_meta_kind(self, key, value):
    return 'Regulation'

class Contract(Documentable, Personable, Directive):
  __mapper_args__ = {
      'polymorphic_identity': 'Contract'
      }
  _table_plural = 'contracts'
  valid_kinds = ("Contract",)

  @validates('meta_kind')
  def validates_meta_kind(self, key, value):
    return 'Contract'
