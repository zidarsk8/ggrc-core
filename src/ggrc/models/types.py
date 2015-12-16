# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: vraj@reciprocitylabs.com
# Maintained By: vraj@reciprocitylabs.com

"""Declaration of custom ORM data types.

Add Json and Compressed type declaration for use in ORM models.
"""

import json
import pickle
import sqlalchemy.types as types
from ggrc import utils
from ggrc.models import exceptions


class JsonType(types.TypeDecorator):
  # pylint: disable=W0223

  """ Custom Json data type

  Custom type for storing Json objects in our database as serialized text.
  The Limit for the serialized Json is the same as the database text column
  limit (65534).
  """
  impl = types.Text

  def process_result_value(self, value, dialect):
    if value is not None:
      value = json.loads(value)
    return value

  def process_bind_param(self, value, dialect):
    if value is None or isinstance(value, basestring):
      pass
    else:
      value = utils.as_json(value)
      # Detect if the byte-length of the encoded JSON is larger than the
      # database "TEXT" column type can handle
      if len(value.encode('utf-8')) > 65534:
        raise exceptions.ValidationError("Log record content too long")
    return value


class CompressedType(types.TypeDecorator):
  # pylint: disable=W0223

  """ Custom Compresed data type

  Custom type for storing any python object in our database as serialized text.
  """
  impl = types.LargeBinary(length=16777215)

  def process_result_value(self, value, dialect):
    if value is not None:
      value = pickle.loads(value)
    return value

  def process_bind_param(self, value, dialect):
    value = pickle.dumps(value)
    # Detect if the byte-length of the compressed pickle is larger than the
    # database "LargeBinary" column type can handle
    if len(value) > 16777215:
      raise exceptions.ValidationError("Log record content too long")
    return value
