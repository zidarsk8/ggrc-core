# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""PyTest fixtures"""

import pytest   # pylint: disable=import-error

from lib import constants
from lib import base
from lib.constants.test import batch
from lib.utils import conftest_utils
from lib.utils import test_utils


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
  cust_attr_widget = conftest_utils.create_custom_program_attribute(
      selenium.driver)
  yield cust_attr_widget
  # todo: delete this custom attribute


@pytest.yield_fixture(scope="class")
def new_control(selenium):
  """Creates a new control object.

  Returns:
      lib.page.widget.ControlsInfo
  """
  control_info_page = conftest_utils.create_lhn_object(
      selenium.driver, constants.element.Lhn.CONTROLS)
  yield control_info_page
  selenium.driver.get(control_info_page.url)
  conftest_utils.delete_object_on_info_widget(
      selenium.driver, constants.element.Lhn.CONTROLS)


@pytest.yield_fixture(scope="class")
def new_program(selenium, new_control):
  """Creates a new program object"""
  # pylint: disable=redefined-outer-name
  modal = conftest_utils.get_lhn_accordeon(
      selenium.driver, constants.element.Lhn.PROGRAMS)\
      .create_new()
  test_utils.ModalNewProgramsPage.enter_test_data(modal)
  program_info_page = modal.save_and_close()
  yield modal, program_info_page
  selenium.driver.get(program_info_page.url)
  conftest_utils.delete_object_on_info_widget(
      selenium.driver, constants.element.Lhn.PROGRAMS)


@pytest.yield_fixture(scope="class")
def new_org_group(selenium):
  """Creates a new org group object.

  Returns:
      lib.page.widget.OrgGroupInfo
  """
  org_group_page = conftest_utils.create_lhn_object(
      selenium.driver, constants.element.Lhn.ORG_GROUPS)
  yield org_group_page
  selenium.driver.get(org_group_page.url)
  conftest_utils.delete_object_on_info_widget(
      selenium.driver, constants.element.Lhn.ORG_GROUPS)


@pytest.yield_fixture(scope="class")
def new_risk(selenium):
  """Creates a new risk group object.

  Returns:
      lib.page.widget.RisksInfo
  """
  risk_page = conftest_utils.create_lhn_object(
      selenium.driver, constants.element.Lhn.RISKS)
  yield risk_page
  selenium.driver.get(risk_page.url)
  conftest_utils.delete_object_on_info_widget(
      selenium.driver, constants.element.Lhn.RISKS)



@pytest.yield_fixture(scope="class")
def new_request(selenium):
  """Creates a new request object.

  Returns:
      lib.page.widget.RequestsInfo
  """
  request_page = conftest_utils.create_lhn_object(
      selenium.driver, constants.element.Lhn.REQUESTS)
  yield request_page
  selenium.driver.get(request_page.url)
  conftest_utils.delete_object_on_info_widget(
      selenium.driver, constants.element.Lhn.REQUESTS)


@pytest.yield_fixture(scope="class")
def new_issue(selenium):
  """Creates a new request object.

  Returns:
      lib.page.widget.IssueInfo
  """
  issue_page = conftest_utils.create_lhn_object(
      selenium.driver, constants.element.Lhn.ISSUES)
  yield issue_page
  selenium.driver.get(issue_page.url)
  conftest_utils.delete_object_on_info_widget(
      selenium.driver, constants.element.Lhn.ISSUES)


@pytest.yield_fixture(scope="class")
def battery_of_controls(selenium):
  """Creates 3 control objects"""
  controls = []

  for _ in xrange(batch.BATTERY):
    controls.append(conftest_utils.create_lhn_object(
        selenium.driver, constants.element.Lhn.CONTROLS))

  yield controls
