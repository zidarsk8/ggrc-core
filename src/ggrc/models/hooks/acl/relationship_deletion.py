# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""All hooks required by relationship unmapping"""

import sqlalchemy as sa
from sqlalchemy.orm.session import Session

from ggrc import db
from ggrc.models import all_models


def delete_propagated(propagated_to, propagated_from):
  """Delete propagated roles if they were propagated by a relationship"""
  for acl in getattr(propagated_to, "access_control_list", []):
    if acl.parent is not None and acl.parent.object == propagated_from:
      db.session.delete(acl)


def after_flush(session, _):
  """Delete propagated relationships when the mapping is removed"""
  for obj in session.deleted:
    if not isinstance(obj, all_models.Relationship):
      continue
    delete_propagated(obj.source, obj.destination)
    delete_propagated(obj.destination, obj.source)


def init_hook():
  """Initialize Relationship-related hooks."""
  sa.event.listen(Session, "after_flush", after_flush)
