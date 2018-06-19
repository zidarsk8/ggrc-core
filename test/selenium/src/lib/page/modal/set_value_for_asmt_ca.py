# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Modals for create objects."""

from lib import base
from lib.constants import locator
from lib.utils import selenium_utils


class SetValueForAsmtDropdown(base.Modal):
  """Modal for set value for assessment custom attribute."""

  def __init__(self, driver):
    super(SetValueForAsmtDropdown, self).__init__(driver)
    self.modal_elem = selenium_utils.get_when_visible(
        self._driver, locator.ModalSetValueForAsmtCA.MODAL_LOCATOR)
    self.modal_header_lbl = base.Label(
        self._driver, locator.ModalSetValueForAsmtCA.MODAL_HEADER)

  def click_close_button(self):
    """Click close button."""
    base.Button(
        self._driver, locator.ModalSetValueForAsmtCA.BUTTON_CLOSE).click()

  def click_save_button(self):
    """Click save button."""
    base.Button(
        self._driver,
        locator.ModalSetValueForAsmtCA.BUTTON_SAVE).click()

  def set_dropdown_comment(self, comment):
    """Set comment via dropdown."""
    input_field = base.TextInputField(
        self._driver,
        locator.ModalSetValueForAsmtCA.INPUT_COMMENT)
    input_field.click()
    input_field.element.send_keys(comment)

  def set_dropdown_url(self, url):
    """Set evidence url via dropdown."""
    base.Button(
        self._driver,
        locator.ModalSetValueForAsmtCA.BUTTON_ADD_URL).click()
    base.TextInputField(
        self._driver,
        locator.ModalSetValueForAsmtCA.INPUT_EVIDENCE_URL).enter_text(
        url)
    base.Button(
        self._driver,
        locator.ModalSetValueForAsmtCA.BUTTON_CONFIRM_URL).click()

  def fill_dropdown_lca(self, **kwargs):
    """Fill comment or url for Assessment dropdown."""
    if "url" in kwargs:
      self.set_dropdown_url(kwargs["url"])
    if "comment" in kwargs:
      self.set_dropdown_comment(kwargs["comment"])
      self.click_save_button()
    else:
      self.click_close_button()
