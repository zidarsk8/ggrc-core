# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Models for the control widget"""

from lib import base
from lib.page.widget import info
from lib.constants import locator


class Controls(base.ObjectWidget):
  """Model for the control widget"""

  _info_pane_cls = info.ControlInfo

  def __init__(self, driver,):
    super(Controls, self).__init__(
        driver,
        locator.WidgetBar.CONTROLS,
        locator.WidgetFilter.TITLE_CONTROL,
        locator.WidgetFilter.BUTTON_HELP,
        locator.WidgetFilter.TEXTFIELD_CONTROL,
        locator.WidgetFilter.BUTTON_SUBMIT_CONTROL,
        locator.WidgetFilter.BUTTON_RESET_CONTROL
    )
    self.label_control_title = base.Label(
        driver,
        locator.ObjectWidget.CONTROL_COLUMN_TITLE)
    self.label_owner = base.Label(driver, locator.ObjectWidget.CONTROL_OWNER)
    self.label_state = base.Label(driver, locator.ObjectWidget.COTNROL_STATE)
