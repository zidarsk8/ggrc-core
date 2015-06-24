# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from collections import defaultdict
from collections import OrderedDict
from flask import current_app

from ggrc import db
from ggrc.converters import IMPORTABLE
from ggrc.converters.base_row import RowConverter
from ggrc.converters.import_helper import get_object_column_definitions
from ggrc.converters.import_helper import get_column_order
from ggrc.converters.import_helper import extract_relevant_data
from ggrc.converters.import_helper import generate_2d_array
from ggrc.converters.utils import pretty_class_name
from ggrc.converters import errors
from ggrc.converters import get_shared_unique_rules
from ggrc.services.common import get_modified_objects
from ggrc.services.common import update_index
from ggrc.services.common import update_memcache_before_commit
from ggrc.services.common import update_memcache_after_commit


CACHE_EXPIRY_IMPORT = 600


class Converter(object):

  """ Main converter class for dealing with csv files and data

  Attributes:
    attr_index (dict): reverse index for getting attribute name from
      display_name
    block_errors (list of str): list containing fatal import errors
    block_warnings (list of str): list containing blokc level import warnings
    row_errors (list of str): list containing row errors
    row_warnings (list of str): list containing row warnings
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
  def from_csv(cls, csv_data, offset=0, dry_run=True, shared_state=None):
    object_class = IMPORTABLE.get(csv_data[1][0].strip().lower())
    if not object_class:
      converter = Converter()
      converter.add_errors(errors.WRONG_OBJECT_TYPE, line=offset + 2)
      return converter

    raw_headers, rows = extract_relevant_data(csv_data)

    converter = Converter(object_class=object_class, rows=rows,
                          raw_headers=raw_headers, dry_run=dry_run,
                          offset=offset, shared_state=shared_state)

    converter.generate_row_converters()
    return converter

  @classmethod
  def from_ids(cls, object_class, ids=[]):
    return Converter(object_class=object_class)

  def get_unique_counts_dict(self, object_class):
    """ get a the varible for storing unique counts

    Make sure to always return the same variable for object with shared tables,
    as defined in sharing rules.
    """
    sharing_rules = get_shared_unique_rules()
    classes = sharing_rules.get(object_class, object_class)
    if classes not in self.shared_state:
      self.shared_state[classes] = defaultdict(lambda: defaultdict(list))
    return self.shared_state[classes]

  def __init__(self, **options):
    self.rows = options.get('rows', [])
    self.shared_state = options.get('shared_state', {})
    self.offset = options.get('offset', 0)
    self.ids = options.get('ids', [])
    self.dry_run = options.get('dry_run', )
    self.object_class = options.get('object_class', )
    self.block_errors = []
    self.block_warnings = []
    self.row_errors = []
    self.row_warnings = []
    self.row_objects = []
    self.row_converters = []
    if self.object_class:
      self.object_headers = get_object_column_definitions(self.object_class)
      raw_headers = options.get('raw_headers', [])
      self.headers = self.clean_headers(raw_headers)
      self.unique_counts = self.get_unique_counts_dict(self.object_class)
      self.name = self.object_class._inflector.human_singular.title()
      self.ignore = False
    else:
      self.ignore = True
      self.name = ""

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

    def sanitize_header(header):
      header = header.strip("*").lower()
      if header.startswith("map:"):
        header = ":".join(map(unicode.strip, header.split(":")))  # noqa
      return header
    """ Sanitize columns from csv file

    Clear out all the bad column headers and remove coresponding column in the
    rows data.

    Args:
      raw_headers (list of str): unmodified header row from csv file

    Returns:
      Ordered Dictionary containing all valid headers
    """
    headers = [sanitize_header(val) for val in raw_headers]

    clean_headers = OrderedDict()
    header_names = self.get_header_names()
    removed_count = 0
    for index, header in enumerate(headers):
      if header in header_names:
        field_name = header_names[header]
        clean_headers[field_name] = self.object_headers[field_name]
      else:
        self.add_warning(errors.UNKNOWN_COLUMN,
                         line=self.offset + 2,
                         column_name=header)
        self.remove_culumn(index - removed_count)
        removed_count += 1
    return clean_headers

  def remove_culumn(self, index):
    """ Remove a column from all rows """
    for row in self.rows:
      if len(row) > index:
        row.pop(index)

  def generate_row_converters(self):
    """ Generate a row converter object for every csv row """
    self.row_converters = []
    for i, row in enumerate(self.rows):
      row = RowConverter(self, self.object_class, row=row,
                         headers=self.headers, index=i)
      self.row_converters.append(row)
    self.check_uniq_columns()

  def check_uniq_columns(self, counts=None):
    self.generate_unique_counts()
    for key, counts in self.unique_counts.items():
      self.remove_duplicate_keys(key, counts)

  def get_info(self):
    stats = [(r.is_new, r.ignore) for r in self.row_converters]
    info = {
        "name": self.name,
        "rows": len(self.rows),
        "created": stats.count((True, False)),
        "updated": stats.count((False, False)),
        "ignored": stats.count((False, True)) + stats.count((True, True)),
        "block_warnings": self.block_warnings,
        "block_errors": self.block_errors,
        "row_warnings": self.row_warnings,
        "row_errors": self.row_errors,
    }

    return info

  def import_mappings(self, slugs_dict):
    for row_converter in self.row_converters:
      row_converter.setup_mappings(slugs_dict)

    if not self.dry_run:
      for row_converter in self.row_converters:
        row_converter.insert_mapping()
      self.save_import()

  def import_objects(self):
    if self.ignore:
      return

    for row_converter in self.row_converters:
      row_converter.setup_object()

    if not self.dry_run:
      for row_converter in self.row_converters:
        try:
          row_converter.insert_object()
          db.session.flush()
        except Exception as e:
          current_app.logger.error("Import failed with: {}".format(e.message))
          row_converter.add_error(errors.UNKNOWN_ROW_ERROR)
      self.save_import()

  def save_import(self):
    modified_objects = get_modified_objects(db.session)
    update_memcache_before_commit(self, modified_objects, CACHE_EXPIRY_IMPORT)
    db.session.commit()
    update_memcache_after_commit(self)
    update_index(db.session, modified_objects)

  def add_errors(self, template, **kwargs):
    message = template.format(**kwargs)
    self.block_errors.append(message)
    self.ignore = True

  def add_warning(self, template, **kwargs):
    message = template.format(**kwargs)
    self.block_warnings.append(message)

  def get_new_slugs(self):
    slugs = set([row.get_value("slug") for row in self.row_converters])
    return self.object_class, slugs

  def generate_unique_counts(self):
    unique = [key for key, header in self.headers.items() if header["unique"]]
    for key in unique:
      for index, row in enumerate(self.row_converters):
        value = row.get_value(key)
        if value:
          self.unique_counts[key][value].append(index + self.offset + 3)

  def in_range(self, index, remove_offset=True):
    if remove_offset:
      index -= 3 + self.offset
    return index >= 0 and index < len(self.row_converters)

  def remove_duplicate_keys(self, key, counts):

    for value, indexes in counts.items():
      if not any(map(self.in_range, indexes)):
        continue  # ignore duplicates in other related code blocks

      if len(indexes) > 1:
        str_indexes = map(str, indexes)
        self.row_errors.append(
            errors.DUPLICATE_VALUE_IN_CSV.format(
                line_list=", ".join(str_indexes),
                column_name=self.headers[key]["display_name"],
                s="s" if len(str_indexes) > 2 else "",
                value=value,
                ignore_lines=", ".join(str_indexes[1:]),
            )
        )

      for offset_index in indexes[1:]:
        index = offset_index - 3 - self.offset
        if self.in_range(index, remove_offset=False):
          self.row_converters[index].set_ignore()
