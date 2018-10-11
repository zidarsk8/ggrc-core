# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""A module with Access Control Role object creation hooks.

The hooks in this file ensure that all objects get their proper access control
list entries for the new access control role.

Since we have started creating ACL entries eagerly on object creation, we
always assume that every object will have all it's ACL entries created. But
when we create a new role for a given object type, those ACL entries are
missing and so we create them manually.

Note:
  - This hook creates a big performance degradation on creating a new custom
    role. This is expected and preferable over the lazy creation of ACLs which
    would reduce performance on assigning or removing people from a role.

  - This hook also makes it impossible for us to create a new role and assign
    people to it in the same request! People can only be assigned to a role
    that already existed before the request was sent. Adding a person to a
    new role must now be done in separate requests.
"""

import logging

import sqlalchemy as sa

from ggrc import db
from ggrc import utils
from ggrc.models import all_models
from ggrc.models import inflector
from ggrc.services import signals

logger = logging.getLogger(__name__)


def _get_missing_models_query(role, filter_=False):
  model = inflector.get_model(role.object_type)
  if not model:
    # We only log info instead of warning here because we still leave access
    # control roles of obsolete objects in our database, so that we can use
    # them with old revisions in our history log.
    logger.info("Trying to handle role '%s' for non existent object '%s'",
                role.name, role.object_type)
    return None

  if not filter:
    return model.query.order_by(model.id)

  query = model.query.outerjoin(
      all_models.AccessControlList,
      sa.and_(
          all_models.AccessControlList.object_type == model.__name__,
          all_models.AccessControlList.object_id == model.id,
          all_models.AccessControlList.ac_role_id == role.id
      )
  ).filter(
      all_models.AccessControlList.id.is_(None)
  ).order_by(
      model.id
  )

  return query


def handle_role_acls(role, filter_=False):
  with utils.benchmark("Generating ACL entries on {} for role {}".format(
          role.object_type, role.name)):
    query = _get_missing_models_query(role, filter_=filter_)
    if not query:
      return
    query_generator = utils.generate_query_chunks(
        query,
        chunk_size=1000,
        include_order=False,
    )
    for query_chunk in query_generator:
      for roleable_obj in query_chunk:
        db.session.add(all_models.AccessControlList(
            ac_role=role,
            object=roleable_obj,
        ))
      db.session.commit()


def init_hook():
  """Initialize all hooks"""

  # pylint: disable=unused-variable
  @signals.Restful.model_posted_after_commit.connect_via(
      all_models.AccessControlRole)
  def handle_role_posted(sender, obj=None, src=None, service=None, event=None):
    """Handle ACL entries creation for newly created access control role."""
    handle_role_acls(obj)
