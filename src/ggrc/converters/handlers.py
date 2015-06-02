# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com


class ColumnHandler(object):

  def __init__(self, importer, key, **options):
    options.setdefault('no_import', False)
    self.importer = importer
    self.base_importer = importer.importer
    self.key = key
    self.options = options

    self.original = None
    self.value = None

    self.errors = []
    self.warnings = []
    # hack for giving haml template the ancestor classes at ALL levels
    from inspect import getmro
    self.ancestor_names = [x.__name__ for x in getmro(self.__class__)]

  def add_error(self, message):
    self.errors.append(message)

  def add_warning(self, message):
    self.warnings.append(message)

  def has_errors(self):
    return any(self.errors) or self.importer.errors.get(self.key)

  def has_warnings(self):
    return any(self.warnings) or self.importer.warnings.get(self.key)

  def display(self):
    value = getattr(self.importer.obj, self.key, '') or ''
    return value if value != 'null' else ''

  def after_save(self, obj):
    pass

  def parse_item(self, value):
    return value

  def validate(self, data):
    if self.options.get('is_required') and data in ("", None):
      missing_column = self.base_importer.get_header_for_column(
          self.base_importer.object_map, self.key)
      self.add_error("{} is required.".format(missing_column))

  def do_import(self, content):
    self.original = content
    if not self.options.get('no_import'):
      self.go_import(content)

  def go_import(self, content):
    # validate first to trigger error in case field is required but None
    # TODO: Unit tests of imports with and without required fields
    self.validate(content)
    if content is not None:
      data = self.parse_item(content)
      if data is not None:
        self.value = data
        self.set_attr(data)

  def set_attr(self, value):
    self.importer.set_attr(self.key, value)

  def export(self):
    return getattr(self.importer.obj, self.key, '')


class StatusColumnHandler(ColumnHandler):

  def parse_item(self, value):
    # compare on fully-lower-cased version of valid states list
    valid_states = self.options.get('valid_states') or self.valid_states
    formatted_valid_states = [
        valid_state.lower() for valid_state in valid_states
    ]
    if value:
      words = value.strip().split()
      formatted_input_state = u" ".join(s.lower() for s in words)
      if formatted_input_state in formatted_valid_states:
        # return the nearest match
        nearest_match_index = formatted_valid_states.index(
            formatted_input_state)
        return valid_states[nearest_match_index]
      else:
        self.add_error('Value must be one of the following: "{}"'.format(
            ", ".join(valid_states)
        ))
        return None
    else:
      default_value = self.options.get('default_value')
      if default_value:
        # default_value should be in valid_states list
        self.add_warning("This field will be set to {}".format(
            default_value))
        return default_value

  def go_import(self, content):
    # override in case empty (None) items need to be set to a default
    if self.options.get('default_value'):
      data = self.parse_item(content)
      self.validate(data)
      self.value = data
      self.set_attr(data)
    else:  # treat as normal if there are no defaults
      return super(StatusColumnHandler, self).go_import(content)


class OwnerColumnHandler(ColumnHandler):

  def go_import(self, content):
    pass


class SlugColumnHandler(ColumnHandler):

  # Dont overwrite slug on object
  def go_import(self, content):
    if content:
      self.value = content
      if self.value in self.base_importer.get_slugs():
        self.add_error('Slug Code is duplicated in CSV')
      else:
        self.validate(content)
        self.base_importer.add_slug_to_slugs(self.value)
      self.value = content
      self.set_attr(content)
    else:
      if self.options.get('is_required'):
        # execute usual validation behavior
        self.validate(content)
      else:
        self.add_warning('Code will be generated on completion of import')


class TitleColumnHandler(ColumnHandler):

  def parse_item(self, value):
    if value:
      value = value.strip()
    return value or ''


