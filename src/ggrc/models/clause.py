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
from ggrc.models.directive import Directive
from ggrc.models.object_document import Documentable
from ggrc.models.object_owner import Ownable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import track_state_for_class
from ggrc.models.track_object_state import HasObjectState


class Clause(HasObjectState, Hierarchical, Noted, Described, Hyperlinked,
             WithContact, Titled, Slugged, Stateful,
             db.Model, CustomAttributable, Documentable,
             Personable, Ownable, Timeboxed, Relatable):

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
  __tablename__ = 'clauses'
  _table_plural = 'clauses'
  _aliases = {
      "url": "Clause URL",
      "description": "Text of Clause",
      "directive": None,
  }

  _title_uniqueness = False

  type = db.Column(db.String)
  na = deferred(db.Column(db.Boolean, default=False, nullable=False),
                'Clause')
  notes = deferred(db.Column(db.Text), 'Clause')

  _publish_attrs = [
      'directive',
      'na',
      'notes',
  ]
  _sanitize_html = ['notes']
  _include_links = []

  @classmethod
  def _filter_by_directive(cls, predicate):
    # FIX THIS
    return Directive.query.filter(
        (Directive.id == cls.directive_id) &
        (predicate(Directive.slug) | predicate(Directive.title))
    ).exists()

  @validates('type')
  def validates_type(self, key, value):
    return self.__class__.__name__

  @classmethod
  def generate_slug_prefix_for(cls, obj):
    # FIX THIS
    from directive import Contract
    if obj.directive and isinstance(obj.directive, Contract):
      return "CLAUSE"
    return super(Clause, cls).generate_slug_prefix_for(obj)

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Clause, cls).eager_query()
    return cls.eager_inclusions(query, Clause._include_links).options(
        orm.joinedload('directive'))

track_state_for_class(Clause)
