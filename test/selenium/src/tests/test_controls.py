# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Controls tests."""

from lib import base, browsers
from lib.service import webui_service


class TestControls(base.Test):
  """Tests for Controls functionality."""
  # pylint: disable=no-self-use
  # pylint: disable=invalid-name

  def test_user_cannot_add_person_to_custom_role(self, control, selenium):
    """Tests that user cannot add a person to custom Role."""
    service = webui_service.ControlsService(selenium)
    widget = service.open_info_page_of_obj(control)
    widget.control_owners.inline_edit.open()
    assert not widget.control_owners.add_person_text_field.exists, (
        "User should not be able to add person to custom Role.")
    old_tab, new_tab = browsers.get_browser().windows()
    assert old_tab.url == new_tab.url, ("Urls should be the same. "
                                        "New url for redirect to GGRCQ.")
