# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Modals for editing objects"""

from lib.constants import locator
from lib.page.modal import delete_object
from lib.page.modal import base as modal_base


class EditModal(modal_base._EditModal):
  _button_delete_locator = locator.ModalEditObject.BUTTON_DELETE

  def delete_object(self):
    """
    Returns:
        delete_object.DeleteObjectModal
    """
    self._driver.find_element(*self._button_delete_locator).click()
    return delete_object.DeleteObjectModal(self._driver)


class Programs(modal_base.ProgramsModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a program object and selecting edit"""


class Controls(modal_base.ControlsModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a control object and selecting edit"""


class Risks(modal_base.RisksModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a risk object and selecting edit"""


class OrgGroups(modal_base.OrgGroupsModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a org group object and selecting edit"""


class Processes(modal_base.ProcessesModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a process object and selecting edit"""


class DataAssets(modal_base.RisksModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a data asset object and selecting edit"""


class Systems(modal_base.RisksModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a system object and selecting edit"""


class Products(modal_base.ProductsModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a product object and selecting edit"""


class Projects(modal_base.ProjectsModal, EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a project object and selecting edit"""
