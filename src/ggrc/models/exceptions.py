# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Model-related exceptions and related logic."""

import re
from sqlalchemy.exc import IntegrityError


def field_lookup(field_string):
  """Find relevant error field for UNIQUE violation in SQL error message."""
  output_format = "{0}; {0}"
  bad_field = 'code'  # assumes this field as a default
  if field_string.startswith('uq_t_'):
    bad_field = 'title'
  elif field_string.endswith('email'):
    bad_field = 'email'
  elif field_string.endswith('title'):
    bad_field = 'title'
  return output_format.format(bad_field)


def translate_message(exception):
  """
  Translates db exceptions to something a user can understand.
  """
  message = exception.message

  if isinstance(exception, IntegrityError):
    # TODO: Handle not null, foreign key, uniqueness errors with compound keys
    duplicate_entry_pattern = re.compile(
        r'\(1062, u?"Duplicate entry (\'.*\') for key \'([^\']*)\'',
    )
    matches = duplicate_entry_pattern.search(message)
    if matches:
      return (u"The value {value} is already used for another {key} "
              u"values must be unique."
              .format(value=matches.group(1),
                      key=field_lookup(matches.group(2))))

  return message


class ValidationError(Exception):
  pass
