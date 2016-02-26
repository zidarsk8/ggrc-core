# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""PyTest fixture utils"""

from selenium.common import exceptions

from lib import test_helpers
from lib.page import dashboard
from lib.page import widget


def navigate_to_page_that_contains_lhn(driver):
  """Navigates to dashboard since dashboard always contains the LHN button
  Args:
      driver (lib.base.CustomDriver)
  """
  # pylint: disable=invalid-name
  try:
    driver.find_element(*dashboard.HeaderPage.locator.TOGGLE_LHN)
  except exceptions.NoSuchElementException:
    driver.get(dashboard.DashboardPage.URL)


def lhn_create_control(driver):
  """Creates a new control object via LHN

  Args:
      driver (lib.base.CustomDriver)
  Returns:
      lib.page.modal.new_program.NewControlModal
  """

  navigate_to_page_that_contains_lhn(driver)
  modal = dashboard.HeaderPage(driver) \
      .open_lhn_menu() \
      .select_controls_or_objectives() \
      .select_controls() \
      .create_new()
  test_helpers.ModalNewControlPage.enter_test_data(modal)
  modal.save_and_close()
  return widget.ControlInfo(driver)


def delete_control(driver):
  """Deletes a control object when on control info widget

  Args:
      driver (lib.base.CustomDriver)
  """
  widget.ControlInfo(driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


def create_custom_program_attribute(driver):
  """Creates a custom text attribute for a program object
  Args:
      driver (lib.base.CustomDriver)
  """
  # pylint: disable=redefined-outer-name

  modal = dashboard.AdminDashboardPage(driver) \
      .select_custom_attributes() \
      .select_programs() \
      .add_new_custom_attribute()
  test_helpers.ModalNewProgramCustomAttributePage.enter_test_data(modal)
  return modal.save_and_close()


def lhn_create_org_group(driver):
  """Creates a new org group object

  Args:
      driver (lib.base.CustomDriver)
  Returns:
      lib.page.modal.new_program.NewOrgGroupModal
  """

  navigate_to_page_that_contains_lhn(driver)
  modal = dashboard.HeaderPage(driver) \
      .open_lhn_menu() \
      .select_people_or_groups() \
      .select_org_groups() \
      .create_new()
  test_helpers.ModalNewOrgGroupPage.enter_test_data(modal)
  modal.save_and_close()
  return widget.OrgGroupsInfo(driver)


def delete_org_group(driver):
  """Deletes an org group object when on org group info widget
  Args:
      driver (lib.base.CustomDriver)
  """
  widget.OrgGroupsInfo(driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


def lhn_create_risk(driver):
  """Creates a new risk group object via LHN

  Args:
      driver (lib.base.CustomDriver)
  Returns:
      lib.page.modal.new_program.NewOrgGroupModal
  """

  navigate_to_page_that_contains_lhn(driver)
  modal = dashboard.HeaderPage(driver) \
      .open_lhn_menu() \
      .select_risks_or_threats() \
      .select_risks() \
      .create_new()
  test_helpers.ModalRiskPage.enter_test_data(modal)
  modal.save_and_close()
  return widget.RiskInfo(driver)


def delete_risk(driver):
  """Deletes a risk object when on risk info widget
  Args:
      driver (lib.base.CustomDriver)
  """
  widget.RiskInfo(driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


def lhn_create_program(driver):
  """Creates a new program object via LHN
  Args:
      driver (lib.base.CustomDriver)
  """
  # pylint: disable=redefined-outer-name

  navigate_to_page_that_contains_lhn(driver)
  modal = dashboard.HeaderPage(driver) \
      .open_lhn_menu() \
      .select_programs() \
      .create_new()

  test_helpers.ModalNewProgramPage.enter_test_data(modal)
  test_helpers.ModalNewProgramPage.set_start_end_dates(modal, 0, -1)
  modal.save_and_close()
  return modal, widget.ProgramInfo(driver)


def delete_program(driver):
  """Deletes a program object when on program info widget
  Args:
      driver (lib.base.CustomDriver)
  """
  widget.ProgramInfo(driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()
