# Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Audit smoke tests."""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments

import pytest

from lib import base
from lib.constants import messages
from lib.entities.entities_factory import AsmtTmplFactory, AsmtFactory
from lib.service.webui_service import (AsmtTmplsService, AsmtsService,
                                       ControlsService)


class TestAuditPage(base.Test):
  """Tests for the audit page."""

  @pytest.mark.smoke_tests
  def test_asmt_tmpl_creation(self, new_audit_rest, selenium):
    """Check if assessment template can be created from Audit page via
    Assessment Templates widget.
    Preconditions:
    - Audit created under Program via REST API.
    """
    audit = new_audit_rest[0]
    expected_asmt_tmpl = AsmtTmplFactory().create()
    AsmtTmplsService(selenium).create_via_tree_view(
        source_obj=audit, asmt_tmpl_obj=expected_asmt_tmpl)
    actual_asmt_tmpls_tab_count = (
        AsmtTmplsService(selenium).get_count_from_tab(source_obj=audit))
    assert len([expected_asmt_tmpl]) == actual_asmt_tmpls_tab_count
    actual_asmt_tmpls = (
        AsmtTmplsService(selenium).get_objs_from_tree_view(source_obj=audit))
    assert [expected_asmt_tmpl] == actual_asmt_tmpls, (
        messages.ERR_MSG_FORMAT.format(
            [expected_asmt_tmpl], actual_asmt_tmpls))

  @pytest.mark.smoke_tests
  def test_asmt_creation(self, new_audit_rest, selenium):
    """Check if assessment can be created from Audit page via
    Assessments widget.
    Preconditions:
    - Audit created under Program via REST API.
    """
    audit = new_audit_rest[0]
    expected_asmt = AsmtFactory().create()
    AsmtsService(selenium).create_via_tree_view(
        source_obj=audit, asmt_obj=expected_asmt)
    actual_asmts_tab_count = (
        AsmtsService(selenium).get_count_from_tab(source_obj=audit))
    assert len([expected_asmt]) == actual_asmts_tab_count
    actual_asmts = (
        AsmtsService(selenium).get_objs_from_tree_view(source_obj=audit))
    assert [expected_asmt] == actual_asmts, (
        messages.ERR_MSG_FORMAT.format([expected_asmt], actual_asmts))

  @pytest.mark.smoke_tests
  def test_asmts_generation(self, map_program_to_controls_rest,
                            new_controls_rest, new_asmt_tmpl_rest, selenium):
    """Check if assessments can be generated from Audit page via Assessments
    widget using assessment template and controls.
    Preconditions:
    - Program, Controls created via REST API.
    - Controls mapped to Program via REST API.
    - Audit created under Program via REST API.
    - Assessment Template created under Audit via REST API.
    """
    asmt_tmpl, audit, _ = new_asmt_tmpl_rest
    expected_asmts = AsmtFactory().generate(
        objs_under_asmt_tmpl=new_controls_rest, audit=audit)
    AsmtsService(selenium).generate_via_tree_view(
        source_obj=audit, asmt_tmpl_obj=asmt_tmpl,
        objs_under_asmt=new_controls_rest)
    actual_asmts_tab_count = (
        AsmtsService(selenium).get_count_from_tab(source_obj=audit))
    assert len(expected_asmts) == actual_asmts_tab_count
    actual_asmts = (
        AsmtsService(selenium).get_objs_from_tree_view(source_obj=audit))
    assert expected_asmts == actual_asmts, (
        messages.ERR_MSG_FORMAT.format(expected_asmts, actual_asmts))

  @pytest.mark.smoke_tests
  def test_audit_contains_snapshotable_ver_of_control(
      self, new_control_rest, new_program_rest, map_program_to_control_rest,
      new_audit_rest, update_control_rest, selenium
  ):
    """Check via UI that Audit contains the snapshotable Control
    that equal to original Control under Program
    after updated the original Control via REST API.
    Preconditions:
    - Program, Control created via REST API.
    - Control mapped to Program via REST API.
    - Audit created under Program via REST API.
    - Original Control updated via REST API.
    """
    audit, _ = new_audit_rest
    expected_control = new_control_rest
    actual_controls_tab_count = (
        ControlsService(selenium).get_count_from_tab(source_obj=audit))
    assert len([expected_control]) == actual_controls_tab_count
    actual_controls = (
        ControlsService(selenium).get_objs_from_tree_view(source_obj=audit))
    assert [expected_control] == actual_controls, (
        messages.ERR_MSG_FORMAT.format([expected_control], actual_controls))

  @pytest.mark.smoke_tests
  def test_update_snapshotable_ver_of_control(
      self, new_control_rest, new_program_rest, map_program_to_control_rest,
      new_audit_rest, update_control_rest, selenium
  ):
    """Check via UI that Audit contains the snapshotable Control that equal to
    updated Control under Program after updated the original Control
    via REST API and updated snapshotable Control to latest version via UI.
    Preconditions:
    - Program, Control created via REST API.
    - Control mapped to Program via REST API.
    - Audit created under Program via REST API.
    - Original Control updated via REST API.
    """
    audit, _ = new_audit_rest
    expected_control = update_control_rest
    ControlsService(selenium).update_ver_via_info_panel(
        source_obj=audit, control_obj=new_control_rest)
    actual_controls_tab_count = (
        ControlsService(selenium).get_count_from_tab(source_obj=audit))
    assert len([expected_control]) == actual_controls_tab_count
    actual_controls = (
        ControlsService(selenium).get_objs_from_tree_view(source_obj=audit))
    assert [expected_control] == actual_controls, (
        messages.ERR_MSG_FORMAT.format(
            [expected_control], actual_controls))
