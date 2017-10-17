# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""A module with Comment object creation hooks"""
import logging

from sqlalchemy import event

from ggrc.login import get_current_user
from ggrc.models.all_models import Comment, AccessControlList
from ggrc.access_control import role
from ggrc.services import signals

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def init_hook():
  """Initialize all hooks"""
  # pylint: disable=unused-variable
  @event.listens_for(Comment, "after_insert")
  def handle_comment_post(mapper, connection, target):
    """Save information on which user created the Comment object."""
    # pylint: disable=unused-argument
    for role_id, role_name in role.get_custom_roles_for(target.type).items():
      user = get_current_user()
      if role_name == "Admin" and not user.is_anonymous():
        AccessControlList(
            ac_role_id=role_id,
            person=user,
            object=target,
        )
        return

  @signals.Restful.model_posted_after_commit.connect_via(Comment)
  def handle_assessment_after_commit(
      sender, obj=None, src=None, service=None, event=None):
    logger.info('------> handle_comment_after_commit: %s', (
        sender, obj, src, service, event))
