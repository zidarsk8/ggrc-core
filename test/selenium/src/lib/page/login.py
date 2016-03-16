# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib.constants import locator
from lib.page import dashboard
from lib import environment, base


class LoginPage(base.Page):
  URL = environment.APP_URL

  def __init__(self, driver):
    super(LoginPage, self).__init__(driver)
    self.button_login = base.Button(driver, locator.Login.BUTTON_LOGIN)

  def login(self):
    """Clicks on the login button on the login page

    Returns:
         dashboard.Dashboard
    """
    self.button_login.click()
    return dashboard.Dashboard(self._driver)

  def login_as(self, user_name, user_email):
    """Clicks on the login button on the login page and logs in as a
    certain user.
    """
    raise NotImplementedError
