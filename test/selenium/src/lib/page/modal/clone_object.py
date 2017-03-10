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

  @decorator.wait_for_redirect
  def confirm_clone(self, is_full=False):
    """Confirm clone Audit not including Assessment Templates
    if 'is_full'=False and including if 'is_full'=True.
    """
    if is_full is True:
      self.checkbox_clone_asmt_tmpls.click()
    self.button_clone.click()
