# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Info Page and Info Panel dropdown elements."""

from lib import base
from lib.constants import locator
from lib.page.modal import (delete_object, edit_object, update_object,
                            clone_object)
from lib.utils import selenium_utils


class CommonDropdownSettings(base.Component):
  """Common for 3BBS button/dropdown settings on Info pages and Info panels.
  """
  _locators = locator.CommonDropdown3bbsInfoWidget

  def __init__(self, driver, is_under_audit):
    super(CommonDropdownSettings, self).__init__(driver)
    self.edit_locator = (
        self._locators.BUTTON_3BBS_EDIT_UNDER_AUDIT if is_under_audit
        else self._locators.BUTTON_3BBS_EDIT)
    self.open_locator = (
        self._locators.BUTTON_3BBS_OPEN_UNDER_AUDIT if is_under_audit
        else self._locators.BUTTON_3BBS_OPEN)
    self.get_permalink_locator = (
        self._locators.BUTTON_3BBS_GET_PERMALINK_UNDER_AUDIT if is_under_audit
        else self._locators.BUTTON_3BBS_GET_PERMALINK)
    self.delete_locator = (
        self._locators.BUTTON_3BBS_DELETE_UNDER_AUDIT if is_under_audit
        else self._locators.BUTTON_3BBS_DELETE)

  def select_open(self):
    """Select open button in 3BBS dropdown modal."""
    base.Button(self._driver, self.open_locator).click()

  def is_open_enabled(self):
    """Find open button in 3BBS dropdown modal and check if it enabled.
    Return:
    True if disabled attribute value does not exist for parent element of open,
    False if disabled attribute value exist for parent element of open.
    """
    parent_element_of_open = selenium_utils.get_parent_element(
        self._driver, self._driver.find_element(*self.open_locator))
    return selenium_utils.is_value_in_attr(
        parent_element_of_open, value=locator.Common.DISABLED_VALUE)

  def select_edit(self):
    """Select edit button in 3BBS dropdown modal.
    Return: lib.page.modal.edit_object.EditModal
    """
    base.Button(self._driver, self.edit_locator).click()
    return getattr(edit_object, self.__class__.__name__)(self._driver)

  def is_edit_exist(self):
    """Find edit button in 3BBS dropdown modal.
    Return: True if edit button is exist,
            False if edit button is not exist.
    """
    return selenium_utils.is_element_exist(self._driver, self.edit_locator)

  def select_get_permalink(self):
    """Select get permalink in 3BBS dropdown modal."""
    base.Button(self._driver, self.get_permalink_locator).click()

  def select_delete(self):
    """Select delete in 3BBS dropdown modal.
    Return: modal.delete_object.DeleteObjectModal
    """
    base.Button(self._driver, self.delete_locator).click()
    return delete_object.DeleteObjectModal(self._driver)


class Audits(CommonDropdownSettings):
  """Audits 3BBS button/dropdown settings on Info pages and Info panels."""
  _locators = locator.AuditsDropdown3bbsInfoWidget

  def select_update_objs(self):
    """Select update objects to latest version in 3BBS dropdown modal.
    Return: modal.update_object.CompareUpdateObjectModal
    """
    base.Button(self._driver, self._locators.BUTTON_3BBS_UPDATE).click()
    return update_object.CompareUpdateObjectModal(self._driver)

  def select_clone(self):
    """Select clone Audit in 3BBS dropdown modal.
    Return: modal.clone_object.CloneAuditModal
    """
    base.Button(self._driver, self._locators.BUTTON_3BBS_CLONE).click()
    return clone_object.CloneAuditModal(self._driver)


class Programs(CommonDropdownSettings):
  """Programs 3BBS button/dropdown settings on Info pages and Info panels."""


class Controls(CommonDropdownSettings):
  """Controls 3BBS button/dropdown settings on Info pages and Info panels."""


class Processes(CommonDropdownSettings):
  """Processes 3BBS button/dropdown settings on Info pages and Info panels."""


class DataAssets(CommonDropdownSettings):
  """DataAssets 3BBS button/dropdown settings on Info pages and Info panels."""


class Systems(CommonDropdownSettings):
  """Systems 3BBS button/dropdown settings on Info pages and Info panels."""


class Products(CommonDropdownSettings):
  """Products 3BBS button/dropdown settings on Info pages and Info panels."""


class Projects(CommonDropdownSettings):
  """Projects 3BBS button/dropdown settings on Info pages and Info panels."""


class OrgGroups(CommonDropdownSettings):
  """OrgGroups 3BBS button/dropdown settings on Info pages and Info panels."""
