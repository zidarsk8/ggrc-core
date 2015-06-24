# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


import ggrc.services
from ggrc import db
from ggrc.services.common import Resource
from ggrc.converters import errors


class RowConverter(object):

  def __init__(self, converter, object_class, **options):
    self.converter = converter
    self.options = options.copy()
    self.object_class = object_class
    self.obj = None
    self.is_new = True
    self.ignore = False
    self.index = options.get("index", -1)
    self.row = options.get("row", [])
    self.headers = options.get("headers", [])
    self.attrs = {}
    self.mappings = {}
    offset = 3  # 2 header rows and 1 for 0 based index
    self.line = self.index + self.converter.offset + offset

    self.handle_row_data()

  def add_error(self, template, **kwargs):
    message = template.format(line=self.line, **kwargs)
    self.converter.row_errors.append(message)
    self.ignore = True

  def add_warning(self, template, **kwargs):
    message = template.format(line=self.line, **kwargs)
    self.converter.row_warnings.append(message)

  def handle_row_data(self):
    """ Pack row data with handlers """
    if len(self.headers) != len(self.row):
      raise Exception("Error: element count does not match header count")
    for i, (attr_name, header_dict) in enumerate(self.headers.items()):
      Handler = header_dict["handler"]
      item = Handler(self, attr_name, raw_value=self.row[i], **header_dict)
      if attr_name.startswith("map:"):
        self.mappings[attr_name] = item
      else:
        self.attrs[attr_name] = item
    self.obj = self.get_object_by_slug()
    self.chect_mandatory_fields()

  def chect_mandatory_fields(self):
    if not self.is_new:
      return
    mandatory = [key for key, header in self.converter.object_headers.items()
                 if header["mandatory"]]
    missing = set(mandatory).difference(set(self.headers.keys()))
    if missing:
      self.add_error(errors.MISSING_COLUMN,
                     s="s" if len(missing) > 1 else "",
                     column_names=", ".join(missing))

  def find_by_slug(self, slug):
    return self.object_class.query.filter_by(slug=slug).first()

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
    slug = self.get_value("slug")
    if slug is None:
      self.ignore = True
      return
    obj = None
    self.is_new = False
    if slug:
      obj = self.find_by_slug(slug)
    if not obj:
      obj = self.object_class()
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
    if self.ignore:
      return
    self.send_signals()
    db.session.add(self.obj)
    for handler in self.attrs.values():
      handler.insert_object()

  def insert_mapping(self):
    if not self.obj or self.ignore:
      return
    for mapping in self.mappings.values():
      mapping.set_obj_attr()
