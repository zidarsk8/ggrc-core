# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Provides access to control assertions."""
from lib import decorator
from lib.entities import app_entity_factory
from lib.rest import base_rest_service


@decorator.memoize
def all_control_assertions():
  """Returns all control assertions."""
  result = []
  assertion_dicts = base_rest_service.get_obj_collection("control_assertions")
  for assertion_dict in assertion_dicts:
    assertion = app_entity_factory.ControlAssertionFactory().create_empty(
        obj_id=assertion_dict["id"],
        name=assertion_dict["name"])
    result.append(assertion)
  return result


def assertion_with_name(name):
  """Returns a control assertion by name."""
  return next(assertion for assertion in all_control_assertions()
              if assertion.name == name)
