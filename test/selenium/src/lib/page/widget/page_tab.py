# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Operations with page tabs"""


class Tabs(object):
  """Represents tab page element on web pages."""

  TOP = "top"
  INTERNAL = "internal"

  def __init__(self, container, level):
    if level == self.TOP:
      self._root = container.ul(class_name="internav")
    elif level == self.INTERNAL:
      self._root = container.element(class_name="nav-tabs")
    else:
      raise NotImplementedError

  def active_tab_name(self):
    """Returns name of the active tab."""
    return self._root.li(class_name="active").text

  def ensure_tab(self, tab_name):
    """Ensure that page tab `tab_name` is opened"""
    if self.active_tab_name() != tab_name:
      self.select_tab(tab_name)

  def select_tab(self, tab_name):
    """Selects tab with name `tab_name`."""
    self._root.li(text=tab_name).click()
