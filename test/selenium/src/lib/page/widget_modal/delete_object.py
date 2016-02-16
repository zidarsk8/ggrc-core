# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com
"""Modals for deleting objects"""

from lib import base
from lib.constants import locator
import lib.page.dashboard


class DeleteObjectModal(base.Modal):
  """A generic modal for deleting an object"""

  _locator = locator.Widget

  def __init__(self, driver):
    super(DeleteObjectModal, self).__init__(driver)
    self.title_modal = base.Label(
        driver, self._locator.MODAL_OBJECT_DELETE_TITLE)
    self.confirmation_text = base.Label(
        driver, self._locator.MODAL_OBJECT_DELETE_CONFIRMATION_TEXT)
    self.title_object = base.Label(
        driver, self._locator.MODAL_OBJECT_DELETE_OBJECT_TITLE)
    self.button_delete = base.Button(
        driver, self._locator.MODAL_OBJECT_DELETE_BUTTON_DELETE)

  def confirm_delete(self):
    """
    Returns:
        lib.page.dashboard.DashboardPage
    """
    self.button_delete.click()
    self.wait_for_redirect()
    return lib.page.dashboard.DashboardPage(self._driver)
