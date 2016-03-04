# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""A module for extended info page models (visible in LHN on hover over
object members)"""

from lib import base
from lib.constants import locator


class ExtendedInfoMappable(base.Component):
  """Model representing an extended info box that allows the object to be
  mapped"""
  def __init__(self, driver):
    super(ExtendedInfoMappable, self).__init__(driver)
    self.button_map = base.Button(driver, locator.ExtendedInfo.BUTTON_MAP_TO)

  def map_to_object(self):
    self.button_map.click()
