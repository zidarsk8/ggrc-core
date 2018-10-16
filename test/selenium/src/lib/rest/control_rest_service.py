# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""REST service for controls."""
from lib.rest import base_rest_service, rest_convert


def create_control(control):
  """Creates a control."""
  return base_rest_service.create_obj(
      control,
      title=control.title,
      access_control_list=rest_convert.build_access_control_list(control),
      assertions=[rest_convert.to_basic_rest_obj(assertion)
                  for assertion in control.assertions],
      context=rest_convert.default_context())
