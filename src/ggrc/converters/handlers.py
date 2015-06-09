# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import re
from dateutil.parser import parse
from inspect import getmro

from ggrc.models import Person
from ggrc.converters import IMPORTABLE


class ColumnHandler(object):

  def __init__(self, row_converter, key, **options):
    self.row_converter = row_converter
    self.key = key
    self.value = None
    self.raw_value = options.get("raw_value")
    self.validator = options.get("validator")
    self.mandatory = options.get("mandatory", False)
    self.default = options.get("default")
    self.description = options.get("description", "")
    self.display_name = options.get("description", "")

    self.errors = []
    self.warnings = []
    self.set_value()

  def set_value(self):
    self.value = self.parse_item()

  def add_error(self, message):
    self.errors.append(message)

  def add_warning(self, message):
    self.warnings.append(message)

  def has_errors(self):
    return any(self.errors) or self.row_converter.errors.get(self.key)

  def has_warnings(self):
    return any(self.warnings) or self.row_converter.warnings.get(self.key)

  def display(self):
    value = getattr(self.row_converter.obj, self.key, '') or ''
    return value if value != 'null' else ''

  def parse_item(self):
    return self.raw_value

  def validate(self):
    if self.validator:
      try:
        self.validator(self.row_converter.obj, self.key, self.value)
      except ValueError:
        self.row_converter.add_error("invalid status '{}'".format(self.value))
    return True

  def set_obj_attr(self):
    if not self.value:
      return
    if not self.validate():
      return

    setattr(self.row_converter.obj, self.key, self.value)

  def export(self):
    return getattr(self.row_converter.obj, self.key, '')


class StatusColumnHandler(ColumnHandler):

  def parse_item(self):
    if self.raw_value:
      return self.raw_value.strip()


class OwnerColumnHandler(ColumnHandler):

  def parse_item(self):
    owner_emails = self.raw_value.splitlines()
    owners = []
    for email in owner_emails:
      person = Person.query.filter(Person.email == email).first()
      if person:
        owners.append(person)
      else:
        self.add_warning("unknown owner {}".format(email))

    if not owners:
      self.add_error("no valid owners found")

    return owners

  def set_obj_attr(self):
    if self.value:
      for owner in self.value:
        self.row_converter.obj.owners.append(owner)


class SlugColumnHandler(ColumnHandler):

  def parse_item(self):
    if self.raw_value:
      return self.raw_value.strip()
    return ""


class DateColumnHandler(ColumnHandler):

  def parse_item(self):
    try:
      return parse(self.raw_value)
    except:
      self.add_error(
          u"Unknown date format, use YYYY-MM-DD or MM/DD/YYYY format")


class TextColumnHandler(ColumnHandler):

  """ Single line text field handler """

  def parse_item(self):
    """ Remove multiple spaces and new lines from text """
    if not self.raw_value:
      return ""
    stripped_value = self.raw_value.strip()
    clean_value = re.sub(r'\s+', " ", stripped_value)
    if clean_value != stripped_value:
      self.add_warning("Some whitespace characters were removed")

    return clean_value


class TitleColumnHandler(TextColumnHandler):

  """ Handle unique titles """

  def validate(self):
    return True


class TextareaColumnHandler(ColumnHandler):

  """ Multi line text field handler """

  def parse_item(self):
    """ Remove multiple spaces and new lines from text """
    if not self.raw_value:
      return ""

    return re.sub(r'\s+', " ", self.raw_value).strip()


class MappingColumnHandler(ColumnHandler):

  """ Handler for mapped objects """

  def __init__(self, row_converter, key, **options):
    super(MappingColumnHandler, self).__init__(row_converter, key, **options)
    self.key = key
    self.mapping_name = key[4:]  # remove "map:" prefix
    self.mapping_object = IMPORTABLE.get(self.mapping_name)

  def parse_item(self):
    """ Remove multiple spaces and new lines from text """
    if not self.raw_value:
      return ""

    return re.sub(r'\s+', " ", self.raw_value).strip()

  def set_obj_attr(self):
    """ Create a new mapping object """
    pass


COLUMN_HANDLERS = {
    "slug": SlugColumnHandler,
    "title": TitleColumnHandler,
    "owners": OwnerColumnHandler,
    "status": StatusColumnHandler,
}
