# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from collections import defaultdict
from collections import OrderedDict


from ggrc import db
from ggrc.converters import IMPORTABLE
from ggrc.converters.base_row import RowConverter
from ggrc.converters.import_helper import get_object_column_definitions
from ggrc.converters.import_helper import get_column_order
from ggrc.converters.import_helper import extract_relevant_data
from ggrc.converters.import_helper import generate_2d_array
from ggrc.converters.import_helper import pretty_class_name


class Converter(object):

  """ Main converter class for dealing with csv files and data

  Attributes:
    attr_index (dict): reverse index for getting attribute name from
      display_name
    errors (list of str): list containing fatal import errors
    warnings (list of str): list containing import warnings
    ids (list of int): list containing all ids for the converted objects
    rows (list of list of str): 2D array containg csv data
    row_objects (list of RowConverter): list of row convertor objects with
      data from the coresponding row in rows attribute
    headers (dict): A dictionary containing csv headers with additional
      information. Keys are object attributes such as "title", "slug"...
      Example:
        {"slug": {
            "display_name": "Code",
            "mandatory": True,
            "default": "value or a callabe function that returns the value",
            "validator": validator_function,
            "handler": HandlerClass,
            "description": "description or function that returns description"
            "valid_values": "list of valid values"

  """

  @classmethod
  def from_csv(cls, csv_data, dry_run=True):
    object_class = IMPORTABLE.get(csv_data[1][0])
    if not object_class:
      return "ERROR"

    raw_headers, rows = extract_relevant_data(csv_data)

    converter = Converter(object_class, rows=rows, raw_headers=raw_headers,
                          dry_run=dry_run)

    converter.generate_row_converters()
    return converter

  @classmethod
  def from_ids(cls, object_class, ids=[]):
    return Converter(object_class)

  def __init__(self, object_class, **options):
    self.rows = options.get('rows', [])
    self.ids = options.get('ids', [])
    self.dry_run = options.get('dry_run', )
    self.object_class = object_class
    self.errors = []
    self.warnings = []
    self.row_objects = []
    self.row_converters = []
    self.object_headers = get_object_column_definitions(object_class)
    raw_headers = options.get('raw_headers', [])
    self.headers = self.clean_headers(raw_headers)

  def generate_csv_header(self):
    """ Generate 2D array with csv headre description """
    csv_header = generate_2d_array(len(self.object_headers) + 1, 2, value="")
    csv_header[0][0] = "Object type"
    csv_header[1][0] = pretty_class_name(self.object_class)
    column_order = get_column_order(self.object_headers.keys())
    for index, code in enumerate(column_order):
      display_name = self.object_headers[code]["display_name"]
      if self.object_headers[code]["mandatory"]:
        display_name += "*"
      csv_header[0][index + 1] = self.object_headers[code]["description"]
      csv_header[1][index + 1] = display_name
    return csv_header

  def generate_csv_body(self):
    """ Generate 2D array populated with object values """
    return []

  def to_array(self):
    csv_header = self.generate_csv_header()
    csv_body = self.generate_csv_body()
    two_empty_rows = [[], []]
    return csv_header + csv_body + two_empty_rows

  def get_header_names(self):
    """ Get all posible user column names for current object """
    header_names = {
        v["display_name"].lower(): k for k, v in self.object_headers.items()}
    return header_names

  def clean_headers(self, raw_headers):
    """ Sanitize columns from csv file

    Clear out all the bad column headers and remove coresponding column in the
    rows data.

    Args:
      raw_headers (list of str): unmodified header row from csv file

    Returns:
      Ordered Dictionary containing all valid headers
    """
    headers = [val.strip("*").lower() for val in raw_headers]
    clean_headers = OrderedDict()
    header_names = self.get_header_names()
    for index, header in enumerate(headers):
      if header in header_names:
        field_name = header_names[header]
        clean_headers[field_name] = self.object_headers[field_name]
      else:
        self.warnings.append("Unknown column " + header)
        self.remove_culumn(index)
    return clean_headers

  def remove_culumn(self, index):
    """ Remove a column from all rows """
    for row in self.rows:
      row.pop(index)

  def generate_row_converters(self):
    """ Generate a row converter object for every csv row """
    self.row_converters = []
    for i, row in enumerate(self.rows):
      self.row_converters.append(RowConverter(self, self.object_class, row=row,
                                             headers=self.headers, index=i))

  def gather_messages(self):
    messages = {
      "error": [],
      "warnings": [],
      "info": [],
    }
    messages["error"].extend(self.errors)
    messages["warnings"].extend(self.warnings)
    import_count = 0
    for row_converter in self.row_converters:
      messages["error"].extend(row_converter.errors)
      messages["warnings"].extend(row_converter.warnings)
      if not row_converter.errors:
        import_count += 1

    messages["info"].append("{} objects to be imported".format(import_count))
    return messages

  def test_import(self):
    for row_converter in self.row_converters:
      row_converter.setup_import()
      row_converter
    return self.gather_messages()

  def import_objects(self):
    for row_converter in self.row_converters:
      row_converter.setup_import()
      row_converter.insert_object()
    self.commit()
    return self.gather_messages()

  def commit(self):
    pass

  def import_mappings(self):
    pass

  def remove_duplicate_codes(self):
    """ Check for duplacte code entries

    Remove first columns with the same code and return an error """
    duplicate_codes = defaultdict(list)
    for i, row in reversed(list(enumerate(self.rows))):
      code = row[0]
      duplicate_codes[code].append(i)

    errors = []
    bad_rows = set()
    for code, indexes in duplicate_codes.items():
      if len(indexes) > 1:
        keep, ignore = indexes[0], indexes[1:]
        errors.append(
            "Duplicate records: Lines {ignore} and {keep} contain the same "
            "code. Lines {ignore} will be ignored.".format(
                ignore=", ".join(ignore), keep=keep)
        )
      bad_rows.update(ignore)

    result = filter(lambda i, row: i not in bad_rows, enumerate(self.rows))
    return errors, result
