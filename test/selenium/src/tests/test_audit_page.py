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
from lib.entities.entities_factory import (
    AuditsFactory, AssessmentTemplatesFactory, AssessmentsFactory)
from lib.service.webui_service import (
    AuditsService, AssessmentTemplatesService, AssessmentsService,
    ControlsService, IssuesService, ProgramsService)


class TestAuditPage(base.Test):
  """Tests for audit page."""

  @pytest.fixture(scope="function")
  def create_and_clone_audit(
      self, new_program_rest, new_control_rest, map_control_to_program_rest,
      new_audit_rest, new_asmt_rest, new_asmt_tmpl_rest, new_issue_rest,
      map_issue_to_audit_rest, selenium
  ):
    """Create Audit with clonable and non clonable objects via REST API and
    clone it with them via UI.
    Preconditions:
    - Program, Control created via REST API.
    - Control mapped to Program via REST API.
    - Audit created under Program via REST API.
    - Assessment, Assessment Template, Issue created under Audit via REST API.
    - Issue mapped to Audit via REST API.
    """
    # pylint: disable=too-many-locals
    expected_audit = AuditsFactory().clone(audit=new_audit_rest[0])[0]
    expected_asmt_tmpl = AssessmentTemplatesFactory().clone(
        asmt_tmpl=new_asmt_tmpl_rest[0])[0]
    actual_audit = AuditsService(selenium).clone_via_info_widget_get_obj(
        audit_obj=new_audit_rest[0])
    return {"audit": new_audit_rest[0], "expected_audit": expected_audit,
            "actual_audit": actual_audit, "asmt": new_asmt_rest[0],
            "issue": new_issue_rest[0], "asmt_tmpl": new_asmt_tmpl_rest[0],
            "expected_asmt_tmpl": expected_asmt_tmpl,
            "control": new_control_rest, "program": new_program_rest}

  @pytest.mark.smoke_tests
  def test_asmt_tmpl_creation(self, new_audit_rest, selenium):
    """Check if assessment template can be created from Audit page via
    Assessment Templates widget.
    Preconditions:
    - Audit created under Program via REST API.
    """
    audit = new_audit_rest[0]
    expected_asmt_tmpl = AssessmentTemplatesFactory().create()
    AssessmentTemplatesService(selenium).create_via_tree_view(
        source_obj=audit, asmt_tmpl_obj=expected_asmt_tmpl)
    actual_asmt_tmpls_tab_count = (
        AssessmentTemplatesService(selenium).get_count_from_tab(
            source_obj=audit))
    assert len([expected_asmt_tmpl]) == actual_asmt_tmpls_tab_count
    actual_asmt_tmpls = (
        AssessmentTemplatesService(selenium).get_objs_from_tree_view(
            source_obj=audit))
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
    expected_asmt = AssessmentsFactory().create()
    AssessmentsService(selenium).create_via_tree_view(
        source_obj=audit, asmt_obj=expected_asmt)
    actual_asmts_tab_count = (
        AssessmentsService(selenium).get_count_from_tab(source_obj=audit))
    assert len([expected_asmt]) == actual_asmts_tab_count
    actual_asmts = AssessmentsService(selenium).get_objs_from_tree_view(
        source_obj=audit)
    assert [expected_asmt] == actual_asmts, (
        messages.ERR_MSG_FORMAT.format([expected_asmt], actual_asmts))

  @pytest.mark.smoke_tests
  def test_asmts_generation(self, map_controls_to_program_rest,
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
    expected_asmts = AssessmentsFactory().generate(
        objs_under_asmt_tmpl=new_controls_rest, audit=audit)
    AssessmentsService(selenium).generate_via_tree_view(
        source_obj=audit, asmt_tmpl_obj=asmt_tmpl,
        objs_under_asmt=new_controls_rest)
    actual_asmts_tab_count = AssessmentsService(selenium).get_count_from_tab(
        source_obj=audit)
    assert len(expected_asmts) == actual_asmts_tab_count
    actual_asmts = AssessmentsService(selenium).get_objs_from_tree_view(
        source_obj=audit)
    assert expected_asmts == actual_asmts, (
        messages.ERR_MSG_FORMAT.format(expected_asmts, actual_asmts))

  @pytest.mark.smoke_tests
  def test_audit_contains_snapshotable_ver_of_control(
      self, new_control_rest, new_program_rest, map_control_to_program_rest,
      new_audit_rest, update_control_rest, selenium
  ):
    """Check via UI that Audit contains snapshotable Control
    that equal to original Control under Program
    after updated original Control via REST API.
    Preconditions:
    - Program, Control created via REST API.
    - Control mapped to Program via REST API.
    - Audit created under Program via REST API.
    - Original Control updated via REST API.
    """
    audit, _ = new_audit_rest
    expected_control = new_control_rest
    actual_controls_tab_count = ControlsService(selenium).get_count_from_tab(
        source_obj=audit)
    assert len([expected_control]) == actual_controls_tab_count
    actual_controls = ControlsService(selenium).get_objs_from_tree_view(
        source_obj=audit)
    assert [expected_control] == actual_controls, (
        messages.ERR_MSG_FORMAT.format([expected_control], actual_controls))

  @pytest.mark.smoke_tests
  @pytest.mark.skipif(True, reason="Failed due JS error in app")
  def test_update_snapshotable_ver_of_control(
      self, new_control_rest, new_program_rest, map_control_to_program_rest,
      new_audit_rest, update_control_rest, selenium
  ):
    """Check via UI that Audit contains snapshotable Control that equal to
    updated Control under Program after updated original Control
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
    actual_controls_tab_count = ControlsService(selenium).get_count_from_tab(
        source_obj=audit)
    assert len([expected_control]) == actual_controls_tab_count
    actual_controls = ControlsService(selenium).get_objs_from_tree_view(
        source_obj=audit)
    assert [expected_control] == actual_controls, (
        messages.ERR_MSG_FORMAT.format(
            [expected_control], actual_controls))

  @pytest.mark.smoke_tests
  def test_cloned_audit_contains_new_attrs(self, create_and_clone_audit,
                                           selenium):
    """Check via UI that cloned Audit contains new predicted attributes.
    Preconditions: execution and return of fixture "create_and_clone_audit".
    """
    expected_audit = create_and_clone_audit["expected_audit"]
    actual_audit = create_and_clone_audit["actual_audit"]
    assert expected_audit == actual_audit, (
        messages.ERR_MSG_FORMAT.format(expected_audit, actual_audit))

  @pytest.mark.smoke_tests
  def test_non_clonable_objs_donot_move_to_cloned_audit(
      self, create_and_clone_audit, selenium
  ):
    """Check via UI that non clonable objects
    Assessment, Issue do not move to cloned Audit.
    Preconditions: execution and return of fixture "create_and_clone_audit".
    """
    actual_audit = create_and_clone_audit["actual_audit"]
    actual_asmts_tab_count = AssessmentsService(selenium).get_count_from_tab(
        source_obj=actual_audit)
    actual_issues_tab_count = IssuesService(selenium).get_count_from_tab(
        source_obj=actual_audit)
    assert actual_asmts_tab_count == actual_issues_tab_count == 0

  @pytest.mark.smoke_tests
  def test_clonable_audit_related_objs_move_to_cloned_audit(
      self, create_and_clone_audit, selenium
  ):
    """Check via UI that clonable audit related object
    Assessment Template move to cloned Audit.
    Preconditions: execution and return of fixture "create_and_clone_audit".
    """
    actual_audit = create_and_clone_audit["actual_audit"]
    expected_asmt_tmpl = create_and_clone_audit["expected_asmt_tmpl"]
    actual_asmt_tmpls = (
        AssessmentTemplatesService(selenium).get_objs_from_tree_view(
            source_obj=actual_audit))
    assert [expected_asmt_tmpl] == actual_asmt_tmpls, (
        messages.ERR_MSG_FORMAT.format(
            [expected_asmt_tmpl], actual_asmt_tmpls))

  @pytest.mark.smoke_tests
  def test_clonable_not_audit_related_objs_move_to_cloned_audit(
      self, create_and_clone_audit, selenium
  ):
    """Check via UI that clonable not audit related objects
    Control, Program move to cloned Audit.
    Preconditions: execution and return of fixture "create_and_clone_audit".
    """
    actual_audit = create_and_clone_audit["actual_audit"]
    expected_control = create_and_clone_audit["control"]
    expected_program = create_and_clone_audit["program"]
    actual_controls = ControlsService(selenium).get_objs_from_tree_view(
        source_obj=actual_audit)
    actual_programs = ProgramsService(selenium).get_objs_from_tree_view(
        source_obj=actual_audit)
    expected_objs = [[expected_control], [expected_program]]
    actual_objs = [actual_controls, actual_programs]
    assert expected_objs == actual_objs, (
        messages.ERR_MSG_FORMAT.format(expected_objs, actual_objs))
