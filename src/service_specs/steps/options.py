# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from behave import given
from tests.ggrc.behave.utils import handle_named_example_resource

@given('an Option named "{name}" with role "{role}"')
def create_option(context, name, role):
  handle_named_example_resource(context, 'Option', name, role=role)
