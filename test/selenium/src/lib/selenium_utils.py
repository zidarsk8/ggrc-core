# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Utility function for selenium"""

# pylint: disable=import-error
from selenium.webdriver.support import expected_conditions as EC

# pylint: disable=import-error
from selenium.webdriver.support.ui import WebDriverWait

import time
from lib import exception
from lib import constants


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
