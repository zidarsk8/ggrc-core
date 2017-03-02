# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Modals for clone objects."""

from lib import base, decorator
from lib.constants import locator


class CloneAuditModal(base.Modal):
  """Modal for clone Audits."""
  _locator = locator.ModalCloneAudit

  def __init__(self, driver):
    super(CloneAuditModal, self).__init__(driver)
    self.title_modal = base.Label(driver, self._locator.MODAL_TITLE)
    self.checkbox_clone_asmt_tmpls = base.Checkbox(
        driver, self._locator.CHECKBOX_CLONE_ASMT_TMPLS)
    self.button_clone = base.Button(driver, self._locator.BUTTON_CONFIRM)

  def confirm_clone_audit(self):
    """Confirm clone Audit."""
    self.button_clone.click()

  @decorator.wait_for_redirect
  def confirm_full_clone_audit(self):
    """Confirm clone Audit including Assessment Templates and
    wait of page redirected."""
    self.checkbox_clone_asmt_tmpls.click()
    self.button_clone.click()
