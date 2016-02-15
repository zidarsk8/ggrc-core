# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib.constants import url
from lib.constants import locator
from lib import environment
from lib.page import widget_bar
from lib.page import lhn


class _UserList(base.Component):
  _locator = locator.PageHeader

  def __init__(self, driver):
    super(_UserList, self).__init__(driver)
    self.button_my_work = base.Button(self._driver,
                                      self._locator.BUTTON_MY_WORK)
    self.button_admin_dashboard = base.Button(
      self._driver, self._locator.BUTTON_ADMIN_DASHBOARD)
    self.button_data_import = base.Button(
      self._driver, self._locator.BUTTON_DATA_IMPORT)
    self.button_data_export = base.Button(
      self._driver, self._locator.BUTTON_DATA_EXPORT)
    self.button_logout = base.Button(self._driver,
                                     self._locator.BUTTON_LOGOUT)

  def open_my_work(self):
    """
    Returns:
        widget.DataAssetInfo
    """
    raise NotImplementedError

  def open_admin_dashboard(self):
    """
    Returns:
        admin_dashboard.AdminDashboardPage
    """
    self.button_my_work.click()
    return AdminDashboardPage(self._driver)

  def import_data(self):
    raise NotImplementedError

  def export_data(self):
    raise NotImplementedError

  def logout(self):
    raise NotImplementedError


class HeaderPage(base.Page):
  """Header of the page"""

  _locator = locator.PageHeader

  def __init__(self, driver):
    super(HeaderPage, self).__init__(driver)
    self.button_lhn_menu = base.Button(self._driver,
                                       self._locator.BUTTON_LHN)
    self.button_dashboard = base.Button(self._driver,
                                        self._locator.BUTTON_DASHBOARD)
    self.button_search = base.Button(self._driver,
                                     self._locator.BUTTON_SEARCH)
    self.button_my_tasks = base.Button(self._driver,
                                       self._locator.BUTTON_MY_TASKS)
    self.button_all_objects = base.Button(
      self._driver, self._locator.BUTTON_ALL_OBJECTS)
    self.button_user_dropdown = base.Button(
      self._driver, self._locator.BUTTON_USER_DROPDOWN)

  def open_lhn_menu(self):
    """Opens LHN on the Dashboard

    Returns:
        LhnMenu
    """
    self.button_lhn_menu.click()
    return lhn.Menu(self._driver)

  def click_on_logo(self):
    """
    Returns:
        widget.DataAssetInfo
    """
    raise NotImplementedError

  def open_user_list(self):
    """
    Returns:
        _UserList
    """
    self.button_user_dropdown.click()
    return _UserList(self._driver)


class DashboardPage(widget_bar.DashboardWidgetBarPage, HeaderPage):
  """The main dashboard page"""

  URL = environment.APP_URL + url.DASHBOARD

  def __init__(self, driver):
    super(DashboardPage, self).__init__(driver)
    self.button_help = base.Button(self._driver, self._locator.BUTTON_HELP)


class AdminDashboardPage(widget_bar.AdminDashboardWidgetBarPage,
                         HeaderPage):
  """Admin dashboard page model"""

  URL = environment.APP_URL + url.ADMIN_DASHBOARD

  def __init__(self, driver):
    super(AdminDashboardPage, self).__init__(driver)
