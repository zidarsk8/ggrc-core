# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: vraj@reciprocitylabs.com
# Maintained By: vraj@reciprocitylabs.com

import re
from sqlalchemy.exc import IntegrityError

def translate_message(exception):
  """
  Translates db exceptions to something a user can understand.
  """
  message = exception.message
  if isinstance(exception, IntegrityError):
    # TODO: Handle not null, foreign key errors, uniqueness errors with compound keys
    duplicate_entry_pattern = re.compile(r'\(1062, u?"Duplicate entry (\'.*\') for key \'([^\']*)\'')
    matches = duplicate_entry_pattern.search(message)
    if matches:
      return u'The value ' + \
        matches.group(1) + \
        u' is already used for a ' + \
        ('title; title' if matches.group(2).startswith('uq_t_') else 'code; code') + \
        u' values must be unique.'
    else:
      return message
  else:
    return message

class ValidationError(Exception):
  pass
