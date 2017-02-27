# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Utility functions for string operations."""

import random
import string
import uuid

BLANK = ''
COMMA = ','  # comma is used as delimiter for multi-choice values
LESS = '<'  # we need exclude this character due to issue GGRC-527
SPECIAL = string.punctuation.replace(COMMA, BLANK).replace(LESS, BLANK)


def random_string(size=5, chars=string.letters + string.digits + SPECIAL):
  """Return string with corresponding size that filled by values from selected
  chars.
  """
  return BLANK.join(random.choice(chars) for position in range(size))


def random_uuid(length=13):
  """Return string with a predefined length base on UUID."""
  return str(uuid.uuid4())[:length]


def random_list_strings(list_len=3, item_size=5,
                        chars=string.letters + string.digits + SPECIAL):
  """Return list of random strings separated by comma."""
  return COMMA.join(random_string(item_size, chars) for i in range(list_len))


def get_bool_from_string(str_to_bool):
  """Return True for 'Yes' and False for 'No'."""
  if str_to_bool.title() == 'Yes':
    return True
  elif str_to_bool.title() == 'No':
    return False
  else:
    raise ValueError("'{}' can't be converted to boolean".format(str_to_bool))


def remap_keys_for_list_dicts(dict_transformation_keys, list_dicts):
  """Remap keys names for old list of dictionaries according the
  transformation dictionary {OLD KEY: NEW KEY} and return the new updated
  list of dictionaries.
  """
  return [{dict_transformation_keys[key]: value for key, value
           in dic.iteritems()} for dic in list_dicts]
