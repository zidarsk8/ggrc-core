# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""PyTest fixture utils"""

from lib import test_helpers
from lib.constants.test import batch
from lib.page import dashboard
from lib.page import widget
from lib.page import login
from lib.page import lhn


def _navigate_to_page_that_contains_lhn(selenium):
  # pylint: disable=invalid-name
  if selenium.driver.current_url in [login.LoginPage.URL, "data:,"]:
    selenium.driver.get(dashboard.DashboardPage.URL)


def create_control(selenium):
  """Creates a new control object.

  Returns:
      lib.page.modal.new_program.NewControlModal
  """

  _navigate_to_page_that_contains_lhn(selenium)
  modal = dashboard.HeaderPage(selenium.driver) \
      .open_lhn_menu() \
      .select_my_objects() \
      .select_controls_or_objectives() \
      .select_controls() \
      .create_new()
  test_helpers.ModalNewControlPage.enter_test_data(modal)
  modal.save_and_close()
  return widget.ControlInfo(selenium.driver)


def create_controls(selenium):
  """Creates a new control object.

  Returns:
      list(widget.ControlInfo)
  """

  _navigate_to_page_that_contains_lhn(selenium)
  objects = []
  objects.append(create_control(selenium))

  for _ in xrange(batch.BATTERY - 1):
    dashboard.HeaderPage(selenium.driver) \
        .open_lhn_menu() \
        .select_my_objects()
    modal = lhn.Controls(selenium.driver).create_new()
    test_helpers.ModalNewControlPage.enter_test_data(modal)
    modal.save_and_close()
    objects.append(widget.ControlInfo(selenium.driver))

  return objects


def delete_control(selenium):
  widget.ControlInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


def create_custom_program_attribute(selenium):
  """Creates a custom attribute for a program object"""
  # pylint: disable=redefined-outer-name

  modal = dashboard.AdminDashboardPage(selenium.driver) \
      .select_custom_attributes() \
      .select_programs() \
      .add_new_custom_attribute()
  test_helpers.ModalNewProgramCustomAttributePage.enter_test_data(modal)
  return modal.save_and_close()


def create_org_group(selenium):
  """Creates a new org group object.

  Returns:
      lib.page.modal.new_program.NewOrgGroupModal
  """

  _navigate_to_page_that_contains_lhn(selenium)
  modal = dashboard.HeaderPage(selenium.driver) \
      .open_lhn_menu() \
      .select_my_objects() \
      .select_people_or_groups() \
      .select_org_groups() \
      .create_new()
  test_helpers.ModalNewOrgGroupPage.enter_test_data(modal)
  modal.save_and_close()
  return widget.OrgGroupsInfo(selenium.driver)


def delete_org_group(selenium):
  widget.OrgGroupsInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


def create_risk(selenium):
  """Creates a new risk group object.

  Returns:
      lib.page.modal.new_program.NewOrgGroupModal
  """

  _navigate_to_page_that_contains_lhn(selenium)
  modal = dashboard.HeaderPage(selenium.driver) \
      .open_lhn_menu() \
      .select_my_objects() \
      .select_risks_or_threats() \
      .select_risks() \
      .create_new()
  test_helpers.ModalRiskPage.enter_test_data(modal)
  modal.save_and_close()
  return widget.RiskInfo(selenium.driver)


def delete_risk(selenium):
  widget.RiskInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


def create_program(selenium):
  """Creates a new program object"""
  # pylint: disable=redefined-outer-name

  _navigate_to_page_that_contains_lhn(selenium)
  modal = dashboard.HeaderPage(selenium.driver) \
      .open_lhn_menu() \
      .select_my_objects() \
      .select_programs() \
      .create_new()

  test_helpers.ModalNewProgramPage.enter_test_data(modal)
  test_helpers.ModalNewProgramPage.set_start_end_dates(modal, 0, -1)
  modal.save_and_close()
  return modal, widget.ProgramInfo(selenium.driver)


def delete_program(selenium):
  widget.ProgramInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()
