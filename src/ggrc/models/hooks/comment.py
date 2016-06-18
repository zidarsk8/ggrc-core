# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""A module with Comment object creation hooks"""

from ggrc import db
from ggrc.login import get_current_user_id
from ggrc.models.all_models import Comment, ObjectOwner
from ggrc.services.common import Resource


def init_hook():
  """Initialize all hooks"""

  # pylint: disable=unused-variable
  @Resource.model_posted_after_commit.connect_via(Comment)
  def handle_comment_post(sender, obj=None, src=None, service=None):
    """Save information on which user created the Comment object

    Args:
      sender: the class of the object that initiated the server request
      obj: the instance of `sender` that initiated the server request
      src: a dictionary containing the POST data sent with request
      service: the server-side API service that handled the request
    Returns:
      None
    """
    # pylint: disable=unused-argument

    creator_id = get_current_user_id()

    obj_owner = ObjectOwner(
        person_id=creator_id,
        ownable_id=obj.id,
        ownable_type=obj.type,
    )

    db.session.add(obj_owner)
