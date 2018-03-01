# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""A module with Comment object creation hooks"""
from sqlalchemy import event

from ggrc.login import get_current_user
from ggrc.models import all_models
from ggrc.access_control import role


def init_hook():
  """Initialize all hooks"""
  # pylint: disable=unused-variable
  @event.listens_for(all_models.Comment, "after_insert")
  def handle_comment_post(mapper, connection, target):
    """Save information on which user created the Comment object."""
    # pylint: disable=unused-argument
    comment_roles = role.get_ac_roles_for(all_models.Comment.__name__)
    comment_admin = comment_roles["Admin"]
    user = get_current_user()
    all_models.AccessControlList(
        ac_role=comment_admin,
        person=user,
        object=target,
    )
