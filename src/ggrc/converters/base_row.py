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
    self.attrs = self.handle_row_data(row, headers)

  def add_error(self, error):
    self.errors.append(error)

  def setup_import(self):
    self.setup_object()

  def setup_export(self):
    pass

  def handle_row_data(self, row, headers):
    """ Pack row data with handlers

    Args:
      row (list of str): row from csv file.

    Returns:
      dict containing handlers with values for all elements in the row.
    """
    if len(headers) != len(row):
      print headers, row
      raise Exception("Error: element count does not match header count")
    items = {}
    for i, (attr_name, header_dict) in enumerate(headers.items()):
      Handler = header_dict["handler"]
      item = Handler(self, attr_name, raw_value=row[i], **header_dict)
      items[attr_name] = item
    return items

  def find_by_slug(self, slug):
    return self.object_type.query.filter_by(slug=slug).first()

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

  def setup_object(self):
    self.obj = self.get_object_by_slug()
    self.reify()

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

  def reify(self):
    """ Set the object values or relate object values

    Set all object attributes to the value specified in attrs. If the value
    is in some related object such as "UserRole" it should be added there and
    handled by the handler defined in attrs.
    """
    if not self.obj:
      raise Exception("Reify object is not set")
    for item_handler in self.attrs.values():
      item_handler.set_obj_attr()
