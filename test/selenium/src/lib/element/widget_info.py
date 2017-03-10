# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Info Widget and Info Panel elements."""

from lib import base
from lib.constants import locator
from lib.page.modal import (delete_object, edit_object, update_object,
                            clone_object)


class CommonDropdownSettings(base.Component):
  """Common for 3BBS button/dropdown settings on
 Info widgets and Info panels.
 """
  _locator = locator.CommonDropdown3bbsInfoWidget

  def __init__(self, driver):
    super(CommonDropdownSettings, self).__init__(driver)

  def select_edit(self):
    """
    Return: lib.page.modal.edit_object.EditModal
    """
    base.Button(self._driver, self._locator.BUTTON_3BBS_EDIT).click()
    return getattr(edit_object, self.__class__.__name__)(self._driver)

  def select_get_permalink(self):
    "Select get permalink."
    base.Button(self._driver, self._locator.BUTTON_3BBS_GET_PERMALINK).click()

  def select_delete_obj(self):
    """
    Return: modal.delete_object.DeleteObjectModal
    """
    base.Button(self._driver, self._locator.BUTTON_3BBS_DELETE).click()
    return delete_object.DeleteObjectModal(self._driver)


class Audits(CommonDropdownSettings):
  """Dropdown settings on Audit Info widgets and Info panels."""
  _locator = locator.AuditDropdown3bbsInfoWidget

  def __init__(self, driver):
    super(Audits, self).__init__(driver)

  def select_update_objs(self):
    """
    Return: modal.update_object.CompareUpdateObjectModal
    """
    base.Button(self._driver, self._locator.BUTTON_3BBS_UPDATE).click()
    return update_object.CompareUpdateObjectModal(self._driver)

  def select_clone(self):
    """
    Return: modal.clone_object.CloneAuditModal
    """
    base.Button(self._driver, self._locator.BUTTON_3BBS_CLONE).click()
    return clone_object.CloneAuditModal(self._driver)


class Programs(CommonDropdownSettings):
  """Dropdown settings on Program Info widgets and Info panels."""


class Controls(CommonDropdownSettings):
  """Dropdown settings on Control Info widgets and Info panels."""


class Processes(CommonDropdownSettings):
  """Dropdown settings on Process Info widgets and Info panels."""


class DataAssets(CommonDropdownSettings):
  """Dropdown settings on Data Asset Info widgets and Info panels."""


class Systems(CommonDropdownSettings):
  """Dropdown settings on System Info widgets and Info panels."""


class Products(CommonDropdownSettings):
  """Dropdown settings on Product Info widgets and Info panels."""


class Projects(CommonDropdownSettings):
  """Dropdown settings on Project Info widgets and Info panels."""


class OrgGroups(CommonDropdownSettings):
  """Dropdown settings on Org Group Info widgets and Info panels."""
