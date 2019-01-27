# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Factories for app entities in control.py."""
from lib import users
from lib.app_entity import control_entity
from lib.app_entity_factory import _base


class ControlFactory(_base.BaseFactory):
  """Factory for Control entities."""
  _entity_cls = control_entity.Control

  @property
  def _empty_attrs(self):
    """See superclass."""
    return {
        "admins": [],
        "assertions": [],
        "comments": []
    }

  @property
  def _default_attrs(self):
    """See superclass."""
    from lib.rest_services import control_rest_service
    return {
        "title": self._obj_title,
        "admins": [users.current_person()],
        "assertions": [control_rest_service.assertion_with_name("Security")]
    }


class ControlAssertionFactory(_base.BaseFactory):
  """Factory for Control Assertions."""
  _entity_cls = control_entity.ControlAssertion
