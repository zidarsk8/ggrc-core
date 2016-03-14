# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""A module for extended info page models (visible in LHN on hover over
object members)"""

from selenium.common import exceptions

from lib import base
from lib.constants import locator


class ExtendedInfo(base.Component):
  """Model representing an extended info box that allows the object to be
  mapped"""
  _locator = locator.ExtendedInfo

  def __init__(self, driver):
    super(ExtendedInfo, self).__init__(driver)
    self.button_map = None

  def _reload_contents(self):
    self.button_map = base.Button(
      self._driver, self._locator.BUTTON_MAP_TO)

  def map_to_object(self):
    try:
      self.button_map = base.Button(
        self._driver, self._locator.BUTTON_MAP_TO)
      self.button_map.click()
    except exceptions.StaleElementReferenceException:
      self._reload_contents()
      return self.map_to_object()

  def is_already_mapped(self):
    """Checks if the object is already mapped"""
    try:
      self._driver.find_element(*self._locator.ALREADY_MAPPED)
      return True
    except exceptions.NoSuchElementException:
      return False
