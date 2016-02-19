# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com
"""Models for the add widget button in the widget bar"""

from lib import base
from lib.constants import locator
import lib.page.widget


class AddWidget(base.Component):
  """No elements are initiated here because based on the context they may be
  missing"""

  _locator = locator.WidgetBarButtonAddDropdown

  def select_controls(self):
    """
    Returns:
        Controls
    """
    self._driver.find_element(*self._locator.CONTROLS).click()
    return lib.page.widget.Controls(self._driver)
