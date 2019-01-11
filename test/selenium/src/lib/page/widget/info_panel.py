# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Contains Info Widget functionality specific to info panels
(split done as `info_widget` module is too large.
"""
from lib.page.modal import update_object
from lib.constants import locator


class InfoPanel(object):
  """Contains functionality specific to info panel."""
  # pylint: disable=too-few-public-methods

  def __init__(self, root):
    self._root = root
    self._locators = locator.WidgetInfoPanel

  @property
  def title(self):
    """Return panel title"""
    return self._root.element(class_name='pane-header__title-details').\
        h3().text

  @property
  def is_minimized(self):
    return self._root.parent(class_name='pin-content--minimized').exists

  @property
  def is_maximized(self):
    return self._root.parent(class_name='pin-content--maximized').exists

  @property
  def button_minimize(self):
    """Return minimize button"""
    return self._root.element(class_name='fa-compress')

  @property
  def button_maximize(self):
    """Return maximize button"""
    return self._root.element(class_name='fa-expand')

  @property
  def button_close(self):
    """Return close button"""
    return self._root.element(class_name='close-pane')


class SnapshotInfoPanel(InfoPanel):
  """Contains functionality specific to snapshot info panel."""

  @property
  def snapshot_version_el(self):
    """Returns snapshot version element."""
    return self._root.element(class_name="state-value snapshot")

  @property
  def _link_to_get_latest_version(self):
    """Returns `Get the latest version` link."""
    return self._root.link(text="Get the latest version")

  def open_link_to_get_latest_version(self):
    """Click on link get latest version under Info panel."""
    # `js_click` is used because Selenium wrongly considers link
    #    to be invisible.
    self._link_to_get_latest_version.js_click()
    return update_object.CompareUpdateObjectModal()

  def has_link_to_get_latest_version(self):
    """Returns whether the page contains link to get latest version."""
    return self._link_to_get_latest_version.exists

  def get_latest_version(self):
    """Get latest version."""
    self.open_link_to_get_latest_version().confirm_update()
