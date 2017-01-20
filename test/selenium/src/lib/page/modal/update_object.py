# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Modals for updating objects to actual version."""

from lib import base
from lib.constants import locator
from lib.utils import selenium_utils


class UpdateObjectModal(base.Modal):
  """A generic modal for updating an object."""
  # pylint: disable=too-few-public-methods

  _page_model_cls_after_redirect = None
  _locator = locator.ModalUpdateObject

  def __init__(self, driver):
    super(UpdateObjectModal, self).__init__(driver)
    self.title_modal = base.Label(driver, self._locator.MODAL_TITLE)
    self.confirmation_text = base.Label(driver,
                                        self._locator.CONFIRMATION_TEXT)
    self.button_update = base.Button(driver, self._locator.BUTTON_UPDATE)

  def confirm_update(self):
    """Confirm updating an object."""
    self.button_update.click()
    selenium_utils.wait_until_not_present(self._driver,
                                          locator.TreeView.ITEM_LOADING)
    selenium_utils.get_when_invisible(self._driver, locator.TreeView.SPINNER)
