# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Export page with Export Panels."""

from lib import base
from lib.constants import locator
from lib.utils import selenium_utils


class ExportPanel(base.Component):
  """Export Panel on Export Page."""

  def __init__(self, driver, export_panel):
    super(ExportPanel, self).__init__(driver)


class ExportPage(base.Page):
  """Export Page."""
  _locators = locator.ExportPage

  def __init__(self, driver):
    super(ExportPage, self).__init__(driver)
    self.export_page = self._driver.find_element(*self._locators.EXPORT_PAGE)
    self.export_panels = self.get_list_export_panels()

  def get_list_export_panels(self):
    """Get list of all Export Panels witch are presented on Export Page at the
    moment of getting.
    """
    return [ExportPanel(self._driver, exp_panel_el) for exp_panel_el in
            self.export_page.find_elements(*self._locators.EXPORT_PANEL)]

  def export_objects(self):
    """Select 'Export Objects' button to confirm export objects to test's
    temporary directory as CSV file.
    """
    button_export_objs = self.export_page.find_element(
        *self._locators.BUTTON_EXPORT_OBJECTS)
    base.Button(self._driver, button_export_objs).click()
    selenium_utils.wait_for_js_to_load(self._driver)
