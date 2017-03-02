# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""PyTest fixture utils."""

from selenium.common import exceptions

from lib import cache, constants, factory
from lib.page import dashboard


def navigate_to_page_with_lhn(driver):
  """Navigates to dashboard it the LHN button isn't found"""
  # pylint: disable=invalid-name
  try:
    driver.find_element(*dashboard.Header.locators.TOGGLE_LHN)
  except exceptions.NoSuchElementException:
    driver.get(dashboard.Dashboard.URL)


def get_lhn_accordion(driver, object_name):
  """Selects the relevant section in LHN and return the relevant
  section accordion.
  """
  navigate_to_page_with_lhn(driver)
  lhn_contents = dashboard.Header(driver).open_lhn_menu()
  # if the object button is not visible, we have to open it's section first
  if object_name in cache.LHN_SECTION_MEMBERS:
    method_name = factory.get_method_lhn_select(object_name)
    lhn_contents = getattr(lhn_contents, method_name)()
  return getattr(lhn_contents, constants.method.SELECT_PREFIX + object_name)()


def create_obj_via_lhn(driver, object_name):
  """Creates an object via LHN."""
  modal = get_lhn_accordion(driver, object_name).create_new()
  factory.get_cls_test_utils(object_name).enter_test_data(modal)
  modal.save_and_close()
  return factory.get_cls_widget(object_name, is_info=True)(driver)


def delete_obj_via_info_widget(driver, object_name):
  """Delete an object via Info Widget."""
  factory.get_cls_widget(object_name, is_info=True)(driver)\
      .press_object_settings() \
      .select_delete() \
      .confirm_delete()
