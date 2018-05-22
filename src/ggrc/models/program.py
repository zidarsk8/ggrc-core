# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc import db
from ggrc.fulltext.mixin import Indexed
from ggrc.access_control.roleable import Roleable
from ggrc.models import mixins
from ggrc.models.deferred import deferred
from ggrc.models import object_document
from ggrc.models.object_person import Personable
from ggrc.models import reflection
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import HasObjectState


class Program(HasObjectState,
              mixins.CustomAttributable,
              object_document.PublicDocumentable,
              Roleable,
              Personable,
              Relatable,
              mixins.LastDeprecatedTimeboxed,
              mixins.BusinessObject,
              mixins.Folderable,
              Indexed,
              db.Model):
  __tablename__ = 'programs'

  KINDS = ['Directive']
  KINDS_HIDDEN = ['Company Controls Policy']

  kind = deferred(db.Column(db.String), 'Program')

  audits = db.relationship(
      'Audit', backref='program', cascade='all, delete-orphan')

  _api_attrs = reflection.ApiAttributes(
      'kind',
      reflection.Attribute('audits', create=False, update=False),
  )
  _include_links = []
  _aliases = {
      "documents_url": None,
      "documents_file": None,
      "owners": None
  }

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Program, cls).eager_query()
    return cls.eager_inclusions(query, Program._include_links).options(
        orm.subqueryload('audits'))
