# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Modals for delete objects."""
from lib import base


class DeleteObjectModal(base.WithBrowser):
  """Modal for delete objects."""
  # pylint: disable=too-few-public-methods

  def delete_modal(self):
    return self._browser.element(
        xpath="//span[contains(.,'Delete')]/../../..").wait_until(
        lambda e: e.present)

  def confirm_delete(self):
    """Confirm delete object."""
    delete_button = self.delete_modal().element(
        class_name="confirm-buttons").link(text="Delete")
    delete_button.click()
    delete_button.wait_until_not_present()
