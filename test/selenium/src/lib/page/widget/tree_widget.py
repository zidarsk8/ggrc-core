# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Tree view."""

from lib import base, decorator
from lib.utils import test_utils


class TreeWidget(base.WithBrowser):
  """Tree widget."""

  def tree_header_titles(self):
    """Returns tree header titles."""
    return [el.text_content for el in self._browser.elements(
        class_name="tree-header-titles__text")]

  def _tree_item_els(self):
    """Returns Tree Item elements. Tree Item element knows only about cell
    contents. It doesn't know about names of cells. So an object can't
    be built using it.
    """
    return [TreeItemEl(el) for el in self._browser.elements(
        tag_name="tree-item")]

  def tree_items(self):
    """Returns wrappers for tree item that knows about headers and cells."""
    self._wait_loading()
    headers = self.tree_header_titles()
    return [TreeItem(headers, tree_item_el)
            for tree_item_el in self._tree_item_els()]

  def _wait_loading(self):
    """Wait for elements to load."""
    def results_present():
      """Return if results are present."""
      if self._browser.element(class_name="tree-no-results-message").present:
        return True
      if len(self._tree_item_els()) > 0:
        return True
      return False
    test_utils.wait_for(results_present)


class TreeItemEl(object):
  """Represents tree item element."""
  # pylint: disable=too-few-public-methods

  def __init__(self, item_row):
    self._root = item_row

  def contents(self):
    """Returns the list with contents of all attr cells."""
    return [el.text for el in self._root.elements(
        class_name="attr-content")]


class TreeItem(object):
  """A wrapper for tree item that knows also about headers.
  That allows to build object from it.
  """

  def __init__(self, headers, tree_item_el):
    self._headers = headers
    self._tree_item_el = tree_item_el

  def title(self):
    """Returns title."""
    try:
      return self._cell_value("Title")
    except ValueError:
      # Title is named Summary on Workflow task group page (GGRC-6042)
      return self._cell_value("Summary")

  def _cell_value(self, header_name):
    """Returns value of cell with header `header_name`."""
    idx = self._headers.index(header_name)
    return self.contents()[idx]

  @decorator.memoize
  def contents(self):
    """Returns the list with contents of all attr cells."""
    return self._tree_item_el.contents()
