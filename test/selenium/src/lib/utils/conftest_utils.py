# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""PyTest fixture utils"""

from selenium.common import exceptions

from lib import cache
from lib import factory
from lib import constants
from lib.page import dashboard
from lib.utils import test_utils


def navigate_to_page_with_lhn(driver):
  """Navigates to dashboard it the LHN button isn't found"""
  # pylint: disable=invalid-name
  try:
    driver.find_element(*dashboard.Header.locators.TOGGLE_LHN)
  except exceptions.NoSuchElementException:
    driver.get(dashboard.Dashboard.URL)


def get_lhn_accordion(driver, object_name):
  """Selects the relevant section in LHN and returns the relevant section
  accordion"""
  navigate_to_page_with_lhn(driver)
  lhn_contents = dashboard.Header(driver).open_lhn_menu()

  # if the object button is not visible, we have to open it's section first
  if object_name in cache.LHN_SECTION_MEMBERS:
    method_name = factory.get_method_lhn_select(object_name)
    lhn_contents = getattr(lhn_contents, method_name)()

  return getattr(lhn_contents, constants.method.SELECT_PREFIX + object_name)()


def create_lhn_object(driver, object_name):
  """Creates a object via LHN"""
  modal = get_lhn_accordion(driver, object_name).create_new()
  factory.get_cls_test_utils(object_name).enter_test_data(modal)
  modal.save_and_close()
  return factory.get_cls_widget(object_name, is_info=True)(driver)


def delete_object_on_info_widget(driver, object_name):
  """Deletes a object when the info widget is opened"""
  factory.get_cls_widget(object_name, is_info=True)(driver)\
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()


def create_custom_program_attribute(driver):
  """Creates a custom text attribute for a program object"""
  driver.get(dashboard.AdminDashboard.URL)
  modal = dashboard.AdminDashboard(driver) \
      .select_custom_attributes() \
      .select_programs() \
      .add_new_custom_attribute()
  test_utils.ModalNewProgramCustomAttribute.enter_test_data(modal)
  return modal.save_and_close()
