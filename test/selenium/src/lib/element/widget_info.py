# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib.constants import locator
from lib.page import widget_modal
from lib.page import lhn_modal


class _DropdownSettings(base.Component):
  _locator = locator.Widget

  def __init__(self, driver):
    super(_DropdownSettings, self).__init__(driver)
    self.edit = base.Button(driver, self._locator.DROPDOWN_SETTINGS_EDIT)
    self.permalink = base.Button(driver,
                                 self._locator.DROPDOWN_SETTINGS_PERMALINK)
    self.delete = base.Button(driver, self._locator.DROPDOWN_DELETE)

  def select_edit(self):
    raise NotImplementedError

  def select_get_permalink(self):
    self.permalink.click()

  def select_delete(self):
    """
    Returns:
        DeleteObjectModal
    """
    self.delete.click()
    return widget_modal.DeleteObjectModal(self._driver)


class DropdownSettingsPrograms(_DropdownSettings):
  def select_edit(self):
    """
    Returns:
        lhn_modal.new_program.NewProgramModal
    """
    self.edit.click()
    return lhn_modal.new_program.EditProgramModal(self._driver)
