# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

import csv
import chardet
import _csv
from flask import current_app
from StringIO import StringIO

from ggrc.converters import base_row
from ggrc.converters import HANDLERS
from ggrc.converters import COLUMN_ORDER
from ggrc.converters.common import ImportException
from ggrc.models import Directive
from ggrc.models.reflection import AttributeInfo


def get_custom_attributes_definitions(target_class):
  definitions = {}
  custom_attributes = target_class.get_custom_attribute_definitions()
  for attr in custom_attributes:
    handler = HANDLERS.get(attr.title, base_row.ColumnHandler)
    definitions[attr.title] = {
        "attr_name": attr.title,
        "display_name": attr.display_name,
        "mandatory": attr.mandatory,
        "handler": handler,
        "validator": None,
        "default": None,
        "description": "",
    }
  return definitions


def update_definition(definition, values_dict):
  for key, value in values_dict.items():
    if key in definition:
      definition[key] = value


def get_object_column_definitions(target_class):
  definitions = {}
  custom_attr_def = {}
  aliases = AttributeInfo.gather_aliases(target_class)

  custom_attributes = aliases.pop("custom_attributes", None)
  if custom_attributes:
    custom_attr_def = get_custom_attributes_definitions(target_class)

  filtered_aliases = [(k, v) for k, v in aliases.items() if v is not None]

  for key, value in filtered_aliases:

    column = target_class.__table__.columns.get(key)

    definition = {
        "attr_name": key,
        "display_name": value,
        "mandatory": False if column is None else not column.nullable,
        "handler": getattr(target_class, "default_{}".format(key), None),
        "validator": getattr(target_class, "validate_{}".format(key), None),
        "default": HANDLERS.get(key, base_row.ColumnHandler),
        "description": "",
    }

    if type(value) is dict:
      update_definition(definition, value)

    definitions[key] = definition

  definitions.update(custom_attr_def)

  return definitions


def handle_csv_import(converter_class, filepath, **options):
  rows = []
  csv_file = filepath
  if isinstance(filepath, basestring):
    csv_file = open(filepath, 'rbU')

  if options.get('directive_id') and not options.get('directive'):
    options['directive'] = Directive.query.filter_by(
        id=int(options['directive_id'])).first()

  try:
    if isinstance(csv_file, list):
      rows = [row for row in csv_reader(csv_file)]
    else:
      rows = [row for row in csv_reader(csv_file.read().splitlines(True))]
  # Decode error occurs when a special character symbol is inserted in excel.
  except (UnicodeDecodeError, _csv.Error):
    raise ImportException(
        "Could not import: invalid character or spreadsheet encountered;"
        "verify the file is correctly formatted.")
  if not isinstance(csv_file, list):
    csv_file.close()
  converter = converter_class.from_rows(rows, **options)
  # remove 'dry_run' key to allow passing dict w/out keyword arg collision
  # on 'dry_run' parameter:
  is_dry_run = options.get('dry_run', True)
  del options['dry_run']
  return converter.do_import(is_dry_run, **options)


def csv_reader(csv_data, dialect=csv.excel, **kwargs):
  reader = csv.reader(utf_8_encoder(csv_data), dialect=dialect, **kwargs)
  for row in reader:
    yield [unicode(cell, 'utf-8') for cell in row]


def read_csv_file(csv_file):
  if isinstance(csv_file, basestring):
    csv_file = open(csv_file, 'rbU')
  return [row for row in csv_reader(csv_file)]


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


def handle_converter_csv_export(filename, objects, converter_class, **options):
  headers = [
      ('Content-Type', 'text/csv'),
      ('Content-Disposition', 'attachment; filename="{}"'.format(filename))
  ]

  exporter = converter_class(objects, **options)
  output_buffer = StringIO()
  writer = csv.writer(output_buffer)

  for metadata_row in exporter.do_export_metadata():
    writer.writerow([line.encode("utf-8") for line in metadata_row])

  exporter.do_export(writer)
  body = output_buffer.getvalue()
  output_buffer.close()
  return current_app.make_response((body, 200, headers))


def generate_array(width, height, value=None):
  return [[value for _ in range(width)] for _ in range(height)]


def get_column_order(attr_list):
  def sort_index(item):
    if item in COLUMN_ORDER:
      return COLUMN_ORDER.index(item)
    else:
      return len(COLUMN_ORDER)
  return sorted(attr_list, key=sort_index)
