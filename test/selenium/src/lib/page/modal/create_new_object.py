# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Modals for creating new objects"""

from lib import base
from lib.constants import locator
from lib.page.modal import base as modal_base


class CreateNewObjectModal(base.Modal):
  """Base create modal model"""

  _locator_button_add_another = locator.ModalCreateNewObject\
      .BUTTON_SAVE_AND_ADD_ANOTHER

  def __init__(self, driver):
    super(CreateNewObjectModal, self).__init__(driver)
    self.button_save_and_add_another = base.Button(
        driver, self._locator_button_add_another)

  def save_and_add_other(self):
    """Saves this objects and opens a new modal"""
    self.button_save_and_add_another.click()
    return self.__class__(self._driver)


class NewProgramModal(modal_base.ProgramModal, CreateNewObjectModal):
  """Class representing a program modal visible after creating a new
  program from LHN"""


class NewControlModal(modal_base.ControlModal, CreateNewObjectModal):
  """Class representing a control modal visible after creating a new
  control from LHN"""


class NewOrgGroupModal(modal_base.OrgGroupModal, CreateNewObjectModal):
  """Class representing an org group modal visible after creating a new
  org group from LHN"""


class NewRiskModal(modal_base.RiskModal, CreateNewObjectModal):
  """Class representing a risk modal visible after creating a new
  risk from LHN"""
