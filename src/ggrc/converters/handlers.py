# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import re
from dateutil.parser import parse

from ggrc.models import Person
from ggrc.login import get_current_user
from ggrc.converters import IMPORTABLE
from ggrc.converters import errors
from ggrc.converters.utils import pretty_class_name


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
    self.display_name = options.get("display_name", "")
    self.value = self.parse_item()

  def add_error(self, message):
    self.row_converter.errors.append(message)

  def add_warning(self, template, **kwargs):
    offset = 3  # 2 header rows and 1 for 0 based index
    block_offset = self.row_converter.converter.offset
    line = self.row_converter.index + block_offset + offset
    message = template.format(line=line, **kwargs)
    self.row_converter.warnings.append(message)

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


class UserColumnHandler(ColumnHandler):

  """ Handler for primary and secondary contacts """

  def parse_item(self):
    email = self.raw_value.strip()
    person = Person.query.filter(Person.email == email).first()
    if email and not person:
      self.add_warning(errors.UNKNOWN_USER_WARNING, email=email)
    return person


class OwnerColumnHandler(ColumnHandler):

  def parse_item(self):
    email_lines = self.raw_value.splitlines()
    owners = []
    owner_emails = filter(unicode.strip, email_lines)  # noqa
    for raw_line in owner_emails:
      email = raw_line.strip()
      person = Person.query.filter(Person.email == email).first()
      if person:
        owners.append(person)
      else:
        self.add_warning(errors.UNKNOWN_USER_WARNING, email=email)

    if not owners:
      self.add_warning(errors.OWNER_MISSING)
      owners.append(get_current_user())

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
    self.key = key
    self.mapping_name = key[4:]  # remove "map:" prefix
    self.mapping_object = IMPORTABLE.get(self.mapping_name)
    super(MappingColumnHandler, self).__init__(row_converter, key, **options)

  def parse_item(self):
    """ Remove multiple spaces and new lines from text """
    class_ = self.mapping_object
    lines = self.raw_value.splitlines()
    slugs = filter(unicode.strip, lines)  # noqa
    objects = []
    for slug in slugs:
      obj = class_.query.filter(class_.slug == slug).first()
      if obj:
        objects.append(obj)
      else:
        self.add_warning(errors.UNKNOWN_OBJECT,
                         object_type=pretty_class_name(class_), slug=slug)

  def set_obj_attr(self):
    """ Create a new mapping object """
    pass


COLUMN_HANDLERS = {
    "slug": SlugColumnHandler,
    "title": TitleColumnHandler,
    "owners": OwnerColumnHandler,
    "status": StatusColumnHandler,
    "contact": UserColumnHandler,
}
