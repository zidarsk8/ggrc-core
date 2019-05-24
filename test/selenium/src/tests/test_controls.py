# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Controls tests."""

# pylint: disable=redefined-outer-name
import copy
import pytest

from lib import base, browsers
from lib.constants import element
from lib.service import webui_service


@pytest.fixture()
def controls_service(selenium):
  """Controls service fixture."""
  return webui_service.ControlsService(selenium)


class TestControls(base.Test):
  """Tests for Controls functionality."""
  # pylint: disable=no-self-use
  # pylint: disable=invalid-name
  # pylint: disable=unused-argument

  def test_user_cannot_add_person_to_custom_role(self, control,
                                                 controls_service):
    """Tests that user cannot add a person to custom Role."""
    expected_conditions = {"add_person_text_field_exists": False,
                           "same_url_for_new_tab": True}
    actual_conditions = copy.deepcopy(expected_conditions)

    widget = controls_service.open_info_page_of_obj(control)
    widget.control_owners.inline_edit.open()
    actual_conditions["add_person_text_field_exists"] = (
        widget.control_owners.add_person_text_field.exists)
    old_tab, new_tab = browsers.get_browser().windows()
    actual_conditions["same_url_for_new_tab"] = (old_tab.url == new_tab.url)
    assert expected_conditions == actual_conditions

  def test_user_cannot_update_custom_attribute(
      self, gcads_for_control, control, controls_service
  ):
    """Tests that user cannot update custom attribute."""
    expected_conditions = {"same_url_for_new_tab": True,
                           "controls_ca_editable": False}
    actual_conditions = copy.deepcopy(expected_conditions)

    actual_conditions["controls_ca_editable"] = (
        controls_service.has_gca_inline_edit(
            control, ca_type=element.AdminWidgetCustomAttributes.RICH_TEXT))
    old_tab, new_tab = browsers.get_browser().windows()
    actual_conditions["same_url_for_new_tab"] = (old_tab.url == new_tab.url)
    assert expected_conditions == actual_conditions

  def test_user_cannot_update_predefined_field(self, control, selenium):
    """Tests that user cannot update predefined field."""
    expected_conditions = {"predefined_field_updatable": False,
                           "same_url_for_new_tab": True}
    actual_conditions = copy.deepcopy(expected_conditions)

    info_widget = webui_service.ControlsService(
        selenium).open_info_page_of_obj(control)
    info_widget.assertions.open_inline_edit()
    actual_conditions[
        "predefined_field_updatable"] = info_widget.assertions.input.exists
    old_tab, new_tab = browsers.get_browser().windows()
    actual_conditions["same_url_for_new_tab"] = (old_tab.url == new_tab.url)
    assert expected_conditions == actual_conditions
