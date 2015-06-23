# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import re
from dateutil.parser import parse
from sqlalchemy import and_
from sqlalchemy import or_

from ggrc import db
from ggrc.models import Person
from ggrc.models import Option
from ggrc.models import Relationship
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
    self.set_value()

  def set_value(self):
    self.value = self.parse_item()

  def get_value(self):
    return getattr(self.row_converter.obj, self.key, self.value)

  def add_error(self, template, **kwargs):
    self.row_converter.add_error(template, **kwargs)

  def add_warning(self, template, **kwargs):
    self.row_converter.add_warning(template, **kwargs)

  def parse_item(self):
    return self.raw_value

  def validate(self):
    if callable(self.validator):
      try:
        self.validator(self.row_converter.obj, self.key, self.value)
      except ValueError:
        self.add_error("invalid status '{}'".format(self.value))
    return True

  def set_obj_attr(self):
    if not self.value:
      return
    setattr(self.row_converter.obj, self.key, self.value)

  def get_default(self):
    if callable(self.default):
      return self.default()
    return self.default

  def insert_object(self):
    """ For inserting fields such as custom attributes and mappings """
    pass


class StatusColumnHandler(ColumnHandler):

  def __init__(self, row_converter, key, **options):
    self.key = key
    valid_states = row_converter.object_type.VALID_STATES
    self.state_mappings = {s.lower(): s for s in valid_states}
    super(StatusColumnHandler, self).__init__(row_converter, key, **options)

  def parse_item(self):
    # TODO: check if mandatory and replace with default if it's wrong
    value = self.raw_value.strip().lower()
    status = self.state_mappings.get(value)
    if not status:
      self.add_warning(errors.WRONG_REQUIRED_VALUE,
                       column_name=self.display_name)
    else:
      status = self.get_default()
    return status


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

    return self.clean_whitespaces(self.raw_value.strip())

  def clean_whitespaces(self, value):
    clean_value = re.sub(r'\s+', " ", value)
    if clean_value != value:
      self.add_warning(errors.WHITESPACE_WARNING,
                       column_name=self.display_name)
    return value


class RequiredTextColumnHandler(TextColumnHandler):

  def parse_item(self):
    value = self.raw_value or ""
    clean_value = self.clean_whitespaces(value.strip())
    if not clean_value:
      self.add_error(errors.MISSING_VALUE_ERROR, column_name=self.display_name)
    return clean_value


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
    self.row_converter = row_converter
    self.key = key
    self.value = None
    self.raw_value = options.get("raw_value")
    self.validator = options.get("validator")
    self.mandatory = options.get("mandatory", False)
    self.default = options.get("default")
    self.description = options.get("description", "")
    self.display_name = options.get("display_name", "")
    self.new_slugs = []

  def set_slugs(self, slugs_dict):
    self.new_slugs = slugs_dict.get(self.row_converter.object_type, [])

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
      elif not (slug in self.new_slugs and
                self.row_converter.converter.dry_run):
        self.add_warning(errors.UNKNOWN_OBJECT,
                         object_type=pretty_class_name(class_), slug=slug)
    return objects

  def set_obj_attr(self):
    """ Create a new mapping object """
    current_obj = self.row_converter.obj
    for obj in self.value:
      if not Relationship.find_related(current_obj, obj):
        mapping = Relationship(source=current_obj, destination=obj)
        db.session.add(mapping)
    db.session.flush()


class CustomAttributeColumHandler(ColumnHandler):
  pass


class OptionColumnHandler(ColumnHandler):

  def parse_item(self):
    prefixed_key = "{}_{}".format(
        self.row_converter.object_type._inflector.table_singular, self.key)
    item = Option.query.filter(
        and_(Option.title == self.raw_value.strip(),
             or_(Option.role == self.key,
                 Option.role == prefixed_key))).first()
    return item


COLUMN_HANDLERS = {
    "slug": SlugColumnHandler,
    "title": RequiredTextColumnHandler,
    "owners": OwnerColumnHandler,
    "status": StatusColumnHandler,
    "contact": UserColumnHandler,
    "secondary_contact": UserColumnHandler,
    "start_date": DateColumnHandler,
    "end_date": DateColumnHandler,
    "report_end_date": DateColumnHandler,
    "report_start_date": DateColumnHandler,
    "verify_frequency": OptionColumnHandler,
    "kind": OptionColumnHandler,
}
