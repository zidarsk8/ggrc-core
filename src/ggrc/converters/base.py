import csv
from .common import *
from ggrc import db
from flask import redirect, flash
class BaseConverter(object):

  def __init__(self, rows_or_objects, **options):

    self.options = options.copy()
    if self.options.get('export'):
      self.objects = rows_or_objects
      self.rows = []
    else:
      self.objects = []
      self.rows = rows_or_objects[:]
    self.all_objects = {}
    self.errors = []
    self.warnings = []
    self.slugs = []
    self.final_results = []
    self.import_exception = None
    self.import_slug = None
    self.create_metadata_map()

  def results(self):
    return self.objects

  def add_slug_to_slugs(self, slug):
    self.slugs.append(slug)

  def get_slugs(self):
    return self.slugs

  def find_object(self, model_class, key):
    all_model_objs = self.all_objects.get(model_class.__class__.__name__)
    return all_model_objs.get(key) if all_model_objs else None

  def add_object(self, model_class, key, newObject):
    self.all_objects[model_class.__name__] = self.all_objects.setdefault(model_class.__name__, dict())
    self.all_objects[model_class.__name__][key] = newObject

  def created_objects(self):
    return [result for result in self.objects if result.id is None]

  def updated_objects(self):
    pass

  def changed_objects(self):
    pass

  def has_errors(self):
    return bool(len(self.errors)) or has_object_errors()

  def has_object_errors(self):
    for obj in self.objects:
      if obj.has_errors(): return True
    return False

  def has_warnings(self):
    return bool(len(self.warnings)) or has_object_warnings()

  def has_object_warnings(self):
   for obj in self.objects:
      if obj.has_warnings(): return True
   return False

  @classmethod
  def from_rows(cls, rows, **options):
    return cls(rows, **options)

  def import_metadata(self):
    if len(self.rows) < 5:
      self.errors.append("There must be at least 5 input lines")
      raise ImportException("Import Error: There must be at least 5 input lines")
    headers = self.read_headers(self.metadata_map, self.rows.pop(0))
    values = self.read_values(headers, self.rows.pop(0))
    self.import_slug = values.get('slug')
    self.rows.pop(0)
    self.rows.pop(0)
    self.validate_metadata(values)

  def read_values(self, headers, row):
    attrs = dict(zip(headers, row))
    return attrs

  def get_header_for_column(self, column_name):
    for header in self.object_map:
      if self.object_map[header] == column_name:
        return header
    return ''

  def read_headers(self, import_map, row):
    ignored_colums = []
    self.trim_list(row)
    keys = []
    for heading in row:
      heading = heading.strip()
      if heading == "<skip>":
        continue
      elif not (heading in import_map):
        ignored_colums.append(heading)
        continue
      else:
        keys.append(import_map[heading])

    if len(ignored_colums):
      ignored_text = ", ".join(ignored_colums)
      self.warnings.append("Ignored column{plural}: {ignored_text}".format(
        plural='s' if len(ignored_colums) > 1 else '', ignored_text=ignored_text))

    missing_columns = import_map.values()
    for element in keys:
      missing_columns.remove(element)

    if len(missing_columns):
      missing_headers = [self.get_header_for_column(temp) for temp in missing_columns if temp is not None]
      missing_text = ", ".join([missing_header for missing_header in missing_headers if missing_header ])
      self.warnings.append("Missing column{plural}: {missing}".format(
        plural='s' if len(missing_columns) > 1 else '', missing = missing_text))

    return keys

  def trim_list(self, a):
    while len(a) > 0 and self.isblank(a[-1]):
      a.pop()

  def isblank(self, string):
    return not len(string) or string.isspace()

  def do_import(self, dry_run = True):

    try:
      self.import_metadata()
      object_headers = self.read_headers(self.object_map, self.rows.pop(0))
      row_attrs = self.read_objects(object_headers, self.rows)

      for index, row_attrs in enumerate(row_attrs):
        row = self.row_converter(self, row_attrs, index)
        row.setup()
        self.final_results.append(row.reify())
        self.objects.append(row)

      if not dry_run:
        self.save_import()

      return self

    except ImportException as e:
      self.import_exception = e
      return self

  def save_import(self):
    db_session = db.session
    for row_converter in self.objects:
      row_converter.save_object(db_session, **self.options)
    db_session.commit()


  def read_objects(self, headers, rows):
    attrs_collection = []
    for row in rows:
      if not len(row):
        continue
      attrs_collection.append(self.read_values(headers, row))
    return attrs_collection

  def validate_metadata(self, attrs):
    print 'validating metadata'
    if self.options.get('directive'):
      self.validate_metadata_type(attrs, self.directive().kind)
      self.validate_code(attrs)

  def validate_code(self, attrs):
    if not attrs.get('slug'):
      self.errors.append('Missing "{}" Code heading'.format(self.directive().kind))
    elif attrs['slug'] != self.directive().slug:
      self.errors.append('{} Code must be {}'.format(self.directive().kind, self.directive().slug))

  def validate_metadata_type(self, attrs, required_type):
    if not attrs.get('type'):
      self.errors.append('Missing "Type" heading')
    elif attrs['type'] != required_type:
      self.errors.append('Type must be "{}"'.format(required_type))

  def do_export(self, csv_writer):
    for i,obj in enumerate(self.objects):
      row = self.row_converter(self, obj, i, export = True)
      row.setup()
      row.reify()
      if row:
        self.rows.append(row.attrs)

    row_header_map = self.object_map
    for row in self.rows:
      csv_row = []
      for key in row_header_map.keys():
        field = row_header_map.get(key)
        csv_row.append(row[field])
      csv_writer.writerow([ele.encode("utf-8") if ele else ''.encode("utf-8") for ele in csv_row])

  def metadata_map(self):
    return self.__class__.metadata_map

  @classmethod
  def metadata_map():
    return self.metadata_map

  def object_map():
    return self.__class__.object_map()

  @classmethod
  def object_map():
    return self.__class__.object_map

  def row_converter():
    return self.__class__.row_converter()

  @classmethod
  def row_converter():
    return self.__class__.row_converter


