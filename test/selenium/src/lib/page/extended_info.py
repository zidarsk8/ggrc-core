# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com
"""A modul for extended info page models (visible in LHN on hover over
object members)"""

from lib import base
from lib import selenium_utils
from lib.constants import locator


class _ExtendedInfo(base.Component):
  pass


class ExtendedInfoMappable(_ExtendedInfo):
  """Model representing an extended info box that allows the object to be
  mapped"""
  _locator_redirected_to_widget = None

  def __init__(self, driver):
    super(ExtendedInfoMappable, self).__init__(driver)
    self.button_map = base.Button(driver, locator.ExtendedInfo.BUTTON_MAP_TO)

  def map_to_object(self):
    self.button_map.click()
    selenium_utils.get_when_visible(
      self._driver, self._locator_redirected_to_widget)


class Controls(ExtendedInfoMappable):
  """Extended info for controls"""

  _locator_redirected_to_widget = locator.WidgetBar.CONTROLS

  def __init__(self, driver):
    super(Controls, self).__init__(driver)
