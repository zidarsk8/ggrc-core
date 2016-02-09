# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib.page import widget
from lib.element import widget_bar
from lib.constants import locator


class _AdminWidget(base.Widget):
  def __init__(self, driver):
    super(_AdminWidget, self).__init__(driver)


class _WidgetBar(base.Component):
  def __init__(self, driver):
    super(_WidgetBar, self).__init__(driver)

  def get_active_widget_name(self):
    """In general multiple tabs are open. Here we get the name of the
    active one.

    Returns:
         str
    """
    active_widget = base.Button(self._driver, locator.WidgetBar.TAB_WIDGET)
    return active_widget.text


class AdminDashboardWidgetBarPage(_WidgetBar):
  def __init__(self, driver):
    super(AdminDashboardWidgetBarPage, self).__init__(driver)
    self.tab_people = widget_bar.Tab(self._driver,
                                     locator.WidgetBar.ADMIN_PEOPLE)
    self.tab_roles = widget_bar.Tab(self._driver,
                                    locator.WidgetBar.ADMIN_ROLES)
    self.tab_events = widget_bar.Tab(self._driver,
                                     locator.WidgetBar.ADMIN_EVENTS)
    self.tab_custom_attributes = widget_bar.Tab(
        self._driver, locator.WidgetBar.ADMIN_CUSTOM_ATTRIBUTE)

  def select_people(self):
    """
    Returns:
        widget.AdminPeople
    """
    self.tab_people.click()
    return widget.AdminPeople(self._driver)

  def select_roles(self):
    """
    Returns:
        widget.AdminRoles
    """
    self.tab_roles.click()
    return widget.AdminRoles(self._driver)

  def select_events(self):
    """
    Returns:
        widget.AdminPeople
    """
    self.tab_events.click()
    return widget.AdminEvents(self._driver)

  def select_custom_attributes(self):
    """
    Returns:
        widget.AdminCustomAttributes
    """
    self.tab_custom_attributes.click()
    return widget.AdminCustomAttributes(self._driver)


class DashboardWidgetBarPage(_WidgetBar):
  def __init__(self, driver):
    super(DashboardWidgetBarPage, self).__init__(driver)
    self.button_add_widget = base.Dropdown(driver,
                                           locator.WidgetBar.BUTTON_ADD)
    self.tab_info = base.Tab(self._driver, locator.WidgetBar.INFO)

  def add_widget(self):
    """
    Returns:
        widget.AddWidget
    """
    self.button_add_widget.click()
    return widget.AddWidget(self._driver)

  def select_info(self):
    """
    Returns:
        widget.InfoWidget
    """
    self.tab_info.click()
    return widget.DashboardInfo(self._driver)
