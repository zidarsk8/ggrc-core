# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Utility functions for string operations."""

import random
import string
import uuid
from collections import defaultdict


BLANK = ''
COMMA = ','  # comma is used as delimiter for multi-choice values
LESS = '<'  # need exclude this character due to issue GGRC-527
DOUBLE_QUOTES = '"'  # need exclude this character due to issue GGRC-931
BACKSLASH = '\\'  # need exclude this character due to issue GGRC-931
EXCLUDE = COMMA + LESS + DOUBLE_QUOTES + BACKSLASH
SPECIAL = BLANK.join(_ for _ in string.punctuation if _ not in EXCLUDE)


def random_string(size=5, chars=string.letters + string.digits + SPECIAL):
  """Return string with corresponding size that filled by values from selected
 chars.
 """
  return BLANK.join(random.choice(chars) for position in range(size))


def random_uuid(length=13):
  """Return string with predefined length base on UUID."""
  return str(uuid.uuid4())[:length]


def random_list_strings(list_len=3, item_size=5,
                        chars=string.letters + string.digits + SPECIAL):
  """Return list of random strings separated by comma."""
  return COMMA.join(random_string(item_size, chars) for i in range(list_len))


def get_bool_from_string(str_to_bool):
  """Return True for 'Yes' or 'True' and False for 'No' or 'False'
  for string and unicode 'str_to_bool', else return source value
  of 'str_to_bool'.
  """
  return ((True if str_to_bool.title() in ['Yes', "True"] else
           False if str_to_bool.title() in ['No', "False"] else str_to_bool)
          if isinstance(str_to_bool, (str, unicode)) else str_to_bool)


def remap_keys_for_list_dicts(dict_of_transform_keys, list_dicts):
  """Remap keys names for old list of dictionaries according
  transformation dictionary {OLD KEY: NEW KEY} and return new updated
  list of dictionaries.
  """
  return [
      {(dict_of_transform_keys[k] if dict_of_transform_keys.get(k) else k): v
       for k, v in dic.iteritems()} for dic in list_dicts]


def convert_to_list(items):
  """Converts items to list items:
  - if items are already list items then skip;
  - if are not list items then convert to list items."""
  list_items = items if isinstance(items, list) else [items, ]
  return list_items


def convert_list_elements_to_list(list_to_convert):
  """Converts list elements in list to sequence of elements:
  Example: [1, 2, 3, [4, 5], 6, [7]] = [1, 2, 3, 4, 5, 6, 7]
  """
  converted_list = []
  for element in list_to_convert:
    if isinstance(element, list):
      converted_list.extend(element)
    else:
      converted_list.append(element)
  return converted_list


def merge_dicts_by_same_key(*dicts):
  """Merger multiple (at list two) dictionaries with the same keys to one witch
  will be contain keys (all values from source dicts) and values (all values
  from destination dicts).
  Example:
  :arg *dicts = ({1: 55, 2: 66}, {2: 67, 1: 56})
  :return {55: 56, 66: 67}
  """
  merged_dict = defaultdict(list)
  for _dict in dicts:
    if isinstance(_dict, dict):
      for key, val in _dict.iteritems():
        merged_dict[key].append(val)
  if merged_dict != {None: [None, None]}:
    merged_dict = {
        key: val for key, val in merged_dict.iteritems() if
        val and len(val) == 2}
  return dict([tuple(item) for item in merged_dict.values()])


def is_one_dict_is_subset_another_dict(src_dict, dest_dict):
  """Check is all items of one dictionary 'src_dict' is subset of items of
  another dictionary 'dest_dict', where 'src_dict' should has same or less
  length then 'dest_dict'.
  Examples:
  ({"b": 2, "a": 1}, {"a": 1, "b": 2, "c": 4}) = True
  ({"a": 1, "b": 2, "c": 4}, {"b": 2, "a": 1}) = False
  """
  # pylint: disable=invalid-name
  return not bool(set(src_dict) - set(dest_dict))
