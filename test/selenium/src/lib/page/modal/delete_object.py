# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Modals for delete objects."""

from lib import base
from lib.constants import locator


class DeleteObjectModal(base.Modal):
  """Modal for delete objects."""
  _locator = locator.ModalDeleteObject

  def __init__(self, driver):
    super(DeleteObjectModal, self).__init__(driver)
    self.title_modal = base.Label(driver, self._locator.MODAL_TITLE)
    self.confirmation_text = base.Label(
        driver, self._locator.CONFIRMATION_TEXT)
    self.title_object = base.Label(driver, self._locator.OBJECT_TITLE)
    self.button_delete = base.Button(driver, self._locator.BUTTON_DELETE)

  def confirm_delete(self):
    """Confirm delete object."""
    self.button_delete.click()
