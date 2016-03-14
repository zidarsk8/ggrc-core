# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com
"""A module for widget bar elements"""

import re

from lib import base
from lib import factory
from lib.utils import selenium_utils
from lib.constants import regex
from lib.constants import element


class Tab(base.Tab):
  def __init__(self, driver, element_locator):
    """
    Args:
        driver (base.CustomDriver
    """
    super(Tab, self).__init__(driver, element_locator)
    self.member_count = None
    self._set_member_count()

  def _set_member_count(self):
    widget_title = selenium_utils.get_when_visible(
        self._driver, self._locator).text

    if "(" not in widget_title:
      self.member_count = int(widget_title)
    else:
      self.member_count = int(
          re.match(regex.WIDGET_TITLE_AND_COUNT, widget_title)
          .group(2))


class AddWidget(base.Component):
  """Model for the add widget button in widget bar
  No elements are initiated here because based on the context they may be
  missing"""

  def _select(self, widget_name):
    """Selects a widget from the dropdown and returns the appropriate
    initialized widget class"""
    self._driver.find_element(*factory.get_locator_add_widget(widget_name))\
        .click()
    return factory.get_cls_widget(widget_name)(self._driver)

  def select_controls(self):
    """
    Returns:
        lib.page.widget.generic_widget.Controls
    """
    return self._select(element.WidgetBar.CONTROLS)

  def select_issues(self):
    """
    Returns:
        lib.page.widget.generic_widget.Issues
    """
    return self._select(element.WidgetBar.ISSUES)

  def select_processes(self):
    """
    Returns:
        lib.page.widget.generic_widget.Processes
    """
    return self._select(element.WidgetBar.PROCESSES)

  def select_data_assets(self):
    """
    Returns:
        lib.page.widget.generic_widget.DataAssets
    """
    return self._select(element.WidgetBar.DATA_ASSETS)

  def select_systems(self):
    """
    Returns:
        lib.page.widget.generic_widget.Systems
    """
    return self._select(element.WidgetBar.SYSTEMS)

  def select_products(self):
    """
    Returns:
        lib.page.widget.generic_widget.Products
    """
    return self._select(element.WidgetBar.PRODUCTS)

  def select_projects(self):
    """
    Returns:
        lib.page.widget.generic_widget.Projects
    """
    return self._select(element.WidgetBar.PROJECTS)

  def select_programs(self):
    """
    Returns:
        lib.page.widget.generic_widget.Programs
    """
    return self._select(element.WidgetBar.PROGRAMS)
