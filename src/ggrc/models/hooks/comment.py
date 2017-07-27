# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""A module with Comment object creation hooks"""

from ggrc.login import get_current_user
from ggrc.models.all_models import Comment, AccessControlList
from ggrc.access_control import role
from ggrc.services import signals


def init_hook():
  """Initialize all hooks"""
  # pylint: disable=unused-variable
  @signals.Restful.collection_posted.connect_via(Comment)
  def handle_comment_post(sender, objects=None, **kwargs):
    """Save information on which user created the Comment object."""
    # pylint: disable=unused-argument
    user = get_current_user()
    if user.is_anonymous():
      return
    roles = role.get_custom_roles_for(Comment.__name__)
    for role_id, role_name in roles.items():
      if role_name == "Admin":
        for obj in objects:
          AccessControlList(
              ac_role_id=role_id,
              person=user,
              object=obj,
          )
        break
