# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Utility function for selenium"""

import time
import logging

# pylint: disable=import-error
from selenium.webdriver.support import expected_conditions as EC
# pylint: disable=import-error
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common import action_chains
from selenium.common import exceptions

from lib import exception
from lib import constants

logger = logging.getLogger(__name__)


def hover_over_element(driver, element):
  """Moves the mouse pointer to the element and hovers"""
  action_chains.ActionChains(driver).move_to_element(element).perform()


def wait_until_stops_moving(element):
  """Waits until the element stops moving

  Args:
      selenium.webdriver.remote.webelement.WebElement
  """

  prev_location = None
  timer_begin = time.time()

  while prev_location != element.location:
    prev_location = element.location
    time.sleep(0.1)

    if time.time() - timer_begin > constants.ux.ELEMENT_MOVING_TIMEOUT:
      raise exception.ElementMovingTimeout


def get_when_visible(driver, locator):
  """
  Args:
    driver (base.CustomDriver)
    locator (tuple)

  Returns:
      selenium.webdriver.remote.webelement.WebElement
  """
  return WebDriverWait(
      driver,
      constants.ux.MAX_USER_WAIT_SECONDS) \
      .until(EC.visibility_of_element_located(locator))


def get_when_clickable(driver, locator):
  """
  Args:
    driver (base.CustomDriver)
    locator (tuple)

  Returns:
      selenium.webdriver.remote.webelement.WebElement
  """
  return WebDriverWait(
      driver,
      constants.ux.MAX_USER_WAIT_SECONDS) \
      .until(EC.element_to_be_clickable(locator))


def get_when_invisible(driver, locator):
  """
  Args:
    driver (base.CustomDriver)
    locator (tuple)

  Returns:
      selenium.webdriver.remote.webelement.WebElement
  """
  return WebDriverWait(
      driver,
      constants.ux.MAX_USER_WAIT_SECONDS) \
      .until(EC.invisibility_of_element_located(locator))


def scroll_to_page_bottom(driver):
  """Scrolls to te page bottom using JS

  Args:
      driver (base.CustomDriver)
  """
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def is_value_in_attr(element, attr="class", value="active"):
  """Checks if the attribute value is present for given attribute

  Args:
    element (selenium.webdriver.remote.webelement.WebElement)
    attr (basestring): attribute name e.g. "class"
    value (basestring): value in the class attribute that
      indicates the element is now active/opened

  Returns:
      bool
  """
  attributes = element.get_attribute(attr)
  return value in attributes.split()


def wait_until_alert_is_present(driver):
  """
  Waits until an alert is present
  Args:
    driver (base.CustomDriver)

  Returns:
      selenium.webdriver.common.alert.Alert
  """
  return WebDriverWait(
      driver,
      constants.ux.MAX_ALERT_WAIT) \
      .until(EC.alert_is_present())


def handle_alert(driver, accept=False):
  """Wait until an alert is present and make a decision to accept or dismiss
  it"""
  try:
    wait_until_alert_is_present(driver)
    alert = driver.switch_to.alert

    if accept:
      alert.accept()
    else:
      alert.dismiss()
  except (exceptions.NoAlertPresentException, exceptions.TimeoutException):
    pass


def click_on_staleable_element(driver, el_locator):
  """Clicks an element that can be modified between the time we find it
  and when we click on it."""
  time_start = time.time()

  while time.time() - time_start < constants.ux.MAX_USER_WAIT_SECONDS:
    try:
      driver.find_element(*el_locator).click()
      break
    except exceptions.StaleElementReferenceException as e:
      logger.error(e)
      time.sleep(0.1)
  else:
    raise exception.ElementNotFound(el_locator)


def scroll_into_view(driver, element):
  driver.execute_script("return arguments[0].scrollIntoView();", element)

  # compensate for the header
  driver.execute_script(
      "window.scrollBy(0, -{});".format(constants.element.SIZE_HEADER))
  return element
