# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Module of classes inherited from AbstractTabContainer control."""
from lib import base
from lib.constants import element, locator, roles
from lib.element.tables import (AssessmentRelatedAsmtsTable,
                                AssessmentRelatedIssuesTable)
from lib.utils import selenium_utils


class AssessmentTabContainer(base.AbstractTabContainer):
  """Class of TabContainer in Assessment info."""
  _elements = element.AssessmentTabContainer

  def _get_locators(self):
    return locator.WidgetInfoAssessment.TabContainer

  def _tabs(self):
    """Dict of Tab objects. AssessmentLog tab item contains dict of
    validation result, because there is no reason for create AssessmentLog
    page object class.
    """
    selenium_utils.scroll_into_view(self._driver, self.container_element)
    return {
        self._elements.RELATED_ASMTS_TAB: AssessmentRelatedAsmtsTable,
        self._elements.RELATED_ISSUES_TAB: AssessmentRelatedIssuesTable,
        self._elements.CHANGE_LOG_TAB: self._log_tab_validate}

  def switch_to_tab(self, tab_name):
    """Method for switch active tab to another one according to tab's name."""
    if self._tab_controller.active_tab.text != tab_name:
      self._tab_controller.active_tab = tab_name

  @staticmethod
  def _log_tab_validate(_driver, log_panel_element):
    """Validation of all log items on Log pane.
    Return: list of dicts.
    """
    tab_elements = element.AsmtLogTab
    tab_locators = locator.AssessmentLogTab
    selenium_utils.wait_for_js_to_load(_driver)

    def check_log_item(log_element):
      """Check consistency of log item by passed log element.
      Return: dict of bool.
      """
      all_cells_texts = [elem.text for elem in
                         log_element.find_elements(*tab_locators.CELLS_CSS)]
      expected_headers = [tab_elements.FIELD, tab_elements.ORIGINAL_VALUE,
                          tab_elements.NEW_VALUE]
      headers_is_valid = (
          [all_cells_texts.pop(0)
           for _ in xrange(len(expected_headers))] == expected_headers)

      field_is_valid = all(
          cell != "" and cell != tab_elements.EMPTY_STATEMENT
          for cell in all_cells_texts[0::3])
      orignal_value_is_valid = all(
          cell == tab_elements.EMPTY_STATEMENT
          for cell in all_cells_texts[1::3])
      new_value_is_valid = all(
          cell != "" and cell != tab_elements.EMPTY_STATEMENT
          for cell in all_cells_texts[2::3])

      person_element = log_element.find_element(
          *tab_locators.COMMENT_PERSON_CSS)

      return {"headers_is_valid": headers_is_valid,
              "field_is_valid": field_is_valid,
              "orignal_value_is_valid": orignal_value_is_valid,
              "new_value_is_valid": new_value_is_valid,
              "person_is_valid": (
                  person_element.text == roles.DEFAULT_USER_EMAIL)
              }
    selenium_utils.wait_until_not_present(
        _driver, tab_locators.LOG_TAB_SPINNER_CSS)
    log_list = selenium_utils.get_when_all_visible(
        log_panel_element, tab_locators.LOG_LIST_CSS)
    return [check_log_item(el) for el in log_list]
