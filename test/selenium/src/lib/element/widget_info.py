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

  _delete_modal_cls = None
  _edit_modal_cls = None

  def __init__(self, driver):
    super(DropdownSettings, self).__init__(driver)
    self.edit = None
    self.permalink = None
    self.delete = None

  def select_edit(self):
    """
    Returns:
        base.Modal
    """
    self.edit.click()
    selenium_utils.get_when_visible(
        self._driver, self._edit_modal_cls.locator_button_save)
    return self._edit_modal_cls(self._driver)

  def select_get_permalink(self):
    self.permalink.click()

  def select_delete(self):
    """
    Returns:
        moda.delete_object.DeleteObjectModal
    """
    self.delete.click()
    return self._delete_modal_cls(self._driver)


class DropdownSettingsPrograms(DropdownSettings):
  _locator = locator.ProgramInfoWidget
  _delete_modal_cls = modal.delete_object.DeleteProgramModal
  _edit_modal_cls = modal.edit_object.EditProgramModalBase

  def __init__(self, driver):
    super(DropdownSettings, self).__init__(driver)
    self.edit = base.Button(driver, self._locator.DROPDOWN_SETTINGS_EDIT)
    self.permalink = base.Button(driver,
                                 self._locator.DROPDOWN_SETTINGS_PERMALINK)
    self.delete = base.Button(driver, self._locator.DROPDOWN_DELETE)
