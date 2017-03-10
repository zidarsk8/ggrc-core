# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Modals for compare and update objects."""

from lib import base
from lib.constants import locator


class CompareUpdateObjectModal(base.Modal):
  """Modal for compare version of objects and update them to latest version."""
  # pylint: disable=too-few-public-methods
  _locator = locator.ModalUpdateObject

  def __init__(self, driver):
    super(CompareUpdateObjectModal, self).__init__(driver)
    self.title_modal = base.Label(driver, self._locator.MODAL_TITLE)
    self.confirmation_text = base.Label(
        driver, self._locator.CONFIRMATION_TEXT)
    self.button_update = base.Button(driver, self._locator.BUTTON_CONFIRM)

  def confirm_update(self):
    """Confirm update object."""
    self.button_update.click()
