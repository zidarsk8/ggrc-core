# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""PyTest fixture utils"""

from selenium.common import exceptions

from lib import test_helpers
from lib.page import dashboard
from lib.page import widget


def _navigate_to_page_that_contains_lhn(selenium):
  """Navigates to dashboard since dashboard always contains the LHN button"""
  # pylint: disable=invalid-name
  try:
    selenium.driver.find_element(*dashboard.HeaderPage.locator.TOGGLE_LHN)
  except exceptions.NoSuchElementException:
    selenium.driver.get(dashboard.DashboardPage.URL)


def lhn_create_control(selenium):
  """Creates a new control object via LHN

  Returns:
      lib.page.modal.new_program.NewControlModal
  """

  _navigate_to_page_that_contains_lhn(selenium)
  modal = dashboard.HeaderPage(selenium.driver) \
      .open_lhn_menu() \
      .select_controls_or_objectives() \
      .select_controls() \
      .create_new()
  test_helpers.ModalNewControlPage.enter_test_data(modal)
  modal.save_and_close()
  return widget.ControlInfo(selenium.driver)


def delete_control(selenium):
  """Deletes a control object when on control info widget"""
  widget.ControlInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


def create_custom_program_attribute(selenium):
  """Creates a custom text attribute for a program object"""
  # pylint: disable=redefined-outer-name

  modal = dashboard.AdminDashboardPage(selenium.driver) \
      .select_custom_attributes() \
      .select_programs() \
      .add_new_custom_attribute()
  test_helpers.ModalNewProgramCustomAttributePage.enter_test_data(modal)
  return modal.save_and_close()


def lhn_create_org_group(selenium):
  """Creates a new org group object

  Returns:
      lib.page.modal.new_program.NewOrgGroupModal
  """

  _navigate_to_page_that_contains_lhn(selenium)
  modal = dashboard.HeaderPage(selenium.driver) \
      .open_lhn_menu() \
      .select_people_or_groups() \
      .select_org_groups() \
      .create_new()
  test_helpers.ModalNewOrgGroupPage.enter_test_data(modal)
  modal.save_and_close()
  return widget.OrgGroupsInfo(selenium.driver)


def delete_org_group(selenium):
  """Deletes an org group object when on org group info widget"""
  widget.OrgGroupsInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


def lhn_create_risk(selenium):
  """Creates a new risk group object via LHN

  Returns:
      lib.page.modal.new_program.NewOrgGroupModal
  """

  _navigate_to_page_that_contains_lhn(selenium)
  modal = dashboard.HeaderPage(selenium.driver) \
      .open_lhn_menu() \
      .select_risks_or_threats() \
      .select_risks() \
      .create_new()
  test_helpers.ModalRiskPage.enter_test_data(modal)
  modal.save_and_close()
  return widget.RiskInfo(selenium.driver)


def delete_risk(selenium):
  """Deletes a risk object when on risk info widget"""
  widget.RiskInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


def lhn_create_program(selenium):
  """Creates a new program object via LHN"""
  # pylint: disable=redefined-outer-name

  _navigate_to_page_that_contains_lhn(selenium)
  modal = dashboard.HeaderPage(selenium.driver) \
      .open_lhn_menu() \
      .select_programs() \
      .create_new()

  test_helpers.ModalNewProgramPage.enter_test_data(modal)
  test_helpers.ModalNewProgramPage.set_start_end_dates(modal, 0, -1)
  modal.save_and_close()
  return modal, widget.ProgramInfo(selenium.driver)


def delete_program(selenium):
  """Deletes a program object when on program info widget"""
  widget.ProgramInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()
