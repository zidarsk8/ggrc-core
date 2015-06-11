# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


import ggrc.services
from ggrc import db
from ggrc.services.common import Resource


class RowConverter(object):

  def __init__(self, converter, object_type, **options):
    self.converter = converter
    self.options = options.copy()
    self.object_type = object_type
    self.errors = []
    self.warnings = []
    self.obj = None
    self.is_new = True
    self.ignore = False
    self.index = options.get("index", -1)
    row = options.get("row", [])
    headers = options.get("headers", [])
    self.attrs = {}
    self.mappings = {}
    self.handle_row_data(row, headers)

  def add_error(self, error):
    self.errors.append(error)

  def setup_export(self):
    pass

  def handle_row_data(self, row, headers):
    """ Pack row data with handlers

    Args:
      row (list of str): row from csv file.
    """
    if len(headers) != len(row):
      print headers, row
      raise Exception("Error: element count does not match header count")
    for i, (attr_name, header_dict) in enumerate(headers.items()):
      Handler = header_dict["handler"]
      item = Handler(self, attr_name, raw_value=row[i], **header_dict)
      if attr_name.startswith("map:"):
        self.mappings[attr_name] = item
      else:
        self.attrs[attr_name] = item


  def find_by_slug(self, slug):
    return self.object_type.query.filter_by(slug=slug).first()

  def get_value(self, key):
    key_set = self.mappings if key.startswith("map:") else self.attrs
    item = key_set.get(key)
    if item:
      return item.value
    return None

  def set_ignore(self, ignore=True):
    self.ignore = ignore

  def get_object_by_slug(self):
    """ Get object if the slug is in the system or return a new object """
    if "slug" not in self.attrs:
      return None
    slug = self.attrs["slug"].value
    obj = None
    self.is_new = False
    if slug:
      obj = self.find_by_slug(slug)
    if not obj:
      obj = self.object_type()
      self.is_new = True

    return obj

  def setup_mappings(self, slugs_dict):
    if not self.obj or self.ignore:
      return
    for mapping in self.mappings.values():
      mapping.set_slugs(slugs_dict)
      mapping.set_value()

  def setup_object(self):
    """ Set the object values or relate object values

    Set all object attributes to the value specified in attrs. If the value
    is in some related object such as "UserRole" it should be added there and
    handled by the handler defined in attrs.
    """
    if self.ignore:
      return

    self.obj = self.get_object_by_slug()
    for item_handler in self.attrs.values():
      item_handler.set_obj_attr()

  def send_signals(self):
    service_class = getattr(ggrc.services, self.object_type.__name__)
    if self.is_new:
      Resource.model_posted.send(
          self.object_type, obj=self.obj, src={}, service=service_class)
    else:
      Resource.model_put.send(
          self.object_type, obj=self.obj, src={}, service=service_class)

  def insert_object(self):
    if self.ignore:
      return
    self.send_signals()
    db.session.add(self.obj)

  def insert_mapping(self):
    if not self.obj or self.ignore:
      return
    for mapping in self.mappings.values():
      mapping.set_obj_attr()
