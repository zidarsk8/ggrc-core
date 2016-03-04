# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Models for the custom attribute widget"""

from lib.page.widget import base
from lib.constants import locator


class AdminCustomAttributes(base.WidgetAdminCustomAttributes):
  """Model for custom attributes widget on the admin dashboard page"""

  def select_programs(self):
    """
    Returns:
        DropdownPrograms
    """
    self.button_programs.click()
    return DropdownPrograms(self._driver)


class NewCustomAttributeModal(base.CustomAttributeModal,
                              base.CreateNewCustomAttributeModal):
  """Model for the custom attribute modal"""


class DropdownPrograms(base.Dropdown):
  """Model for programs dropdown"""

  _locator_button_add = locator.AdminCustomAttributes\
      .BUTTON_ADD_CUSTOM_PROGRAM_ATTR
  _locator_label_attribute_name = locator.AdminCustomAttributes\
      .PROGRAMS_LABEL_ATTRIBUTE_NAME
  _locator_label_attribute_type = locator.AdminCustomAttributes\
      .PROGRAMS_LABEL_ATTRIBUTE_TYPE
  _locator_label_mandatory = locator.AdminCustomAttributes\
      .PROGRAMS_LABEL_MANDATORY
  _locator_label_edit = locator.AdminCustomAttributes.PROGRAMS_LABEL_EDIT
  _locator_listed_members = locator.AdminCustomAttributes.LISTED_MEMBERS
  _locator_buttons_edit = locator.AdminCustomAttributes\
      .BUTTON_LISTED_MEMBERS_EDIT
  _cls_new_attrb_modal = NewCustomAttributeModal
