# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Elements in the object's info widget"""

from lib import base
from lib.page import modal
from lib.constants import locator


class DropdownSettings(base.Component):
  """A class for the button/dropdown settings in the info widget"""

  _locator = locator.WidgetInfoSettingsButton

  def __init__(self, driver):
    super(DropdownSettings, self).__init__(driver)
    self.edit = base.Button(driver, self._locator.DROPDOWN_SETTINGS_EDIT)
    self.permalink = base.Button(driver,
                                 self._locator.DROPDOWN_SETTINGS_PERMALINK)
    self.delete = base.Button(driver, self._locator.DROPDOWN_SETTINGS_DELETE)

  def select_edit(self):
    """
    Returns:
        lib.page.modal.edit_object.EditModal
    """
    self.edit.click()
    return getattr(modal.edit_object, self.__class__.__name__)(self._driver)

  def select_get_permalink(self):
    self.permalink.click()

  def select_delete(self):
    """
    Returns:
        modal.delete_object.DeleteObjectModal
    """
    self.delete.click()
    return modal.delete_object.DeleteObjectModal(self._driver)


class Programs(DropdownSettings):
  """A model for the settings dropdown on the program object"""


class Controls(DropdownSettings):
  """A model for the settings dropdown on the control object"""


class Processes(DropdownSettings):
  """A model for the settings dropdown on the process object"""


class DataAssets(DropdownSettings):
  """A model for the settings dropdown on the data asset object"""


class Systems(DropdownSettings):
  """A model for the settings dropdown on the system object"""


class Products(DropdownSettings):
  """A model for the settings dropdown on the products object"""


class Projects(DropdownSettings):
  """A model for the settings dropdown on the project object"""


class OrgGroups(DropdownSettings):
  """A model for the settings dropdown on the org group object"""
