# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Modals to set visible fields for objects."""

from selenium.webdriver.common.by import By

from lib import base
from lib.constants import locator
from lib.utils import selenium_utils


class SetVisibleFieldsModal(base.Modal):
  """Modal to select and set visible fields for objects to represent them on
  Tree View."""
  _locators = locator.ModalSetVisibleFields

  def __init__(self, driver, widget_name, fields_to_set):
    super(SetVisibleFieldsModal, self).__init__(driver)
    self.widget_name = widget_name
    self.fields_to_set = fields_to_set

  def select_visible_fields(self):
    """Select visible fields checkboxes on Select Visible Fields modal
    according to titles of fields to set."""
    # pylint: disable=attribute-defined-outside-init
    _locator_modal_fields = (By.CSS_SELECTOR,
                             self._locators.MODAL.format(self.widget_name))
    _locator_fields_titles = (
        By.CSS_SELECTOR,
        locator.ModalSetVisibleFields.FIELDS_TITLES.format(self.widget_name))
    _locator_fields_checkboxes = (
        By.CSS_SELECTOR,
        locator.ModalSetVisibleFields.FIELDS_CHECKBOXES.format(
            self.widget_name))
    selenium_utils.get_when_visible(self._driver, _locator_modal_fields)
    self.visible_fields_elements = base.ListCheckboxes(
        self._driver, titles_locator=_locator_fields_titles,
        checkboxes_locator=_locator_fields_checkboxes)
    self.visible_fields_elements.select_by_titles(self.fields_to_set)

  def confirm_set_visible_fields(self):
    """Confirm set visible fields."""
    _locator_set_fields = (
        By.CSS_SELECTOR,
        self._locators.BUTTON_SET_FIELDS.format(self.widget_name))
    base.Button(self._driver, _locator_set_fields).click()
    selenium_utils.get_when_invisible(self._driver, _locator_set_fields)

  def select_and_set_visible_fields(self):
    """Select checkboxes to set objects visible fields and confirm set."""
    self.select_visible_fields()
    self.confirm_set_visible_fields()
