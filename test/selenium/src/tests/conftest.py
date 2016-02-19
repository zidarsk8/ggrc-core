# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""PyTest fixtures"""

import pytest   # pylint: disable=import-error
from lib import base
from lib import test_helpers
from lib.page import dashboard
from lib.page import widget


@pytest.yield_fixture(scope="session")
def db_drop():
  """Reset the DB"""
  # todo
  pass


@pytest.yield_fixture(scope="session")
def db_migrate():
  """Make sure the DB is up to date"""
  # todo
  pass


@pytest.yield_fixture(scope="class")
def selenium():
  """Setup test resources for running test in headless mode.

  Returns:
      base.CustomDriver
  """
  selenium_base = base.Selenium()
  yield selenium_base

  selenium_base.close_resources()


@pytest.yield_fixture(scope="class")
def custom_program_attribute(selenium):
  """Creates a custom attribute for a program object"""
  # pylint: disable=redefined-outer-name
  modal = dashboard.AdminDashboardPage(selenium.driver) \
      .select_custom_attributes() \
      .select_programs() \
      .add_new_custom_attribute()
  test_helpers.ModalNewProgramCustomAttributePage.enter_test_data(modal)
  cust_attr_widget = modal.save_and_close()

  yield cust_attr_widget

  # todo: delete this custom attribute


@pytest.yield_fixture(scope="class")
def initial_lhn(selenium):
  """
  Returns:
      lib.page.lhn.LhnContents
  """
  # pylint: disable=redefined-outer-name
  lhn_contents = dashboard.DashboardPage(selenium.driver) \
      .open_lhn_menu() \
      .select_my_objects()
  yield lhn_contents


@pytest.yield_fixture(scope="class")
def new_control(selenium):
  """Creates a new control object.

  Returns:
      lib.page.modal.new_program.NewControlModal
  """
  modal = dashboard.DashboardPage(selenium.driver) \
      .open_lhn_menu() \
      .select_my_objects() \
      .select_controls_or_objectives() \
      .select_controls() \
      .create_new()
  test_helpers.ModalNewControlPage.enter_test_data(modal)
  modal.save_and_close()
  control_info_page = widget.ControlInfo(selenium.driver)

  yield control_info_page

  selenium.driver.get(control_info_page.url)
  widget.ControlInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


@pytest.yield_fixture(scope="class")
def new_program(selenium, new_control):
  """Creates a new program object.

  Returns:
      lib.page.modal.new_program.NewProgramModal
  """
  # pylint: disable=redefined-outer-name
  modal = dashboard.DashboardPage(selenium.driver) \
      .open_lhn_menu() \
      .select_my_objects() \
      .select_programs() \
      .create_new()

  test_helpers.ModalNewProgramPage.enter_test_data(modal)
  test_helpers.ModalNewProgramPage.set_start_end_dates(modal, 0, -1)
  modal.save_and_close()
  program_info_page = widget.ProgramInfo(selenium.driver)

  yield modal, program_info_page

  selenium.driver.get(program_info_page.url)
  widget.ProgramInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


@pytest.yield_fixture(scope="class")
def new_org_group(selenium):
  """Creates a new org group object.

  Returns:
      lib.page.modal.new_program.NewOrgGroupModal
  """
  modal = dashboard.DashboardPage(selenium.driver) \
      .open_lhn_menu() \
      .select_my_objects() \
      .select_people_or_groups() \
      .select_org_groups() \
      .create_new()
  test_helpers.ModalNewOrgGroupPage.enter_test_data(modal)
  modal.save_and_close()
  org_group_page = widget.OrgGroupsInfo(selenium.driver)

  yield org_group_page

  selenium.driver.get(org_group_page.url)
  widget.OrgGroupsInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()
