# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Program model."""

from sqlalchemy import orm
from werkzeug import exceptions as wzg_exceptions


from ggrc import db
from ggrc.fulltext.mixin import Indexed
from ggrc.access_control.roleable import Roleable
from ggrc.models.context import HasOwnContext
from ggrc.models import mixins
from ggrc.models.mixins import base
from ggrc.models.mixins import rest_handable as rest_handable_mixins
from ggrc.models.deferred import deferred
from ggrc.models import object_document
from ggrc.models.object_person import Personable
from ggrc.models import reflection
from ggrc.models import review
from ggrc.models.relationship import Relatable
from ggrc.utils import errors


class Program(review.Reviewable,
              mixins.CustomAttributable,
              object_document.PublicDocumentable,
              Roleable,
              Personable,
              Relatable,
              HasOwnContext,
              mixins.LastDeprecatedTimeboxed,
              rest_handable_mixins.WithDeleteHandable,
              base.ContextRBAC,
              mixins.BusinessObject,
              mixins.Folderable,
              Indexed,
              db.Model):
  """Representation for Program model."""
  __tablename__ = 'programs'

  KINDS = ['Directive']
  KINDS_HIDDEN = ['Company Controls Policy']

  kind = deferred(db.Column(db.String), 'Program')

  audits = db.relationship(
      'Audit', backref='program', cascade='all, delete-orphan')

  _api_attrs = reflection.ApiAttributes(
      'kind',
      reflection.Attribute('audits', create=False, update=False),
      reflection.Attribute('risk_assessments', create=False, update=False),
  )
  _include_links = []
  _aliases = {
      "documents_file": None,
      "owners": None
  }

  @classmethod
  def eager_query(cls):
    query = super(Program, cls).eager_query()
    return cls.eager_inclusions(query, Program._include_links).options(
        orm.subqueryload('audits'),
        orm.subqueryload('risk_assessments'),
    )

  def _check_no_audits(self):
    """Check that audit has no assessments before delete."""
    if self.audits:
      db.session.rollback()
      raise wzg_exceptions.Conflict(errors.MAPPED_AUDITS)

  def handle_delete(self):
    """Handle model_deleted signals."""
    self._check_no_audits()
