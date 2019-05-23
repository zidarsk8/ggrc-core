# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Unified mapper tests."""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
import copy

import pytest

from lib import base, browsers, url
from lib.app_entity_factory import regulation_entity_factory
from lib.constants import objects
from lib.entities.entity import Representation
from lib.page.modal import unified_mapper
from lib.page.widget import controls_tab
from lib.service import webui_service, webui_facade
from lib.ui import ui_facade
from lib.utils import selenium_utils


@pytest.fixture()
def dashboard_controls_tab(selenium):
  """Open My Work Dashboard Controls Tab URL and
  return Controls Tab page objects model."""
  selenium_utils.open_url(url.Urls().dashboard_controls_tab)
  return controls_tab.ControlsTab()


@pytest.fixture()
def regulation(selenium):
  """Creates regulation object."""
  return regulation_entity_factory.RegulationFactory().create()


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
      ui_facade.verify_modal_obj_not_present_in_all_windows(
          unified_mapper.BaseUnifiedMapperModal())
      old_tab, new_tab = browsers.get_browser().windows()
      assert old_tab.url == new_tab.url, "Urls for tabs should be the same."
      old_tab.use()
      new_tab.close()


class TestControlsPage(base.Test):
  """Tests of unified mapper for Controls."""

  def test_user_cannot_map_control_via_unified_mapper(self, control,
                                                      dashboard_controls_tab,
                                                      selenium):
    """Tests that user cannot map Control to Scope Objects/Directives
    via Unified Mapper (existent new scope/directive object)"""
    dashboard_controls_tab.get_control(control).select_map_to_this_object()
    map_modal = webui_facade.map_object_via_unified_mapper(
        selenium=selenium, obj_name=objects.CONTROLS,
        dest_objs_type=objects.get_singular(plural=objects.PRODUCTS,
                                            title=True),
        return_tree_items=False,
        open_in_new_frontend=True)
    browsers.get_browser().windows()[1].use()
    ui_facade.verify_modal_obj_not_present(modal_obj=map_modal)

  def test_cannot_map_control_via_um_create_new_obj(self, control, regulation,
                                                    dashboard_controls_tab,
                                                    selenium):
    """Tests that user cannot map control to scope objects/directives
    via unified mapper (create a new scope/directive object)."""
    expected_conditions = {"regulation_in_top_tabs": False,
                           "new_tab_url": url.Urls().dashboard_info_tab}
    actual_conditions = copy.deepcopy(expected_conditions)

    dashboard_controls_tab.get_control(control).select_map_to_this_object()
    webui_facade.map_object_via_unified_mapper(
        selenium=selenium, obj_name=objects.CONTROLS,
        dest_objs_type=objects.get_singular(plural=objects.REGULATIONS,
                                            title=True),
        obj_to_map=regulation, proceed_in_new_tab=True)
    _, new_tab = browsers.get_browser().windows()
    actual_conditions['new_tab_url'] = new_tab.url
    actual_conditions['regulation_in_top_tabs'] = (
        objects.get_normal_form(
            objects.REGULATIONS) in webui_service.ControlsService(
                selenium).open_info_page_of_obj(control).top_tabs.tab_names)
    assert expected_conditions == actual_conditions
