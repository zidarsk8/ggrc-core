# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from lib import base
from lib import environment
from lib.constants import locator
from lib.constants import url
from lib.page.widget import widget_base
from lib.utils import selenium_utils


class Widget(base.Widget):
  """Base class for admin widgets"""


class Events(Widget):
  """Model for event widget on admin dashboard"""
  _locator = locator.WidgetAdminEvents

  URL = environment.APP_URL \
      + url.ADMIN_DASHBOARD \
      + url.Widget.EVENTS

  def __init__(self, driver):
    super(Events, self).__init__(driver)
    self.widget_header = base.Label(driver, self._locator.TREE_VIEW_HEADER)

  def get_events(self):
    """Get list of WebElements that displayed in tree view at Event widget"""
    selenium_utils.get_when_clickable(
        self._driver,
        self._locator.FIRST_TREE_VIEW_ITEM)
    return self._driver.find_elements(*self._locator.TREE_VIEW_ITEMS)


class People(Widget):
  """Model for people widget on admin dashboard"""
  URL = environment.APP_URL \
      + url.ADMIN_DASHBOARD \
      + url.Widget.PEOPLE


class Roles(Widget):
  """Model for the widget admin roles on admin dashboard"""
  _locator = locator.WidgetAdminRoles

  URL = environment.APP_URL \
      + url.ADMIN_DASHBOARD \
      + url.Widget.ROLES

  def __init__(self, driver):
    super(Roles, self).__init__(driver)
    self.tree_view_items = base.selenium_utils.get_when_all_visible(
        driver, self._locator.ROLES_TREE_VIEW_ITEMS)

  def get_role_scopes_text_as_dict(self):
    """Get dictionary of labels that displayed in tree view at Event widget"""
    return dict([item.text.splitlines() for item in self.tree_view_items])


class CustomAttributes(widget_base.WidgetAdminCustomAttributes):
  """Model for custom attributes widget on the admin dashboard page"""
  def select_programs(self):
    """
    Returns:
        DropdownPrograms
    """
    self.button_programs.click()
    return DropdownPrograms(self._driver)


class ModalCustomAttributes(widget_base.CustomAttributeModal,
                            widget_base.CreateNewCustomAttributeModal):
  """Model for the custom attribute modal"""


class DropdownPrograms(widget_base.Dropdown):
  """Model for programs dropdown"""
  _locator_button_add = locator.AdminCustomAttributes \
      .BUTTON_ADD_CUSTOM_PROGRAM_ATTR
  _locator_label_attribute_name = locator.AdminCustomAttributes \
      .PROGRAMS_LABEL_ATTRIBUTE_NAME
  _locator_label_attribute_type = locator.AdminCustomAttributes \
      .PROGRAMS_LABEL_ATTRIBUTE_TYPE
  _locator_label_mandatory = locator.AdminCustomAttributes \
      .PROGRAMS_LABEL_MANDATORY
  _locator_label_edit = locator.AdminCustomAttributes.PROGRAMS_LABEL_EDIT
  _locator_listed_members = locator.AdminCustomAttributes.LISTED_MEMBERS
  _locator_buttons_edit = locator.AdminCustomAttributes \
      .BUTTON_LISTED_MEMBERS_EDIT
  _cls_new_attrb_modal = ModalCustomAttributes
