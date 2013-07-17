# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import json
from behave import given
from ggrc_basic_permissions.models import Role
from tests.ggrc.behave.utils import (
    Example,
    get_service_endpoint_url,
    get_resource,
    handle_named_example_resource,
    )

@given('a new Role named "{role_name}" is created from json')
def create_role_from_json(context, role_name):
  json_obj = json.loads(context.text)
  handle_named_example_resource(context, Role, role_name, **json_obj)
  
@given('existing Role named "{role_name}"')
def retrieve_role_by_name(context, role_name):
  url = get_service_endpoint_url(context, Role)
  response = get_resource(context, url)
  url = '{0}?name={1}'.format(
      get_service_endpoint_url(context, Role), role_name)
  response = get_resource(context, url)
  root = response.json().keys()[0]
  entry_list = response.json()[root][Role.__tablename__]
  assert len(entry_list) == 1
  role = Example('Role', {'role': entry_list[0]})
  setattr(context, role_name, role)
  

