# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Elements for info widget"""

from lib import base
from lib import selenium_utils
from lib.page import modal
from lib.constants import locator


class DropdownSettings(base.Component):
  """A class for the button/dropdown settings in the info widget"""

  _locator = locator.WidgetInfoSettingsButton
  _edit_modal_cls = None

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
    selenium_utils.get_when_visible(
        self._driver, self._edit_modal_cls.locator_button_save)

    # pylint: disable=not-callable
    return self._edit_modal_cls(self._driver)

  def select_get_permalink(self):
    self.permalink.click()

  def select_delete(self):
    """
    Returns:
        modal.delete_object.DeleteObjectModal
    """
    self.delete.click()
    return modal.delete_object.DeleteObjectModal(self._driver)


class DropdownSettingsPrograms(DropdownSettings):
  """A model for the settings dropdown on the program object"""

  _edit_modal_cls = modal.edit_object.EditProgramModal


class DropdownSettingsControls(DropdownSettings):
  """A model for the settings dropdown on the program object"""

  _edit_modal_cls = modal.edit_object.EditControlModal
