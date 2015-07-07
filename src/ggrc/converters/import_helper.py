# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import csv
import chardet
from StringIO import StringIO
from sqlalchemy.sql.schema import UniqueConstraint

from ggrc.utils import get_mapping_rules
from ggrc.converters.handlers import COLUMN_HANDLERS
from ggrc.converters import COLUMN_ORDER
from ggrc.converters import handlers
from ggrc.converters.utils import pretty_name
from ggrc.models.reflection import AttributeInfo


def get_mapping_definitions(object_class):
  definitions = {}
  mapping_rules = get_mapping_rules()
  if object_class.__name__ not in mapping_rules:
    return {}

  for mapping_class in mapping_rules[object_class.__name__]:
    class_name = pretty_name(mapping_class)
    mapping_name = "map:{}".format(class_name)
    definitions[mapping_name.lower()] = {
        "display_name": mapping_name,
        "mandatory": False,
        "handler": handlers.MappingColumnHandler,
        "validator": None,
        "default": None,
        "unique": False,
        "description": "",
    }

  return definitions


def get_custom_attributes_definitions(object_class):
  definitions = {}
  if not hasattr(object_class, "get_custom_attribute_definitions"):
    return definitions
  custom_attributes = object_class.get_custom_attribute_definitions()
  for attr in custom_attributes:
    handler = handlers.CustomAttributeColumHandler
    definitions[attr.title] = {
        "display_name": attr.title,
        "mandatory": attr.mandatory,
        "handler": handler,
        "validator": None,
        "default": None,
        "unique": False,
        "description": "",
        "custom": True,
    }
  return definitions


def update_definition(definition, values_dict):
  for key, value in values_dict.items():
    if key in definition:
      definition[key] = value


def get_unique_constraints(object_class):
  """ Return a set of attribute names for single unique columns """
  constraints = object_class.__table__.constraints
  unique = filter(lambda x: isinstance(x, UniqueConstraint), constraints)
  # we only handle single column unique constraints
  unique_columns = [u.columns.keys() for u in unique if len(u.columns) == 1]
  return set(sum(unique_columns, []))


def get_object_column_definitions(object_class):
  definitions = {}

  aliases = AttributeInfo.gather_aliases(object_class)
  filtered_aliases = [(k, v) for k, v in aliases.items() if v is not None]

  unique_columns = get_unique_constraints(object_class)

  for key, value in filtered_aliases:
    column = object_class.__table__.columns.get(key)
    definition = {
        "display_name": value,
        "mandatory": False if column is None else not column.nullable,
        "default": getattr(object_class, "default_{}".format(key), None),
        "validator": getattr(object_class, "validate_{}".format(key), None),
        "handler": COLUMN_HANDLERS.get(key, handlers.ColumnHandler),
        "unique": key in unique_columns,
        "description": "",
    }
    if type(value) is dict:
      update_definition(definition, value)
    definitions[key] = definition

  custom_attr_def = get_custom_attributes_definitions(object_class)
  mapping_def = get_mapping_definitions(object_class)
  definitions.update(custom_attr_def)
  definitions.update(mapping_def)

  return definitions


def get_object_column_json(object_class):
  definitions = get_object_column_definitions(object_class)
  for attr_name, attr_info in definitions.items():
    for key, value in attr_info.items():
      if type(value) not in (unicode, str, int, long, bool, None):
        del definitions[attr_name][key]
  order = get_column_order(definitions.keys())
  result = []
  for key in order:
    item = definitions[key]
    item["attr_name"] = key
    result.append(item)
  return result


def get_column_order(attr_list):
  """ Sort attribute list

  Attribute list should be sorted with 3 rules:
    - attributes in COLUMN_ORDER variable must be fist and in the same
      order as defined in that variable.
    - Custom Attributes are sorted alphabetically after default attributes
    - mapping attributes are sorted alphabetically and placed last
  """
  attr_set = set(attr_list)
  default_attrs = [v for v in COLUMN_ORDER if v in attr_set]
  default_set = set(default_attrs)
  other_attrs = [v for v in attr_list if v not in default_set]
  custom_attrs = [v for v in other_attrs if not v.lower().startswith("map:")]
  mapping_attrs = [v for v in other_attrs if v.lower().startswith("map:")]
  custom_attrs.sort(key=lambda x: x.lower())
  mapping_attrs.sort(key=lambda x: x.lower())
  return default_attrs + custom_attrs + mapping_attrs


def generate_csv_string(csv_data):
  output_buffer = StringIO()
  writer = csv.writer(output_buffer)

  csv_data = equalize_array(csv_data)
  csv_data = utf_8_encode_array(csv_data)

  for row in csv_data:
    writer.writerow(row)

  body = output_buffer.getvalue()
  output_buffer.close()
  return body


def extract_relevant_data(csv_data):
  """ Split csv data into data and metadata """
  striped_data = [map(unicode.strip, line) for line in csv_data]
  transpose_data = zip(*striped_data[1:])
  non_empty = filter(any, transpose_data)
  data = zip(*non_empty[1:])
  column_definitions = list(data.pop(0))
  data = map(list, data)
  return column_definitions, data


def equalize_array(array):
  """ Expand all rows of 2D array to the same lenght """
  if len(array) == 0:
    return array
  max_length = max(map(len, array))
  for row in array:
    diff = max_length - len(row)
    row.extend([""] * diff)
  return array


def split_array(csv_data):
  """ Split array by empty lines """
  data_blocks = []
  offsets = []
  current_block = None
  for ofset, line in enumerate(csv_data):
    if sum(map(len, line)) > 0:
      if current_block is None:
        offsets.append(ofset)
        data_blocks.append([])
        current_block = len(data_blocks) - 1
      data_blocks[current_block].append(line)
    else:
      current_block = None

  return offsets, data_blocks


def generate_2d_array(width, height, value=None):
  """ Generate 2D array of size width x height """
  return [[value for _ in range(width)] for _ in range(height)]


def csv_reader(csv_data, dialect=csv.excel, **kwargs):
  reader = csv.reader(utf_8_encoder(csv_data), dialect=dialect, **kwargs)
  for row in reader:
    yield [unicode(cell, 'utf-8') for cell in row]  # noqa


def read_csv_file(csv_file):
  if isinstance(csv_file, basestring):  # noqa
    csv_file = open(csv_file, 'rbU')
  return [row for row in csv_reader(csv_file)]


def utf_8_encode_array(array):
  """ encode 2D array to utf8 """
  return [[val.encode("utf-8") for val in line] for line in array]


def utf_8_encoder(csv_data):
  """This function is a generator that attempts to encode the string as utf-8.
  It is assumed that the data is likely to be encoded in ascii. If encoding
  fails, however, the function will attempt to guess the encoding and convert
  it to utf-8.
  Guessing is only done when a line fails to encode as there may be characters
  further in the stream that aren't valid ascii and encoding is performed per
  line yielded; guessing is the fallback on a per-line basis.
  """
  for line in csv_data:
    try:
      yield line.decode('utf-8').encode('utf-8')
    except UnicodeDecodeError:
      encoding_guess = chardet.detect(line)['encoding']
      yield line.decode(encoding_guess).encode('utf-8')
