# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

""" This module is used for handling a single line from a csv file """

from ggrc import db
from ggrc.converters import errors
from ggrc.models.reflection import AttributeInfo
from ggrc.rbac import permissions
from ggrc.services.common import Resource
import ggrc.services


class RowConverter(object):

  def __init__(self, block_converter, object_class, **options):
    self.block_converter = block_converter
    self.options = options.copy()
    self.object_class = object_class
    self.obj = options.get("obj")
    self.from_ids = self.obj is not None
    self.is_new = True
    self.is_delete = False
    self.ignore = False
    self.index = options.get("index", -1)
    self.row = options.get("row", [])
    self.attrs = {}
    self.objects = {}
    self.id_key = ""
    offset = 3  # 2 header rows and 1 for 0 based index
    self.line = self.index + self.block_converter.offset + offset
    self.headers = options.get("headers", [])

  def add_error(self, template, **kwargs):
    message = template.format(line=self.line, **kwargs)
    self.block_converter.row_errors.append(message)
    new_objects = self.block_converter.converter.new_objects[self.object_class]
    key = self.get_value(self.id_key)
    if key in new_objects:
      del new_objects[key]
    self.ignore = True

  def add_warning(self, template, **kwargs):
    message = template.format(line=self.line, **kwargs)
    self.block_converter.row_warnings.append(message)

  def handle_csv_row_data(self, field_list=None):
    """ Pack row data with handlers """
    handle_fields = self.headers if field_list is None else field_list
    for i, (attr_name, header_dict) in enumerate(self.headers.items()):
      if attr_name not in handle_fields or \
          attr_name in self.attrs or \
          self.is_delete:
        continue
      Handler = header_dict["handler"]
      item = Handler(self, attr_name, raw_value=self.row[i], **header_dict)
      if header_dict.get("type") == AttributeInfo.Type.PROPERTY:
        self.attrs[attr_name] = item
      else:
        self.objects[attr_name] = item
      if attr_name in ("slug", "email"):
        self.id_key = attr_name
        self.obj = self.get_or_generate_object(attr_name)
        item.set_obj_attr()

  def handle_obj_row_data(self):
    for i, (attr_name, header_dict) in enumerate(self.headers.items()):
      Handler = header_dict["handler"]
      item = Handler(self, attr_name, **header_dict)
      if header_dict.get("type") == AttributeInfo.Type.PROPERTY:
        self.attrs[attr_name] = item
      else:
        self.objects[attr_name] = item

  def handle_row_data(self, field_list=None):
    if self.from_ids:
      self.handle_obj_row_data()
    else:
      self.handle_csv_row_data(field_list)

  def chect_mandatory_fields(self):
    if not self.is_new or self.is_delete:
      return
    mandatory = [key for key, header in
                 self.block_converter.object_headers.items()
                 if header["mandatory"]]
    missing = set(mandatory).difference(set(self.headers.keys()))
    if missing:
      self.add_error(errors.MISSING_COLUMN,
                     s="s" if len(missing) > 1 else "",
                     column_names=", ".join(missing))

  def find_by_key(self, key, value):
    return self.object_class.query.filter_by(**{key: value}).first()

  def get_value(self, key):
    item = self.attrs.get(key) or self.objects.get(key)
    if item:
      return item.value
    return None

  def set_ignore(self, ignore=True):
    self.ignore = ignore

  def get_or_generate_object(self, attr_name):
    """ fetch existing object if possible or create and return a new one

    Person object is the only exception here since it does not have a slug
    field."""
    value = self.get_value(attr_name)
    new_objects = self.block_converter.converter.new_objects[self.object_class]
    if value in new_objects:
      return new_objects[value]
    obj = self.get_object_by_key(attr_name)
    if value:
      new_objects[value] = obj
    return obj

  def get_object_by_key(self, key="slug"):
    """ Get object if the slug is in the system or return a new object """
    value = self.get_value(key)
    if value is None:
      self.add_error(errors.MISSING_COLUMN, s="", column_names=key)
      return
    obj = None
    self.is_new = False
    if value:
      obj = self.find_by_key(key, value)
    if not obj:
      obj = self.object_class()
      self.is_new = True
    elif not permissions.is_allowed_update_for(obj):
      self.ignore = True
      self.add_error(errors.PERMISSION_ERROR)

    return obj

  def setup_secondary_objects(self, slugs_dict):
    if not self.obj or self.ignore or self.is_delete:
      return
    for mapping in self.objects.values():
      mapping.set_obj_attr()

  def setup_object(self):
    """ Set the object values or relate object values

    Set all object attributes to the value specified in attrs. If the value
    is in some related object such as "UserRole" it should be added there and
    handled by the handler defined in attrs.
    """
    if self.ignore:
      return

    for item_handler in self.attrs.values():
      item_handler.set_obj_attr()

  def send_signals(self):
    service_class = getattr(ggrc.services, self.object_class.__name__)
    service_class.model = self.object_class
    if self.is_new:
      Resource.model_posted.send(
          self.object_class, obj=self.obj, src={}, service=service_class)
    else:
      Resource.model_put.send(
          self.object_class, obj=self.obj, src={}, service=service_class)

  def insert_object(self):
    if self.ignore or self.is_delete:
      return
    else:
      self.send_signals()
      if self.is_new:
        db.session.add(self.obj)
      for handler in self.attrs.values():
        handler.insert_object()

  def insert_secondary_objecs(self):
    if not self.obj or self.ignore or self.is_delete:
      return
    for secondery_object in self.objects.values():
      secondery_object.insert_object()

  def to_array(self, fields):
    row = []
    for field in fields:
      if self.headers[field].get("type") == AttributeInfo.Type.PROPERTY:
        row.append(self.attrs[field].get_value() or "")
      else:
        row.append(self.objects[field].get_value() or "")
    return row
