# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Models for widgets other than the info widget"""

import re

from selenium.common import exceptions

from lib import base
from lib.page.widget import info_widget
from lib.constants import locator
from lib.constants import regex
from lib.utils import selenium_utils


class Widget(base.Widget):
  """Class representing all widgets with filters that list objects"""
  _info_pane_cls = None
  _locator_widget = None
  _locator_filter = None

  def __init__(self, driver):
    # wait for the elements to load
    self.member_count = None
    self.label_filter = base.Label(driver, self._locator_filter.TITLE)
    self.button_filter_question = base.Button(
        driver, self._locator_filter.BUTTON_HELP)
    self.filter = base.Filter(
        driver,
        self._locator_filter.TEXTFIELD,
        self._locator_filter.BUTTON_SUBMIT,
        self._locator_filter.BUTTON_RESET)

    super(Widget, self).__init__(driver)
    self._set_members_listed()

  def _set_member_count(self):
    """Parses the widget name and number of items from the widget tab title"""
    widget_label = selenium_utils.get_when_visible(
        self._driver, self._locator_widget).text

    # The widget label has 2 forms: "widget_name_plural (number_of_items)"
    # and "number_of_items" and they change depending on how many widgets
    # are open. In order to handle both forms, we first try to parse the
    # first form and only then the second one.
    parsed_label = re.match(
        regex.WIDGET_TITLE_AND_COUNT, widget_label)

    item_count = widget_label \
        if parsed_label is None \
        else parsed_label.group(2)
    self.member_count = int(item_count)

  def _set_members_listed(self):
    """Waits for the listed members to be loaded and adds them to a local
    container"""
    self._set_member_count()

    if self.member_count:
      # wait until the elements are loaded
      selenium_utils.get_when_clickable(
          self._driver, locator.ObjectWidget.MEMBERS_TITLE_LIST)

      self.members_listed = self._driver.find_elements(
          *locator.ObjectWidget.MEMBERS_TITLE_LIST)
    else:
      self.members_listed = []

  def select_nth_member(self, member):
    """Selects member from the list. Members start from (including) 0.

    Args:
        member (int)

    Returns:
        lib.page.widget.info.Widget
    """
    try:
      element = self.members_listed[member]

      # wait for the listed items animation to stop
      selenium_utils.wait_until_stops_moving(element)
      element.click()

      # wait for the info pane animation to stop
      info_pane = selenium_utils.get_when_clickable(
          self._driver, locator.ObjectWidget.INFO_PANE)
      selenium_utils.wait_until_stops_moving(info_pane)

      return self._info_pane_cls(self._driver)
    except exceptions.StaleElementReferenceException:
      self.members_listed = self._driver.find_elements(
          *locator.ObjectWidget.MEMBERS_TITLE_LIST)
      return self.select_nth_member(member)
    except exceptions.TimeoutException:
      # sometimes the click to the listed member results in hover
      return self.select_nth_member(member)


class Controls(Widget):
  """Model for the control widget"""
  _info_pane_cls = info_widget.Controls
  _locator_widget = locator.WidgetBar.CONTROLS
  _locator_filter = locator.WidgetControls

  def __init__(self, driver,):
    super(Controls, self).__init__(driver)
    self.label_title = base.Label(
        driver,
        locator.ObjectWidget.CONTROL_COLUMN_TITLE)
    self.label_owner = base.Label(driver, locator.ObjectWidget.CONTROL_OWNER)
    self.label_state = base.Label(driver, locator.ObjectWidget.COTNROL_STATE)


class Issues(Widget):
  """Model for the issue widget"""
  _info_pane_cls = info_widget.Issues
  _locator_widget = locator.WidgetBar.ISSUES
  _locator_filter = locator.WidgetIssues


class Processes(Widget):
  """Model for the process widget"""
  _info_pane_cls = info_widget.Processes
  _locator_widget = locator.WidgetBar.PROCESSES
  _locator_filter = locator.WidgetProcesses


class DataAssets(Widget):
  """Model for the data asset widget"""
  _info_pane_cls = info_widget.DataAssets
  _locator_widget = locator.WidgetBar.DATA_ASSETS
  _locator_filter = locator.WidgetDataAssets


class Systems(Widget):
  """Model for the system widget"""
  _info_pane_cls = info_widget.Systems
  _locator_widget = locator.WidgetBar.SYSTEMS
  _locator_filter = locator.WidgetSystems


class Products(Widget):
  """Model for the product widget"""
  _info_pane_cls = info_widget.Products
  _locator_widget = locator.WidgetBar.PRODUCTS
  _locator_filter = locator.WidgetProducts


class Projects(Widget):
  """Model for the project widget"""
  _info_pane_cls = info_widget.Projects
  _locator_widget = locator.WidgetBar.PROJECTS
  _locator_filter = locator.WidgetProjects
