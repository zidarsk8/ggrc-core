# Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Snapshot smoke tests."""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments

import pytest

from lib import base
from lib.constants import messages
from lib.constants.element import Lhn, MappingStatusAttrs
from lib.page import dashboard
from lib.service import webui_service
from lib.utils.filter_utils import FilterUtils
from lib.utils import selenium_utils


class TestSnapshots(base.Test):
  """Tests for snapshot functionality."""

  @pytest.fixture(scope="function")
  def create_audit_and_update_first_of_two_original_controls(
      self, create_audit_with_control_and_update_control,
      new_control_rest, map_new_program_rest_to_new_control_rest
  ):
    """Create Audit with snapshotable Control and update original Control under
    Program via REST API. After that create second Control and map it to
    Program via REST API.
    Preconditions:
    - Execution and return of fixture
      'create_audit_with_control_and_update_control'.
    - Second Control created via REST API.
    - Second Control mapped to Program via REST API.
    """
    audit_with_one_control = create_audit_with_control_and_update_control
    return {
        "audit": audit_with_one_control["new_audit_rest"][0],
        "program": audit_with_one_control["new_program_rest"][0],
        "control": audit_with_one_control["new_control_rest"][0],
        "updated_control": audit_with_one_control["update_control_rest"][0],
        "second_control": new_control_rest
    }

  @pytest.mark.smoke_tests
  def test_audit_contains_readonly_ver_of_control(
      self, create_audit_with_control, selenium
  ):
    """Check via UI that Audit contains read-only snapshotable Control.
    Preconditions:
    - Program, Control created via REST API.
    - Control mapped to Program via REST API.
    - Audit created under Program via REST API.
    """
    audit_with_one_control = create_audit_with_control
    audit = audit_with_one_control["new_audit_rest"][0]
    control = audit_with_one_control["new_control_rest"][0]
    actual_controls_tab_count = (webui_service.ControlsService(selenium).
                                 get_count_objs_from_tab(src_obj=audit))
    assert len([control]) == actual_controls_tab_count
    is_control_editable = (
        webui_service.ControlsService(selenium).is_obj_editable_via_info_panel(
            src_obj=audit, obj=control))
    assert is_control_editable is False

  @pytest.mark.smoke_tests
  @pytest.mark.parametrize(
      ("create_audit_with_control_and_manipulate_on_control",
       "is_update_to_latest_ver", "is_updateable", "is_openable"),
      [("create_audit_with_control_and_update_control", False, True, True),
       ("create_audit_with_control_and_update_control", True, False, True),
       ("create_audit_with_control_and_delete_control", False, True, False),
       ("create_audit_with_control_and_delete_control", True, False, False)],
      ids=["Audit contains snapshotable Control after updating Control",
           "Update snapshotable control after updating Control",
           "Audit contains snapshotable Control after deleting Control",
           "Update snapshotable control after deleting Control"])
  def test_snapshotable_control_without_cas(
      self, create_audit_with_control_and_manipulate_on_control, action,
      is_update_to_latest_ver, is_updateable, is_openable, selenium
  ):
    """Test snapshotable Control and check via UI that:
    - Audit contains snapshotable Control after updating Control.
    - Update snapshotable control after updating original Control.
    - Audit contains snapshotable Control after deleting Control.
    - Update snapshotable control after deleting Control.
    Preconditions:
      Execution and return of dynamic fixtures used REST API:
    - 'create_audit_with_control_and_update_control'.
    - 'create_audit_with_control_and_delete_control'.
    """
    # preconditions = generate_snapshots_fixtures(
    #     "create_audit_with_control_and_update_control")
    #     "create_audit_with_control_and_" + action)
    audit_with_one_control = (
        create_audit_with_control_and_manipulate_on_control)
    audit = audit_with_one_control["new_audit_rest"][0]
    expected_control = audit_with_one_control["new_control_rest"][0]
    if is_update_to_latest_ver:
      (webui_service.ControlsService(selenium).
       update_obj_ver_via_info_panel(src_obj=audit, obj=expected_control))
      if action == "update_control":
        expected_control = audit_with_one_control["update_control_rest"][0]
    actual_controls_tab_count = (webui_service.ControlsService(selenium).
                                 get_count_objs_from_tab(src_obj=audit))
    assert len([expected_control]) == actual_controls_tab_count
    is_control_updateable = (webui_service.ControlsService(selenium).
                             is_obj_updateble_via_info_panel(
        src_obj=audit, obj=expected_control))
    is_control_openable = (webui_service.ControlsService(selenium).
                           is_obj_page_exist_via_info_panel(
        src_obj=audit, obj=expected_control))
    assert is_control_updateable is is_updateable
    assert is_control_openable is is_openable
    actual_controls = (webui_service.ControlsService(selenium).
                       get_list_objs_from_tree_view(src_obj=audit))
    assert [expected_control] == actual_controls, (
        messages.ERR_MSG_FORMAT.format([expected_control], actual_controls))

  @pytest.mark.smoke_tests
  def test_update_snapshotable_ver_after_updating_original_control(
      self, create_audit_with_control_and_update_control, selenium
  ):
    """Check via UI that Audit contains snapshotable Control that up-to-date
    with it actual state of original control after updating snapshot to latest
    version.
    Preconditions:
    - Execution and return of fixture
      'create_audit_and_update_original_control'.
    """
    audit_with_one_control = create_audit_with_control_and_update_control
    audit = audit_with_one_control["new_audit_rest"][0]
    control = audit_with_one_control["new_control_rest"][0]
    expected_control = audit_with_one_control["update_control_rest"][0]
    (webui_service.ControlsService(selenium).
     update_obj_ver_via_info_panel(src_obj=audit, obj=control))
    actual_controls_tab_count = (webui_service.ControlsService(selenium).
                                 get_count_objs_from_tab(src_obj=audit))
    assert len([expected_control]) == actual_controls_tab_count
    actual_controls = (webui_service.ControlsService(selenium).
                       get_list_objs_from_tree_view(src_obj=audit))
    assert [expected_control] == actual_controls, (
        messages.ERR_MSG_FORMAT.format([expected_control], actual_controls))

  @pytest.mark.smoke_tests
  def test_audit_contains_snapshotable_control_after_deleting_control(
      self, create_audit_with_control_and_delete_control, selenium
  ):
    """Check via UI that Audit contains snapshotable Control after
    deleting original Control but without updating to latest version.
    Check of snapshotable Control has link to update version to latest state
    and link to view original Control is disabled.
    Preconditions:
    - Execution and return of fixture
      'create_audit_and_delete_original_control'.
    """
    audit_with_one_control = create_audit_with_control_and_delete_control
    audit = audit_with_one_control["new_audit_rest"][0]
    expected_control = audit_with_one_control["new_control_rest"][0]
    actual_controls_tab_count = (webui_service.ControlsService(selenium).
                                 get_count_objs_from_tab(src_obj=audit))
    assert len([expected_control]) == actual_controls_tab_count
    actual_controls = (webui_service.ControlsService(selenium).
                       get_list_objs_from_tree_view(src_obj=audit))
    assert [expected_control] == actual_controls, (
        messages.ERR_MSG_FORMAT.format([expected_control], actual_controls))
    is_control_updateable = (webui_service.ControlsService(selenium).
                             is_obj_updateble_via_info_panel(
        src_obj=audit, obj=expected_control))
    is_control_openable = (webui_service.ControlsService(selenium).
                           is_obj_page_exist_via_info_panel(
        src_obj=audit, obj=expected_control))
    assert is_control_updateable is True
    assert is_control_openable is False

  @pytest.mark.smoke_tests
  def test_update_snapshotable_ver_after_deleting_original_control(
      self, create_audit_with_control_and_delete_control, selenium
  ):
    """Check via UI that Audit contains snapshotable Control after
    deleting original Control and updating to latest version.
    Check of snapshotable Control does not has link to update version to latest
    state and link to view original Control is disabled.
    Preconditions:
    - Execution and return of fixture
      'create_audit_and_delete_original_control'.
    """
    audit_with_one_control = create_audit_with_control_and_delete_control
    audit = audit_with_one_control["new_audit_rest"][0]
    expected_control = audit_with_one_control["new_control_rest"][0]
    (webui_service.ControlsService(selenium).
     update_obj_ver_via_info_panel(src_obj=audit, obj=expected_control))
    actual_controls_tab_count = (webui_service.ControlsService(selenium).
                                 get_count_objs_from_tab(src_obj=audit))
    assert len([expected_control]) == actual_controls_tab_count
    actual_controls = (webui_service.ControlsService(selenium).
                       get_list_objs_from_tree_view(src_obj=audit))
    assert [expected_control] == actual_controls, (
        messages.ERR_MSG_FORMAT.format([expected_control], actual_controls))
    is_control_updateable = (webui_service.ControlsService(selenium).
                             is_obj_updateble_via_info_panel(
        src_obj=audit, obj=expected_control))
    is_control_openable = (webui_service.ControlsService(selenium).
                           is_obj_page_exist_via_info_panel(
        src_obj=audit, obj=expected_control))
    assert is_control_updateable is False
    assert is_control_openable is False

  @pytest.mark.smoke_tests
  def test_mapped_to_program_controls_does_not_added_to_existing_audit(
      self, create_audit_and_update_first_of_two_original_controls, selenium
  ):
    """Check via UI that Audit contains snapshotable Control that equal to
    original Control does not contain Control that was mapped to
    Program after Audit creation.
    Preconditions:
    - Execution and return of fixture
      'create_audit_and_update_first_of_two_original_controls'.
    """
    audit_with_two_controls = (
        create_audit_and_update_first_of_two_original_controls)
    audit = audit_with_two_controls["audit"]
    expected_control = audit_with_two_controls["control"]
    actual_controls_tab_count = (webui_service.ControlsService(selenium).
                                 get_count_objs_from_tab(src_obj=audit))
    assert len([expected_control]) == actual_controls_tab_count
    actual_controls = (webui_service.ControlsService(selenium).
                       get_list_objs_from_tree_view(src_obj=audit))
    assert [expected_control] == actual_controls, (
        messages.ERR_MSG_FORMAT.format([expected_control], actual_controls))

  @pytest.mark.smoke_tests
  def test_bulk_update_audit_objects_to_latest_ver(
      self, create_audit_and_update_first_of_two_original_controls, selenium
  ):
    """Check via UI that Audit contains snapshotable Controls that up-to-date
    with their actual states after bulk updated audit objects
    to latest version.
    Preconditions:
    - Execution and return of fixture
      'create_audit_and_update_first_of_two_original_controls'.
    """
    audit_with_two_controls = (
        create_audit_and_update_first_of_two_original_controls)
    audit = audit_with_two_controls["audit"]
    expected_controls = [audit_with_two_controls["updated_control"],
                         audit_with_two_controls["second_control"]]
    (webui_service.AuditsService(selenium).
     bulk_update_via_info_page(audit_obj=audit))
    actual_controls_tab_count = (webui_service.ControlsService(selenium).
                                 get_count_objs_from_tab(src_obj=audit))
    assert len(expected_controls) == actual_controls_tab_count
    actual_controls = (webui_service.ControlsService(selenium).
                       get_list_objs_from_tree_view(src_obj=audit))
    assert expected_controls == actual_controls, (
        messages.ERR_MSG_FORMAT.format(expected_controls, actual_controls))

  @pytest.mark.smoke_tests
  @pytest.mark.parametrize("tab_name", [Lhn.ALL_OBJS, Lhn.MY_OBJS])
  @pytest.mark.parametrize(
      "version_of_ctrl, is_found",
      [("new_control_rest", False), ("update_control_rest", True)],
      ids=["Snapshoted version is not found",
           "Actual snapshotable control is presented"])
  def test_search_snapshots_in_lhn(
      self, create_audit_with_control_and_update_control, selenium,
      version_of_ctrl, is_found, tab_name
  ):
    """Check via UI that LHN search not looking for snapshots."""
    audit_with_one_control = create_audit_with_control_and_update_control
    selenium_utils.open_url(selenium, dashboard.Dashboard.URL)
    lhn_menu = dashboard.Dashboard(selenium).open_lhn_menu()
    lhn_menu.select_tab(tab_name)
    control_title = audit_with_one_control[version_of_ctrl][0].title
    lhn_menu.filter_query(control_title)
    controls = (lhn_menu.select_controls_or_objectives().
                select_controls().members_visible)
    assert (control_title in [el.text for el in controls
                              if len(controls) != 0]) == is_found

  @pytest.mark.smoke_tests
  @pytest.mark.parametrize(
      "version_of_ctrl, is_found",
      [("new_control_rest", True), ("update_control_rest", False)],
      ids=["Snapshoted version is filtered",
           "Actual snapshotable control is not filtered"])
  def test_filter_of_snapshotable_control(
      self, create_audit_with_control_and_update_control, selenium,
      version_of_ctrl, is_found
  ):
    """Check via UI that filtering work for snapshoted version of Control only,
    filtering by actual values returns no items in scope of Audit page.
    """
    audit_with_one_control = create_audit_with_control_and_update_control
    audit = audit_with_one_control["new_audit_rest"][0]
    expected_control = audit_with_one_control[version_of_ctrl][0]
    filter_exp = FilterUtils.get_filter_exp_by_title(expected_control.title)
    actual_controls = (webui_service.ControlsService(selenium).
                       filter_list_objs_from_tree_view(
                       src_obj=audit, filter_exp=filter_exp))
    assert (expected_control in
            [ctrls for ctrls in actual_controls if len(actual_controls) != 0]
            ) == is_found, messages.ERR_MSG_FORMAT.format(
                [expected_control], actual_controls)

  @pytest.mark.smoke_tests
  @pytest.mark.parametrize(
      "version_of_ctrl, is_found",
      [("new_control_rest", False), ("update_control_rest", True)],
      ids=["Snapshoted version is not found",
           "Actual snapshotable control is found and already mapped to audit"])
  @pytest.mark.smoke_tests
  def test_search_unified_mapper(
      self, create_audit_with_control_and_update_control, selenium,
      version_of_ctrl, is_found
  ):
    """Check on Audit's Unified Mapper modal that Unified Mapper search not
    looking for snapshots. Search by actual state of snapshotable control
    showing control that is already mapped to audit.
    """
    audit_with_one_control = create_audit_with_control_and_update_control
    audit = audit_with_one_control["new_audit_rest"][0]
    expected_control = audit_with_one_control[version_of_ctrl][0]
    expected_map_status = MappingStatusAttrs(
        expected_control.title, True, True)
    controls_service = webui_service.ControlsService(selenium)
    actual_controls, actual_map_status = (
        controls_service.get_list_objs_from_mapper(
            src_obj=audit, dest_objs=[expected_control]))
    assert (((expected_control in actual_controls) and
            (expected_map_status in actual_map_status)) is is_found)

  @pytest.mark.smoke_tests
  def test_mapping_control_to_existing_audit(
      self, new_program_rest, new_audit_rest, new_control_rest, selenium
  ):
    """Check if Control can be mapped to existing Audit and mapping
    between Control and Program of this Audit automatically created.
    Preconditions:
    - Audit and program, and different control created via REST API
    """
    expected_control = new_control_rest
    (webui_service.ControlsService(selenium).map_objs_via_tree_view(
        src_obj=new_audit_rest, dest_objs=[new_control_rest]))
    actual_controls_count_in_tab_audit = (
        webui_service.ControlsService(selenium).
        get_count_objs_from_tab(src_obj=new_audit_rest))
    actual_control_in_audit = (
        webui_service.ControlsService(selenium).
        get_list_objs_from_tree_view(src_obj=new_audit_rest))
    actual_controls_count_in_tab_program = (
        webui_service.ControlsService(selenium).
        get_count_objs_from_tab(src_obj=new_program_rest))
    actual_control_in_program = (
        webui_service.ControlsService(selenium).
        get_list_objs_from_tree_view(src_obj=new_program_rest))
    assert (len([expected_control]) ==
            actual_controls_count_in_tab_audit ==
            actual_controls_count_in_tab_program)
    assert ([expected_control] ==
            actual_control_in_audit ==
            actual_control_in_program), messages.ERR_MSG_TRIPLE_FORMAT.format(
                expected_control,
                actual_control_in_audit,
                actual_control_in_program)
