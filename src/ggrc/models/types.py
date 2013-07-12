# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: vraj@reciprocitylabs.com
# Maintained By: vraj@reciprocitylabs.com

import sqlalchemy.types as types
import json
from ggrc.utils import as_json

class JsonType(types.TypeDecorator):
  '''
  Marshals Python structures to and from JSON stored
  as Text in the db
  '''
  impl = types.Text

  def process_result_value(self, value, dialect):
    if value is not None:
      value = json.loads(value)
    return value

  def process_bind_param(self, value, dialect):
    if value is None or isinstance(value, basestring):
      pass
    else:
        value = as_json(value)
    return value
