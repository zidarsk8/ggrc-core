# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""REST facade for objects."""
from lib.rest import base_rest_service


def get_obj(obj):
  """Sends request to get the object."""
  return base_rest_service.get_service_by_entity_cls(type(obj)).get(obj)
