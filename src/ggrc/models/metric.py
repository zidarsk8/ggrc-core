# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Metric model."""

from ggrc import db
from ggrc.access_control.roleable import Roleable
from ggrc.fulltext.mixin import Indexed
from ggrc.models.comment import Commentable
from ggrc.models.mixins import (BusinessObject, LastDeprecatedTimeboxed,
                                CustomAttributable, TestPlanned)
from ggrc.models.mixins.base import ContextRBAC
from ggrc.models.object_document import PublicDocumentable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable
from ggrc.models import track_object_state


class Metric(Personable, Roleable, Relatable,
             PublicDocumentable, track_object_state.HasObjectState,
             Commentable, TestPlanned, LastDeprecatedTimeboxed,
             CustomAttributable, BusinessObject, Indexed, ContextRBAC,
             db.Model):
  """Representation for Metric model."""
  __tablename__ = 'metrics'
