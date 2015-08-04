# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: vraj@reciprocitylabs.com

from sqlalchemy.orm import validates

from ggrc import db
from ggrc.models.exceptions import ValidationError
from ggrc.models.mixins import (
    deferred, Hierarchical, Noted, Described, Hyperlinked, WithContact,
    Titled, Slugged, CustomAttributable, Stateful, Timeboxed
)
from ggrc.models.object_document import Documentable
from ggrc.models.object_owner import Ownable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import track_state_for_class
from ggrc.models.track_object_state import HasObjectState


class SectionBase(HasObjectState, Hierarchical, Noted, Described, Hyperlinked,
                  WithContact, Titled, Slugged, Stateful, db.Model):
  VALID_STATES = [
      'Draft',
      'Final',
      'Effective',
      'Ineffective',
      'Launched',
      'Not Launched',
      'In Scope',
      'Not in Scope',
      'Deprecated',
  ]
  _table_plural = 'section_bases'
  __tablename__ = 'sections'
  _title_uniqueness = False

  type = db.Column(db.String)
  directive_id = deferred(
      db.Column(db.Integer, db.ForeignKey('directives.id'), nullable=True),
      'SectionBase')
  na = deferred(db.Column(db.Boolean, default=False, nullable=False),
                'SectionBase')
  notes = deferred(db.Column(db.Text), 'SectionBase')

  __mapper_args__ = {
      'polymorphic_on': type
  }

  _publish_attrs = [
      'directive',
      'na',
      'notes',
  ]
  _sanitize_html = ['notes']
  _include_links = []
  _aliases = {"directive": "Policy / Regulation / Standard"}

  @validates('type')
  def validates_type(self, key, value):
    return self.__class__.__name__

  @classmethod
  def generate_slug_prefix_for(cls, obj):
    from directive import Contract
    if obj.directive and isinstance(obj.directive, Contract):
      return "CLAUSE"
    return super(SectionBase, cls).generate_slug_prefix_for(obj)

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(SectionBase, cls).eager_query()
    return cls.eager_inclusions(query, SectionBase._include_links).options(
        orm.joinedload('directive'))

track_state_for_class(SectionBase)


class Section(CustomAttributable, Documentable, Personable,
              Ownable, Relatable, SectionBase):
  __mapper_args__ = {
      'polymorphic_identity': 'Section'
  }
  _table_plural = 'sections'
  _aliases = {
      "url": "Section URL",
      "description": "Text of Section",
  }

  @validates('directive_id')
  def validates_directive_id(self, key, value):
    if self.directive_id:
      return self.directive_id
    raise ValidationError("Directive is required for sections")

  def log_json(self):
    out_json = super(Section, self).log_json()
    # so that event log can refer to deleted directive
    out_json["mapped_directive"] = self.directive.display_name
    return out_json


class Clause(CustomAttributable, Documentable, Personable, Ownable,
             Timeboxed, Relatable, SectionBase):
  __mapper_args__ = {
      'polymorphic_identity': 'Clause'
  }
  _table_plural = 'clauses'
  _aliases = {
      "url": "Clause URL",
      "description": "Text of Clause",
      "directive": None,
  }
