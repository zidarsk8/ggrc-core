# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Modals for editing objects"""

from lib import decorator
from lib.constants import locator
from lib.page.modal import delete_object
from lib.page.modal import base as modal_base


class _EditModal(modal_base.BaseModal):
  _button_delete_locator = locator.ModalEditObject.BUTTON_DELETE

  def delete_object(self):
    """
    Returns:
        delete_object.DeleteObjectModal
    """
    self._driver.find_element(*self._button_delete_locator).click()
    return delete_object.DeleteObjectModal(self._driver)

  @decorator.handle_alert
  def save_and_close(self):
    """Saves this object"""
    self.button_save_and_close.click()


class Programs(modal_base.ProgramsModal, _EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a program object and selecting edit"""


class Controls(modal_base.ControlsModal, _EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a control object and selecting edit"""


class Risks(modal_base.RisksModal, _EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a risk object and selecting edit"""


class OrgGroups(modal_base.OrgGroupsModal, _EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a org group object and selecting edit"""


class Processes(modal_base.ProcessesModal, _EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a process object and selecting edit"""


class DataAssets(modal_base.RisksModal, _EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a data asset object and selecting edit"""


class Systems(modal_base.RisksModal, _EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a system object and selecting edit"""


class Products(modal_base.ProductsModal, _EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a product object and selecting edit"""


class Projects(modal_base.ProjectsModal, _EditModal):
  """Class representing a modal visible after clicking the settings button
  in the info widget of a project object and selecting edit"""
