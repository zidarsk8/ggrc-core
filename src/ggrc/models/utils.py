# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
from .exceptions import ValidationError

def validate_option(model, attribute, option, desired_role):
  if option and option.role != desired_role:
    message = "Invalid value for attribute {}.{}. "\
    "Expected option with role {}, received role {}.".format(model, attribute, desired_role, option.role)
    raise ValidationError(message)
  return option
