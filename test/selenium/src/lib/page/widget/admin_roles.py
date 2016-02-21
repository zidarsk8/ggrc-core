# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib import environment
from lib.constants import url
from lib.constants import locator


class AdminRoles(base.Widget):
  """Model for the widget admin rols on admin dashboard"""

  _locator = locator.AdminRolesWidget
  URL = environment.APP_URL \
      + url.ADMIN_DASHBOARD \
      + url.Widget.ROLES

  def __init__(self, driver):
    super(AdminRoles, self).__init__(driver)
    self.role_editor = base.Label(driver, self._locator.ROLE_EDITOR)
    self.role_grc_admin = base.Label(driver, self._locator.ROLE_GRC_ADMIN)
    self.role_program_editor = base.Label(
        driver, self._locator.ROLE_PROGRAM_EDITOR)
    self.role_program_owner = base.Label(
        driver, self._locator.ROLE_PROGRAM_OWNER)
    self.role_program_reader = base.Label(
        driver, self._locator.ROLE_PROGRAM_READER)
    self.role_reader = base.Label(driver, self._locator.ROLE_READER)
    self.role_workflow_member = base.Label(
        driver, self._locator.ROLE_WORKFLOW_MEMBER)
    self.role_workflow_owner = base.Label(
        driver, self._locator.ROLE_WORKFLOW_OWNER)

    self.scope_editor = base.Label(driver, self._locator.SCOPE_EDITOR)
    self.scope_grc_admin = base.Label(driver, self._locator.SCOPE_GRC_ADMIN)
    self.scope_program_editor = base.Label(
        driver, self._locator.SCOPE_PROGRAM_EDITOR)
    self.scope_program_owner = base.Label(
        driver, self._locator.SCOPE_PROGRAM_OWNER)
    self.scope_program_reader = base.Label(
        driver, self._locator.SCOPE_PROGRAM_READER)
    self.scope_reader = base.Label(driver, self._locator.SCOPE_READER)
    self.scope_workflow_member = base.Label(
        driver, self._locator.SCOPE_WORKFLOW_MEMBER)
    self.scope_workflow_owner = base.Label(
        driver, self._locator.SCOPE_WORKFLOW_OWNER)
