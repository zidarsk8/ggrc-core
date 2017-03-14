# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Modals for create objects."""

from lib import base, decorator
from lib.constants import locator
from lib.page.modal import base as modal_base
from lib.utils import selenium_utils


class _CreateNewObjectModal(modal_base.BaseModal):
  """Modal for create objects."""
  _locator_button_add_another = (
      locator.ModalCreateNewObject.BUTTON_SAVE_AND_ADD_ANOTHER)

  def __init__(self, driver):
    super(_CreateNewObjectModal, self).__init__(driver)
    self.button_save_and_add_another = None

  def save_and_add_other(self):
    """Create object and open new Create modal."""
    self.button_save_and_add_another = base.Button(
        self._driver, self._locator_button_add_another)
    self.button_save_and_add_another.click()
    selenium_utils.get_when_invisible(
        self._driver, self._locator_button_add_another)
    return self.__class__(self._driver)

  @decorator.wait_for_redirect
  @decorator.handle_alert
  def save_and_close(self):
    """Create object and close Create modal."""
    self.button_save_and_close.click()
    selenium_utils.get_when_invisible(self._driver, self.locator_button_save)


class _GenerateNewObjectModal(base.Modal):
  """Modal for generate objects."""
  _locator_button_generate = locator.ModalGenerateNewObject.BUTTON_GENERATE

  def __init__(self, driver):
    super(_GenerateNewObjectModal, self).__init__(driver)
    self.button_generate_and_close = None

  def generate_and_close(self):
    """Generate object and close Generate modal."""
    self.button_generate_and_close = base.Button(
        self._driver, self._locator_button_generate)
    self.button_generate_and_close.click()
    selenium_utils.get_when_invisible(
        self._driver, self._locator_button_generate)


class ProgramsCreate(modal_base.ProgramsModal, _CreateNewObjectModal):
  # pylint: disable=abstract-method
  """Programs create modal."""


class ControlsCreate(modal_base.ControlsModal, _CreateNewObjectModal):
  """Controls create modal."""


class OrgGroupsCreate(modal_base.OrgGroupsModal, _CreateNewObjectModal):
  """Org Groups create modal."""


class RisksCreate(modal_base.RisksModal, _CreateNewObjectModal):
  """Risks create modal."""


class IssuesCreate(modal_base.IssuesModal, _CreateNewObjectModal):
  """Issues create modal."""


class ProcessesCreate(modal_base.ProcessesModal, _CreateNewObjectModal):
  """Processes create modal."""


class DataAssetsCreate(modal_base.DataAssetsModal, _CreateNewObjectModal):
  """Data Assets create modal."""


class SystemsCreate(modal_base.SystemsModal, _CreateNewObjectModal):
  """Systems create modal."""


class ProductsCreate(modal_base.ProductsModal, _CreateNewObjectModal):
  """Products create modal."""


class ProjectsCreate(modal_base.ProjectsModal, _CreateNewObjectModal):
  """Projects create modal."""


class AssessmentTemplatesCreate(modal_base.AsmtTmplModal,
                                _CreateNewObjectModal):
  """Assessment Templates create modal."""


class AssessmentsCreate(modal_base.AsmtsModal, _CreateNewObjectModal):
  """Assessments create modal."""


class AssessmentsGenerate(modal_base.AsmtsModalGenerate,
                          _GenerateNewObjectModal):
  """Assessments generate modal."""
