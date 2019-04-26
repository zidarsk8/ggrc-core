# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Unified mapper tests."""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

import pytest

from lib import base, browsers
from lib.constants import objects
from lib.entities.entity import Representation
from lib.page.widget import object_modal
from lib.service import webui_service
from lib.ui import ui_facade


class TestProgramPage(base.Test):
  """Tests of unified mapper."""

  @pytest.mark.smoke_tests
  def test_destructive_mapping_controls_to_program_via_unified_mapper(
      self, program, controls, selenium
  ):
    """Check if Controls can be mapped to Program from Controls widget under
    Program page via unified mapper.
    Preconditions:
    - Program, Controls created via REST API.
    """
    expected_controls = [
        expected_control.repr_ui() for expected_control
        in controls]
    controls_ui_service = webui_service.ControlsService(selenium)
    controls_ui_service.map_objs_via_tree_view(
        src_obj=program, dest_objs=expected_controls)
    actual_controls_tab_count = controls_ui_service.get_count_objs_from_tab(
        src_obj=program)
    assert len(expected_controls) == actual_controls_tab_count
    actual_controls = controls_ui_service.get_list_objs_from_tree_view(
        src_obj=program)
    # 'actual_controls': created_at, updated_at, custom_attributes (None)
    self.general_equal_assert(
        sorted(expected_controls), sorted(actual_controls),
        *Representation.tree_view_attrs_to_exclude)

  def test_no_modal_for_program_control(self, login_as_creator, program,
                                        selenium):
    """Tests that 'New Control' modal is not opened
    when creator adds control to a program."""
    programs_service = webui_service.ProgramsService(selenium)
    programs_service.open_info_page_of_obj(program)
    obj_modal = programs_service.add_and_map_obj_widget(objects.CONTROLS)
    assert not obj_modal.is_present, ("'New Control' modal "
                                      "should not be present.")

  def test_user_cannot_map_control_to_scope_ojbects_via_add_tab(self, control,
                                                                selenium):
    """Tests that user cannot map control to scope objects/directives
    via 'Add Tab' menu."""
    service = webui_service.ControlsService(selenium)
    controls_info_widget = service.open_info_page_of_obj(control)
    controls_info_widget.click_add_tab_btn()
    hidden_items = controls_info_widget.get_hidden_items_from_add_tab()
    for h_item in hidden_items:
      controls_info_widget.click_add_tab_btn()
      h_item.click()
      ui_facade.verify_modal_not_present(
          object_modal.UnifiedMapperModal())
      old_tab, new_tab = browsers.get_browser().windows()
      assert old_tab.url == new_tab.url, "Urls for tabs should be the same."
      old_tab.use()
      new_tab.close()
