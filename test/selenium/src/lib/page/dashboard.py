# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib.constants import url
from lib.constants import locator
from lib import environment
from lib import decorator
from lib.page import widget_bar
from lib.page import lhn


class UserList(base.Component):
  locator_cls = locator.PageHeader

  def __init__(self, driver):
    super(UserList, self).__init__(driver)
    self.button_my_work = base.Button(self._driver,
                                      self.locator_cls.BUTTON_MY_WORK)
    self.button_admin_dashboard = base.Button(
        self._driver, self.locator_cls.BUTTON_ADMIN_DASHBOARD)
    self.button_data_import = base.Button(
        self._driver, self.locator_cls.BUTTON_DATA_IMPORT)
    self.button_data_export = base.Button(
        self._driver, self.locator_cls.BUTTON_DATA_EXPORT)
    self.button_logout = base.Button(
        self._driver, self.locator_cls.BUTTON_LOGOUT)
    self.notifications = base.Label(
        self._driver, self.locator_cls.NOTIFICATIONS)
    self.checkbox_daily_digest = base.Checkbox(
        self._driver, self.locator_cls.CHECKBOX_DAILY_DIGEST)

  def select_my_work(self):
    """
    Returns:
        widget.DataAssetsInfo
    """
    self.button_my_work.click()
    return DashboardPage(self._driver)

  def select_admin_dashboard(self):
    """
    Returns:
        admin_dashboard.AdminDashboardPage
    """
    self.button_my_work.click()
    return AdminDashboardPage(self._driver)

  def select_import_data(self):
    raise NotImplementedError

  def select_export_data(self):
    raise NotImplementedError

  @decorator.wait_for_redirect
  def select_logout(self):
    raise NotImplementedError

  def check_daily_email_digest(self):
    """Checks the daily checkbox"""
    self.checkbox_daily_digest.check()

  def uncheck_daily_email_digest(self):
    """Unchecks the daily checkbox"""
    self.checkbox_daily_digest.uncheck()


class HeaderPage(base.Page):
  """Header of the page"""

  locator = locator.PageHeader

  def __init__(self, driver):
    super(HeaderPage, self).__init__(driver)
    self.toggle_lhn_menu = base.Toggle(self._driver,
                                       self.locator.TOGGLE_LHN)
    self.button_dashboard = base.Button(self._driver,
                                        self.locator.BUTTON_DASHBOARD)
    self.button_search = base.Button(self._driver,
                                     self.locator.BUTTON_SEARCH)
    self.button_my_tasks = base.Button(self._driver,
                                       self.locator.BUTTON_MY_TASKS)
    self.button_all_objects = base.Button(
        self._driver, self.locator.BUTTON_ALL_OBJECTS)
    self.toggle_user_dropdown = base.Toggle(
        self._driver, self.locator.TOGGLE_USER_DROPDOWN)

  def open_lhn_menu(self):
    """Opens LHN on the Dashboard

    Returns:
        LhnMenu
    """
    self.toggle_lhn_menu.toggle()
    return lhn.Menu(self._driver)

  def close_lhn_menu(self):
    """Closes LHN on the Dashboard

    Returns:
        LhnMenu
    """
    self.toggle_lhn_menu.toggle(on=False)
    return DashboardPage(self._driver)

  def click_on_logo(self):
    """
    Returns:
        widget.DataAssetsInfo
    """
    raise NotImplementedError

  def open_user_list(self):
    """
    Returns:
        UserList
    """
    self.toggle_user_dropdown.click()
    return UserList(self._driver)


class DashboardPage(widget_bar.DashboardWidgetBarPage, HeaderPage):
  """The main dashboard page"""

  URL = environment.APP_URL + url.DASHBOARD

  def __init__(self, driver):
    super(DashboardPage, self).__init__(driver)
    self.button_help = base.Button(self._driver, self.locator.BUTTON_HELP)


class AdminDashboardPage(widget_bar.AdminDashboardWidgetBarPage,
                         HeaderPage):
  """Admin dashboard page model"""

  URL = environment.APP_URL + url.ADMIN_DASHBOARD

  def __init__(self, driver):
    super(AdminDashboardPage, self).__init__(driver)
