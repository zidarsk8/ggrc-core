# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

import pytest
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
  selenium = base.Selenium()
  yield selenium

  selenium.close_resources()


@pytest.yield_fixture(scope="class")
def custom_program_attribute(selenium):
  modal = dashboard.AdminDashboardPage(selenium.driver) \
      .select_custom_attributes() \
      .select_programs() \
      .add_new_custom_attribute()
  test_helpers.ModalNewProgramCustomAttribute.enter_test_data(modal)
  cust_attr_widget = modal.save_and_close()

  yield cust_attr_widget

  # todo: delete this custom attribute


@pytest.yield_fixture(scope="class")
def initial_lhn(selenium):
  """
  Returns:
      lib.page.lhn.LhnContents
  """
  lhn_contents = dashboard.DashboardPage(selenium.driver) \
      .open_lhn_menu() \
      .select_my_objects()
  yield lhn_contents


@pytest.yield_fixture(scope="class")
def new_program(selenium):
  """Creates a new program object.

  Returns:
      lib.page.modal.new_program.NewProgramModal
  """
  modal = dashboard.DashboardPage(selenium.driver) \
      .open_lhn_menu() \
      .select_my_objects() \
      .select_programs() \
      .create_new()

  test_helpers.ModalNewProgramPage.enter_test_data(modal)
  program_info_page = modal.save_and_close()

  yield modal, program_info_page

  selenium.driver.get(program_info_page.url)
  widget.ProgramInfo(selenium.driver) \
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()
