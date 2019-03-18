# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module with common validators for GGRC."""

from ggrc import db
from werkzeug import exceptions


def modified_only(func):
  """Decorator that checks if target object is changed in session."""
  def wrapper(mapper, content, target):
    """Skip listener if target object is not modified."""
    if db.session.is_modified(target):
      return func(mapper, content, target)

    return None

  return wrapper


# pylint: disable=unused-argument
def validate_object_type_ggrcq(mapper, content, target):
  """Validate object_type actions for GGRCQ."""
  from ggrc import login as login_module
  from ggrc.models import get_model
  from ggrc.models.mixins import synchronizable

  model = get_model(target.object_type)
  user = login_module.get_current_user(False)

  if not user or user.is_anonymous():
    return

  should_prevent = all([
      issubclass(model, synchronizable.Synchronizable),
      not login_module.is_external_app_user()
  ])

  if should_prevent:
    raise exceptions.MethodNotAllowed()


# pylint: disable=unused-argument
def validate_definition_type_ggrcq(mapper, content, target):
  """Validate GGRCQ action for object with definition_type."""
  from ggrc import login as login_module
  from ggrc.models import get_model
  from ggrc.models.mixins import synchronizable

  model = get_model(target.definition_type)
  user = login_module.get_current_user(False)

  if not user or user.is_anonymous():
    return

  should_prevent = all([
      issubclass(model, synchronizable.Synchronizable),
      not login_module.is_external_app_user()
  ])

  if should_prevent:
    raise exceptions.MethodNotAllowed()
