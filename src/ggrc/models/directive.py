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

class Directive(Documentable, Personable, Timeboxed, BusinessObject, db.Model):
  __tablename__ = 'directives'

  version = deferred(db.Column(db.String), 'Directive')
  organization = deferred(db.Column(db.String), 'Directive')
  scope = deferred(db.Column(db.Text), 'Directive')
  kind_id = deferred(db.Column(db.Integer), 'Directive')
  audit_start_date = deferred(db.Column(db.DateTime), 'Directive')
  audit_frequency_id = deferred(db.Column(db.Integer), 'Directive')
  audit_duration_id = deferred(db.Column(db.Integer), 'Directive')
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

  @validates('kind')
  def validate_kind(self, key, value):
    if type(self) is Directive:
      assert self._model_for_kind(value) is not None
    else:
      assert value in self.valid_kinds
    return value

  def kind_model(self):
    return self._model_for_kind(self.kind)

  @classmethod
  def _model_for_kind(cls, kind):
    for model in (Policy, Regulation, Contract):
      if kind in model.valid_kinds:
        return model

  @property
  def kind_plural(self):
    return self.kind_model()._kind_plural

  @property
  def kind_singular(self):
    return self.kind_model().__name__

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
class Policy(Directive):
  _kind_plural = 'policies'
  valid_kinds = ("Company Policy", "Org Group Policy", "Data Asset Policy", "Product Policy", "Contract-Related Policy", "Company Controls Policy")

class Regulation(Directive):
  _kind_plural = 'regulations'
  valid_kinds = ("Regulation",)

class Contract(Directive):
  _kind_plural = 'contracts'
  valid_kinds = ("Contract",)
