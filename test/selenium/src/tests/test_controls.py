# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Controls tests."""
import copy

from lib import base, browsers
from lib.service import webui_service


class TestControls(base.Test):
  """Tests for Controls functionality."""
  # pylint: disable=no-self-use
  # pylint: disable=invalid-name

  def test_user_cannot_add_person_to_custom_role(self, control, selenium):
    """Tests that user cannot add a person to custom Role."""
    expected_conditions = {"add_person_text_field_exists": False,
                           "same_url_for_new_tab": True}
    actual_conditions = copy.deepcopy(expected_conditions)

    service = webui_service.ControlsService(selenium)
    widget = service.open_info_page_of_obj(control)
    widget.control_owners.inline_edit.open()
    actual_conditions["add_person_text_field_exists"] = (
        widget.control_owners.add_person_text_field.exists)
    old_tab, new_tab = browsers.get_browser().windows()
    actual_conditions["same_url_for_new_tab"] = (old_tab.url == new_tab.url)
    assert expected_conditions == actual_conditions
