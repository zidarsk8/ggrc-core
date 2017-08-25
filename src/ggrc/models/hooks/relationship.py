# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Relationship creation/modification hooks."""

from datetime import datetime

import sqlalchemy as sa

from ggrc.services import signals
from ggrc.models import all_models
from ggrc.models.comment import Commentable
from ggrc.models.mixins import ChangeTracked


def init_hook():
  """Initialize Relationship-related hooks."""
  sa.event.listen(all_models.Relationship, "before_insert",
                  all_models.Relationship.validate_attrs)
  sa.event.listen(all_models.Relationship, "before_update",
                  all_models.Relationship.validate_attrs)

  @signals.Restful.collection_posted.connect_via(all_models.Relationship)
  def handle_comment_mapping(sender, objects=None, **kwargs):
    """Update Commentable.updated_at when Comment mapped."""
    for obj in objects:
      if obj.source_type != u"Comment" and obj.destination_type != u"Comment":
        continue

      comment, other = obj.source, obj.destination
      if comment.type != u"Comment":
        comment, other = other, comment

      if isinstance(other, (Commentable, ChangeTracked)):
        other.updated_at = datetime.now()
