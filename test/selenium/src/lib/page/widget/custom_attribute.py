# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib import environment
from lib.constants import url
from lib.constants import locator


class _Dropdown(base.Component):
  def __init__(self, driver, locator_button_add):
    super(_Dropdown, self).__init__(driver)
    self.button_add = base.Button(driver, locator_button_add)

  def add_new_custom_attribute(self):
    """
    Returns:
        new_custom_attribute.NewCustomAttributeModal
    """
    self.button_add.click_when_moving_over()
    return NewCustomAttributeModal(self._driver)


class NewCustomAttributeModal(base.Modal):
  _locator = locator.ModalCustomAttribute

  def __init__(self, driver):
    super(NewCustomAttributeModal, self).__init__(driver)
    self.attribute_title = base.Label(
        self._driver, self._locator.ATTRIBUTE_TITLE)
    self.inline_help = base.Label(self._driver, self._locator.INLINE_HELP)
    self.attribute_type = base.Label(
        self._driver, self._locator.ATTRIBUTE_TYPE)
    self.placeholder = base.Label(self._driver, self._locator.PLACEHOLDER)
    self.mandatory = base.Label(self._driver, self._locator.MANDATORY)
    self.ui_attribute_title = base.TextInputField(
        self._driver, self._locator.UI_ATTRIBUTE_TITLE)
    self.ui_inline_help = base.TextInputField(
        self._driver, self._locator.UI_INLINE_HELP)
    self.ui_placeholder = base.TextInputField(
        self._driver, self._locator.UI_PLACEHOLDER)
    self.checkbox_mandatory = base.Checkbox(
        self._driver, self._locator.CHECKBOX_MANDATORY)
    self.button_submit = base.Button(
        self._driver, self._locator.BUTTON_SAVE)
    self.button_add_more = base.Button(
        self._driver, self._locator.BUTTON_ADD_ANOTHER)

  def enter_title(self, title):
    self.ui_attribute_title.enter_text(title)

  def enter_inline_help(self, inline_help):
    self.ui_inline_help.enter_text(inline_help)

  def enter_placeholder(self, placeholder):
    self.ui_placeholder.enter_text(placeholder)

  def check_is_mandatory(self):
    self.checkbox_mandatory.click()

  def save_and_close(self):
    """
    Returns:
        custom_attribute.AdminCustomAttributes
    """
    self.button_submit.click()
    return AdminCustomAttributes(self._driver)

  def save_and_add_another(self):
    """
    Returns:
        NewCustomAttributeModal
    """
    self.button_add_more.click_when_visible()
    return NewCustomAttributeModal(self._driver)


class AdminCustomAttributes(base.Widget):
  _locator = locator.AdminCustomAttributes
  URL = environment.APP_URL \
      + url.ADMIN_DASHBOARD \
      + url.Widget.CUSTOM_ATTRIBUTES

  def __init__(self, driver):
    super(AdminCustomAttributes, self).__init__(driver)
    self.filter = base.Filter(
        self._driver,
        self._locator.FILTER_INPUT_FIELD,
        self._locator.FILTER_BUTTON_SUBMIT,
        self._locator.FILTER_BUTTON_RESET
    )
    self.button_workflows = base.Button(
        self._driver, self._locator.BUTTON_WORKFLOWS)
    self.button_risk_assessments = base.Button(
        self._driver, self._locator.BUTTON_RISK_ASSESSMENTS)
    self.button_threats = base.Button(
        self._driver, self._locator.BUTTON_THREATS)
    self.button_risks = base.Button(
        self._driver, self._locator.BUTTON_RISKS)
    self.button_programs = base.Button(
        self._driver, self._locator.BUTTON_PROGRAMS)

  def select_programs(self):
    """
    Returns:
        _Dropdown
    """
    self.button_programs.click()
    return _Dropdown(self._driver,
                     self._locator.BUTTON_ADD_CUSTOM_PROGRAM_ATTR)
