# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from ggrc.models.reflection import AttributeInfo
from .mixins import deferred, BusinessObject, Timeboxed, CustomAttributable
from .object_document import Documentable
from .object_owner import Ownable
from .object_person import Personable
from .relationship import Relatable
from .context import HasOwnContext
from .track_object_state import HasObjectState, track_state_for_class


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
          "display_name": "Owner",
          "mandatory": True,
          "type": AttributeInfo.Type.USER_ROLE,
      },
      "program_editor": {
          "display_name": "Editor",
          "type": AttributeInfo.Type.USER_ROLE,
      },
      "program_reader": {
          "display_name": "Reader",
          "type": AttributeInfo.Type.USER_ROLE,
      },
      "program_mapped": {
          "display_name": "Mapped",
          "type": AttributeInfo.Type.USER_ROLE,
      },
  }

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Program, cls).eager_query()
    return cls.eager_inclusions(query, Program._include_links).options(
        orm.subqueryload('audits'))

track_state_for_class(Program)
