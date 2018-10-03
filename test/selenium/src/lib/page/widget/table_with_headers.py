# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Generic classes to represent table with headers."""
import inflection

from lib import decorator


class TableWithHeaders(object):
  """Represents generic table with headers."""

  def __init__(self, container, header_locator, table_rows):
    self._root = container
    self._header_locator = header_locator
    self._table_rows = table_rows

  def table_header_names(self):
    """Returns names of table headers."""
    # JS `text_content` is used as displayed text is capitalized using CSS
    return [el.text_content for el in self._root.elements(
        **self._header_locator)]

  def get_table_row_by(self, **conditions):
    """Returns a table row that matches conditions."""
    for table_row in self._table_rows():
      if table_row.matches_conditions(**conditions):
        return table_row
    return None


class TableRow(object):
  """Represents generic row of the table."""

  def __init__(self, container, table_header_names, cell_locator,
               header_attr_mapping=None):
    self.root = container
    self._headers = table_header_names
    self._cell_locator = cell_locator
    self._header_attr_mapping = header_attr_mapping or {}

  @property
  def _attr_header_mapping(self):
    """Returns reversed `header_attr_mapping`."""
    return {v: k for k, v in self._header_attr_mapping.iteritems()}

  def obj_dict(self, row_obj):
    """Returns a dict where:
    * keys are column headers (in lowercase, underscored) or attrs from
    `self._header_attr_mapping`
    * values are text of these headers or object methods.
    """
    result = {}
    for header_name in self._headers:
      attr_name = self._attr_name_for_header_name(header_name)
      if hasattr(row_obj, attr_name):
        value = getattr(row_obj, attr_name)()
      else:
        value = self.text_for_header(header_name)
      result[attr_name] = value
    return result

  def _attr_name_for_header_name(self, header_name):
    """Returns an attr name by header name."""
    if header_name in self._header_attr_mapping:
      return self._header_attr_mapping[header_name]
    return inflection.underscore(header_name)

  def matches_conditions(self, row_obj, **expected_dict):
    """Returns whether tree item matches conditions.
    Conditions are evaluated similarly to how `obj_dict` is built.
    """
    for attr_name, expected_value in expected_dict.iteritems():
      if hasattr(row_obj, attr_name):
        actual_value = getattr(row_obj, attr_name)()
      else:
        actual_value = self.text_for_header(
            self._header_name_for_attr_name(attr_name))
      if actual_value != expected_value:
        return False
    return True

  def _header_name_for_attr_name(self, attr_name):
    """Returns a header name by attr name."""
    if attr_name in self._attr_header_mapping:
      return self._attr_header_mapping[attr_name]
    return inflection.camelize(attr_name)

  def text_for_header(self, header_name):
    """Returns value of cell with header `header_name`."""
    idx = self._headers.index(header_name)
    return self._cached_text_in_cells()[idx]

  def cell_for_header(self, header_name):
    """Returns cell for header `header_name`."""
    idx = self._headers.index(header_name)
    return self.cells()[idx]

  @decorator.memoize
  def _cached_text_in_cells(self):
    """Returns the cached contents."""
    return [el.text for el in self.cells()]

  def cells(self):
    """Returns the list with contents of all attr cells."""
    return self.root.elements(**self._cell_locator)
