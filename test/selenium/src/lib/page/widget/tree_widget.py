# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Tree view."""

from lib import base
from lib.page.widget import table_with_headers
from lib.utils import test_utils


class TreeWidget(base.WithBrowser):
  """Tree widget."""

  def __init__(self, table_row_cls=None):
    super(TreeWidget, self).__init__()
    self._root = self._browser
    if table_row_cls:
      self._table_row_cls = table_row_cls
    else:
      self._table_row_cls = TreeItem
    self._table = table_with_headers.TableWithHeaders(
        self._root,
        header_locator={"class_name": "tree-header-titles__text"},
        table_rows=self.tree_items
    )

  def get_tree_item_by(self, **conditions):
    """Returns a table row that matches conditions."""
    return self._table.get_table_row_by(**conditions)

  def tree_items(self):
    """Returns tree items."""
    self._wait_loading()
    return [self._table_row_cls(row, self._table.table_header_names())
            for row in self._tree_item_rows()]

  def _tree_item_rows(self):
    """Returns tree item elements."""
    return self._root.elements(tag_name="tree-item")

  def _wait_loading(self):
    """Wait for elements to load."""
    def results_present():
      """Return if results are present."""
      if self._browser.element(class_name="tree-no-results-message").present:
        return True
      if list(self._tree_item_rows()):
        return True
      return False
    test_utils.wait_for(results_present)


class TreeItem(object):
  """Tree item."""

  def __init__(self, row_el, table_header_names, header_attr_mapping=None):
    self._table_row = table_with_headers.TableRow(
        container=row_el,
        table_header_names=table_header_names,
        cell_locator={"class_name": "attr-content"},
        header_attr_mapping=header_attr_mapping
    )
    self.text_for_header = self._table_row.text_for_header

  def matches_conditions(self, **conditions):
    """Returns whether a row matches conditions."""
    return self._table_row.matches_conditions(self, **conditions)

  def obj_dict(self):
    """Returns an obj dict."""
    return self._table_row.obj_dict(self)

  def select(self):
    """Clicks tree item to open info panel."""
    self._table_row.root.element(class_name="selectable-attrs").click()
