# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""REST service for people."""
from lib.rest import base_rest_service, rest_convert


def create_person(person):
  """Creates a person."""
  return base_rest_service.create_obj(
      person,
      name=person.name,
      email=person.email,
      context=rest_convert.default_context())
