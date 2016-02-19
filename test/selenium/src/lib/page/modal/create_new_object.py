# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Modals for creating new objects"""

from lib import base
from lib.constants import locator
from lib.page.modal import edit_object


class _CreateNewObjectModal(base.Modal):
  _locator_button_add_another = None

  def __init__(self, driver):
    super(_CreateNewObjectModal, self).__init__(driver)
    self.button_save_and_add_another = base.Button(
        driver, self._locator_button_add_another)

  def save_and_add_other(self):
    """Saves this objects and opens a new modal"""
    self.button_save_and_add_another.click()
    return self.__class__(self._driver)


class NewProgramModal(_CreateNewObjectModal, edit_object.EditProgramModal):
  """Class representing a program modal visible after creating a new
  program from LHN"""

  _locator_button_add_another = locator.ModalCreateNewProgram\
      .BUTTON_SAVE_AND_ADD_ANOTHER


class NewControlModal(_CreateNewObjectModal, edit_object.EditControlModal):
  """Class representing a control modal visible after creating a new
  control from LHN"""

  _locator_button_add_another = locator.ModalCreateNewControl\
      .BUTTON_SAVE_AND_ADD_ANOTHER


class NewOrgGroupModal(_CreateNewObjectModal, edit_object.EditOrgGroupModal):
  """Class representing an org group modal visible after creating a new
  program from LHN"""

  _locator_button_add_another = locator.ModalCreateNewOrgGroup \
      .BUTTON_SAVE_AND_ADD_ANOTHER
