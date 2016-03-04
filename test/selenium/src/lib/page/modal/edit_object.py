# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Modals for editing objects"""

from lib.constants import locator
from lib.page.modal import delete_object
from lib.page.modal import base as modal_base


class EditModal(modal_base._Modal):
  _button_delete_locator = locator.ModalEditObject.BUTTON_DELETE

  def delete_object(self):
    """
    Returns:
        delete_object.DeleteObjectModal
    """
    self._driver.find_element(*self._button_delete_locator).click()
    return delete_object.DeleteObjectModal(self._driver)


class EditProgramModal(modal_base.ProgramModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a program object and selecting edit"""


class EditControlModal(modal_base.ControlModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a control object and selecting edit"""


class EditRiskModal(modal_base.RiskModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a risk object and selecting edit"""


class EditOrgGroupModal(modal_base.OrgGroupModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a org group object and selecting edit"""
