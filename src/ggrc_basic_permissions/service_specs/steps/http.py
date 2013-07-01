# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import json
from utils import handle_named_example_resource

@given('a new Role named "{role_name}" is created from json')
def create_role_from_json(context, role_name):
  json_obj = json.loads(context.step)
  handle_named_example_resource(context, 'Role', role_name, **json_obj)
  
