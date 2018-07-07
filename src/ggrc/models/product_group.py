# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""ProductGroup model."""

from ggrc import db
from ggrc.access_control.roleable import Roleable
from ggrc.fulltext.mixin import Indexed
from ggrc.models.comment import Commentable
from ggrc.models.mixins import (BusinessObject, LastDeprecatedTimeboxed,
                                CustomAttributable, TestPlanned, base)
from ggrc.models.object_document import PublicDocumentable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable
from ggrc.models import track_object_state


class ProductGroup(CustomAttributable, Personable, Roleable,
                   Relatable, PublicDocumentable,
                   track_object_state.HasObjectState, Commentable,
                   TestPlanned, LastDeprecatedTimeboxed,
                   base.ContextRBAC, BusinessObject, db.Model,
                   Indexed):
  """Representation for ProductGroup model."""
  __tablename__ = 'product_groups'
