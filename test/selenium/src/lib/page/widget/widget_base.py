# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Base classes for widget models"""
# pylint: disable=not-callable
# pylint: disable=not-an-iterable
# pylint: disable=too-few-public-methods

from lib import base
from lib import decorator
from lib import environment
from lib.constants import locator
from lib.constants import url
from lib.entities.entity import CustomAttribute
from lib.utils import selenium_utils
from lib.utils.string_utils import get_bool_from_string


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


class CustomAttributesItemContent(base.Component):
  """A generic model for a 2-tier of custom attributes tree-view item."""
  _locator = locator.CustomAttributesItemContent

  def __init__(self, driver, item_text):
    super(CustomAttributesItemContent, self).__init__(driver)
    self.button_add = base.Button(driver, self._locator.ADD_BTN)
    self.custom_attributes_list = []
    self._item_name = item_text

  def add_new_custom_attribute(self, ca_object):
    """Create Custom Attribute entry based on given CustomAttribute object."""
    ca_modal = self.open_add_new_ca_modal()
    ca_modal.select_type(ca_object.ca_type)
    ca_modal.enter_title(ca_object.title)

    if ca_object.is_mandatory:
      ca_modal.set_mandatory()

    if ca_object.placeholder is not None:
      ca_modal.enter_placeholder(ca_object.placeholder)

    ca_modal.enter_inline_help(ca_object.helptext)

    if ca_object.multi_choice_options is not None:
      ca_modal.enter_possible_values(ca_object.multi_choice_options)

    ca_modal.save_and_close()

  def _set_custom_attributes_list(self):
    """
    Set custom attributes list with CustomAttribute objects from the
    current opened content item.
    """
    for elem in selenium_utils.get_when_all_visible(self._driver,
                                                    self._locator.ROW):
      attr = [i.text for i in elem.find_elements(*self._locator.CELL_IN_ROW)]
      self.custom_attributes_list.append(
          CustomAttribute(
              title=attr[0],
              ca_type=attr[1],
              is_mandatory=get_bool_from_string(attr[2]),
              definition_type=self._item_name))

  def get_custom_attributes_list_from_group(self):
    """Returns list of CustomAttribute objects."""
    self._set_custom_attributes_list()
    return self.custom_attributes_list

  def open_add_new_ca_modal(self):
    """Open Add Attribute modal and return CustomAttributeModal PageObject."""
    selenium_utils.wait_until_stops_moving(self.button_add.element)
    selenium_utils.scroll_into_view(self._driver, self.button_add.element)
    selenium_utils.get_when_clickable(self._driver, self._locator.ADD_BTN)
    selenium_utils.get_when_invisible(self._driver, self._locator.TREE_SPINNER)
    self.button_add.click()
    return CustomAttributeModal(self._driver)

  def edit_nth_member(self, member):
    """Selects nth member from listed members in the dropdown. Since we're
    selecting from a list, the first member has the index 0.

    Args:
        member (int)
    """
    # check that the buttons are loaded
    selenium_utils.get_when_clickable(
        self._driver, self._locator.EDIT_BTN)

    elements = self._driver.find_elements(self._locator.EDIT_BTN)
    selenium_utils.scroll_into_view(self._driver, elements[member]).click()
    return CustomAttributeModal(self._driver)


class CustomAttributeModal(_Modal):
  """Model for the custom attribute modal."""

  def __init__(self, driver):
    super(CustomAttributeModal, self).__init__(driver)
    self.attribute_title = base.Label(
        self._driver, self._locator.ATTRIBUTE_TITLE)
    self.inline_help = base.Label(self._driver, self._locator.INLINE_HELP)
    self.attribute_type = base.Label(
        self._driver, self._locator.ATTRIBUTE_TYPE)
    self.placeholder = base.Label(self._driver, self._locator.PLACEHOLDER)
    self.mandatory = base.Label(self._driver, self._locator.MANDATORY)
    self.ui_inline_help = None
    self.ui_placeholder = None
    self.checkbox_mandatory = base.Checkbox(
        self._driver, self._locator.CHECKBOX_MANDATORY)
    self.attribute_type_selector = base.DropdownStatic(
        self._driver,
        self._locator.ATTRIBUTE_TYPE_SELECTOR,
        self._locator.ATTRIBUTE_TYPE_OPTIONS)
    self.ui_possible_values = None

  def enter_inline_help(self, inline_help):
    """Fill the 'Inline help' field."""
    self.ui_inline_help = base.TextInputField(
        self._driver, self._locator.UI_INLINE_HELP)
    self.ui_inline_help.enter_text(inline_help)

  def enter_placeholder(self, placeholder):
    """Fill the 'Placeholder' field."""
    self.ui_placeholder = base.TextInputField(
        self._driver, self._locator.UI_PLACEHOLDER)
    self.ui_placeholder.enter_text(placeholder)

  def set_mandatory(self):
    """Check 'Mandatory' checkbox."""
    self.checkbox_mandatory.click()

  def select_type(self, ca_type):
    """Select CustomAttribute type from 'Attribute type' dropdown."""
    self.attribute_type_selector.select(ca_type)

  def enter_possible_values(self, values_string):
    """Fill 'Possible values' field for 'Dropdown' type of CustomAttribute."""
    self.ui_possible_values = base.TextInputField(
        self._driver,
        self._locator.UI_POSSIBLE_VALUES)
    self.ui_possible_values.enter_text(values_string)


class DynamicTreeToggle(base.Toggle):
  """Class representing the tree item in admin custom attribute widget"""

  def __init__(self, driver, el_locator):
    self.element = driver.find_element(*el_locator)
    self.is_activated = selenium_utils.is_value_in_attr(self.element)


class WidgetAdminCustomAttributes(base.Widget):
  """Base model for custom attributes on the admin dashboard page."""
  _locator = locator.AdminCustomAttributes
  URL = environment.APP_URL \
      + url.ADMIN_DASHBOARD \
      + url.Widget.CUSTOM_ATTRIBUTES
