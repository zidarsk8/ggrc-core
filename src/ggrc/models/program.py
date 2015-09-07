# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from ggrc.models.context import HasOwnContext
from ggrc.models.mixins import deferred, BusinessObject, Timeboxed, CustomAttributable
from ggrc.models.object_document import Documentable
from ggrc.models.object_owner import Ownable
from ggrc.models.object_person import Personable, ObjectPerson
from ggrc.models.person import Person
from ggrc.models.reflection import AttributeInfo
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import HasObjectState, track_state_for_class


class Program(HasObjectState, CustomAttributable, Documentable,
              Personable, Relatable, HasOwnContext, Timeboxed,
              Ownable, BusinessObject, db.Model):
  __tablename__ = 'programs'

  KINDS = ['Directive']
  KINDS_HIDDEN = ['Company Controls Policy']

  private = db.Column(db.Boolean, default=False, nullable=False)
  kind = deferred(db.Column(db.String), 'Program')

  audits = db.relationship(
      'Audit', backref='program', cascade='all, delete-orphan')

  _publish_attrs = [
      'kind',
      'audits',
      'private',
  ]
  _include_links = []
  _aliases = {
      "url": "Program URL",
      "private": "Privacy",
      "owners": None,
      "program_owner": {
          "display_name": "Manager",
          "mandatory": True,
          "type": AttributeInfo.Type.USER_ROLE,
          "filter_by": "_filter_by_program_owner",
      },
      "program_editor": {
          "display_name": "Editor",
          "type": AttributeInfo.Type.USER_ROLE,
          "filter_by": "_filter_by_program_editor",
      },
      "program_reader": {
          "display_name": "Reader",
          "type": AttributeInfo.Type.USER_ROLE,
          "filter_by": "_filter_by_program_reader",
      },
      "program_mapped": {
          "display_name": "No Access",
          "type": AttributeInfo.Type.USER_ROLE,
          "filter_by": "_filter_by_program_mapped",
      },
  }

  @classmethod
  def _filter_by_program_owner(cls, predicate):
    return cls._filter_by_role("ProgramOwner", predicate)

  @classmethod
  def _filter_by_program_editor(cls, predicate):
    return cls._filter_by_role("ProgramEditor", predicate)

  @classmethod
  def _filter_by_program_reader(cls, predicate):
    return cls._filter_by_role("ProgramReader", predicate)

  @classmethod
  def _filter_by_program_mapped(cls, predicate):
    return ObjectPerson.query.join(Person).filter(
      (ObjectPerson.personable_type == "Program") &
      (ObjectPerson.personable_id == cls.id) &
      (predicate(Person.email) | predicate(Person.name))
    ).exists()

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Program, cls).eager_query()
    return cls.eager_inclusions(query, Program._include_links).options(
        orm.subqueryload('audits'))

track_state_for_class(Program)
