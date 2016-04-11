# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Base classes for widget models"""
# pylint: disable=not-callable
# pylint: disable=not-an-iterable

from lib import base
from lib import decorator
from lib import environment
from lib.utils import selenium_utils
from lib.constants import locator
from lib.constants import url


class _Modal(base.Modal):
  """Base model for the edit modal"""

  _locator = locator.ModalCustomAttribute

  def __init__(self, driver):
    super(_Modal, self).__init__(driver)

    self.ui_attribute_title = base.TextInputField(
        self._driver, self._locator.UI_ATTRIBUTE_TITLE)
    self.button_submit = base.Button(
        self._driver, self._locator.BUTTON_SAVE_AND_CLOSE)

  def enter_title(self, title):
    self.ui_attribute_title.enter_text(title)

  @decorator.handle_alert
  def save_and_close(self):
    """
    Returns:
        WidgetAdminCustomAttributes
    """
    self.button_submit.click()


class CreateNewCustomAttributeModal(base.Modal):
  _locator = locator.ModalCustomAttribute

  def __init__(self, driver):
    super(CreateNewCustomAttributeModal, self).__init__(driver)

    self.button_add_more = base.Button(
        self._driver, self._locator.BUTTON_ADD_ANOTHER)

  def save_and_add_another(self):
    """
    Returns:
        ModalCustomAttributes
    """
    self.button_add_more.click_when_visible()
    return self.__class__(self._driver)


class Dropdown(base.Component):
  """A generic model for a dropdown in custom attributes"""

  _locator_button_add = None
  _locator_label_attribute_name = None
  _locator_label_attribute_type = None
  _locator_label_mandatory = None
  _locator_label_edit = None
  _locator_listed_members = None
  _locator_buttons_edit = None
  _cls_new_attrb_modal = None

  def __init__(self, driver):
    super(Dropdown, self).__init__(driver)

    self.button_add = base.Button(driver, self._locator_button_add)
    self.attribute_name = base.Label(
        driver, self._locator_label_attribute_name)
    self.attribute_type = base.Label(
        driver, self._locator_label_attribute_type)
    self.mandatory = base.Label(driver, self._locator_label_mandatory)
    self.edit = base.Label(driver, self._locator_label_edit)

  def add_new_custom_attribute(self):
    """
    Returns:
        new_custom_attribute.ModalCustomAttributes
    """
    selenium_utils.wait_until_stops_moving(self.button_add.element)
    selenium_utils.scroll_into_view(self._driver, self.button_add.element)
    self.button_add.click()
    return self._cls_new_attrb_modal(self._driver)

  def edit_nth_member(self, member):
    """Selects nth member from listed members in the dropdown. Since we're
    selecting from a list, the first member has the index 0.

    Args:
        member (int)
    """
    # check that the buttons are loaded
    selenium_utils.get_when_clickable(
        self._driver, self._locator_buttons_edit)

    elements = self._driver.find_elements(*self._locator_buttons_edit)
    selenium_utils.scroll_into_view(self._driver, elements[member]).click()
    return CustomAttributeModal(self._driver)


class CustomAttributeModal(_Modal):
  """Model for the custom attribute modal"""

  def __init__(self, driver):
    super(CustomAttributeModal, self).__init__(driver)
    self.attribute_title = base.Label(
        self._driver, self._locator.ATTRIBUTE_TITLE)
    self.inline_help = base.Label(self._driver, self._locator.INLINE_HELP)
    self.attribute_type = base.Label(
        self._driver, self._locator.ATTRIBUTE_TYPE)
    self.placeholder = base.Label(self._driver, self._locator.PLACEHOLDER)
    self.mandatory = base.Label(self._driver, self._locator.MANDATORY)
    self.ui_inline_help = base.TextInputField(
        self._driver, self._locator.UI_INLINE_HELP)
    self.ui_placeholder = base.TextInputField(
        self._driver, self._locator.UI_PLACEHOLDER)
    self.checkbox_mandatory = base.Checkbox(
        self._driver, self._locator.CHECKBOX_MANDATORY)

  def enter_inline_help(self, inline_help):
    self.ui_inline_help.enter_text(inline_help)

  def enter_placeholder(self, placeholder):
    self.ui_placeholder.enter_text(placeholder)

  def check_is_mandatory(self):
    self.checkbox_mandatory.click()


class DynamicTreeToggle(base.Toggle):
  """Class representing the tree item in admin custom attribute widget"""

  def __init__(self, driver, el_locator):
    self.element = driver.find_element(*el_locator)
    self.is_activated = selenium_utils.is_value_in_attr(self.element)


class WidgetAdminCustomAttributes(base.Widget):
  """Base model for custom attributes on the admin dashboard page"""
  _locator = locator.AdminCustomAttributes
  URL = environment.APP_URL \
      + url.ADMIN_DASHBOARD \
      + url.Widget.CUSTOM_ATTRIBUTES

  def __init__(self, driver):
    super(WidgetAdminCustomAttributes, self).__init__(driver)
    self.filter = base.Filter(
        self._driver,
        self._locator.FILTER_INPUT_FIELD,
        self._locator.FILTER_BUTTON_SUBMIT,
        self._locator.FILTER_BUTTON_RESET)

    self.button_workflows = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_WORKFLOWS)
    self.button_risk_assessments = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_RISK_ASSESSMENTS)
    self.button_threats = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_THREATS)
    self.button_risks = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_RISKS)
    self.button_programs = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_PROGRAMS)
    self.button_audits = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_AUDITS)
    self.button_objectives = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_OBJECTIVES)
    self.button_sections = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_SECTIONS)
    self.button_controls = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_CONTROLS)
    self.button_issues = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_ISSUES)
    self.button_assessments = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_ASSESSMENTS)
    self.button_standards = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_STANDARDS)
    self.button_regulations = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_REGULATIONS)
    self.button_policies = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_POLICIES)
    self.button_contracts = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_CONTRACTS)
    self.button_clauses = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_CLAUSES)
    self.button_requests = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_REQUESTS)
    self.button_vendors = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_VENDORS)
    self.button_people = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_PEOPLE)
    self.button_objectives = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_OBJECTIVES)
    self.button_access_groups = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_ACCESS_GROUPS)
    self.button_org_groups = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_ORG_GROUPS)
    self.button_products = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_PRODUCTS)
    self.button_markets = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_MARKETS)
    self.button_processes = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_PROCESSES)
    self.button_facilities = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_FACILITIES)
    self.button_projects = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_PROJECTS)
    self.button_contracts = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_CONTRACTS)
    self.button_data_assets = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_DATA_ASSETS)
    self.button_systems = DynamicTreeToggle(
        self._driver, self._locator.TOGGLE_SYSTEMS)
