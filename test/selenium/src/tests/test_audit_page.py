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
from lib.service import webui_service


class TestAuditPage(base.Test):
  """Tests for audit functionality."""

  @pytest.fixture(scope="function")
  def create_and_clone_audit(
      self, new_program_rest, new_control_rest,
      map_new_program_rest_to_new_control_rest, new_audit_rest,
      new_assessment_rest, new_assessment_template_rest, new_issue_rest,
      selenium
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
    expected_audit = AuditsFactory().clone(audit=new_audit_rest)[0]
    expected_asmt_tmpl = AssessmentTemplatesFactory().clone(
        asmt_tmpl=new_assessment_template_rest)[0]
    actual_audit = (
        webui_service.AuditsService(selenium).
        clone_via_info_page_and_get_obj(audit_obj=new_audit_rest)
    )
    return {
        "audit": new_audit_rest, "expected_audit": expected_audit,
        "actual_audit": actual_audit, "assessment": new_assessment_rest,
        "issue": new_issue_rest,
        "assessment_template": new_assessment_template_rest,
        "expected_assessment_template": expected_asmt_tmpl,
        "control": new_control_rest, "program": new_program_rest
    }

  @pytest.mark.smoke_tests
  def test_asmt_tmpl_creation(self, new_program_rest, new_audit_rest,
                              selenium):
    """Check if Assessment Template can be created from Audit page via
    Assessment Templates widget.
    Preconditions:
    - Audit created under Program via REST API.
    """
    expected_asmt_tmpl = AssessmentTemplatesFactory().create()
    (webui_service.AssessmentTemplatesService(selenium).
     create_obj_via_tree_view(src_obj=new_audit_rest, obj=expected_asmt_tmpl))
    actual_asmt_tmpls_tab_count = (
        webui_service.AssessmentTemplatesService(selenium).
        get_count_objs_from_tab(src_obj=new_audit_rest))
    assert len([expected_asmt_tmpl]) == actual_asmt_tmpls_tab_count
    actual_asmt_tmpls = (webui_service.AssessmentTemplatesService(selenium).
                         get_list_objs_from_tree_view(src_obj=new_audit_rest))
    assert [expected_asmt_tmpl] == actual_asmt_tmpls, (
        messages.ERR_MSG_FORMAT.format(
            [expected_asmt_tmpl], actual_asmt_tmpls))

  @pytest.mark.smoke_tests
  def test_asmt_creation(self, new_program_rest, new_audit_rest, selenium):
    """Check if Assessment can be created from Audit page via
    Assessments widget.
    Preconditions:
    - Audit created under Program via REST API.
    """
    expected_asmt = AssessmentsFactory().create()
    (webui_service.AssessmentsService(selenium).
     create_obj_via_tree_view(src_obj=new_audit_rest, obj=expected_asmt))
    actual_asmts_tab_count = (webui_service.AssessmentsService(selenium).
                              get_count_objs_from_tab(src_obj=new_audit_rest))
    assert len([expected_asmt]) == actual_asmts_tab_count
    actual_asmts = (webui_service.AssessmentsService(selenium).
                    get_list_objs_from_tree_view(src_obj=new_audit_rest))
    assert [expected_asmt] == actual_asmts, (
        messages.ERR_MSG_FORMAT.format([expected_asmt], actual_asmts))

  @pytest.mark.smoke_tests
  def test_asmts_generation(
      self, new_program_rest, new_controls_rest,
      map_new_program_rest_to_new_controls_rest, new_audit_rest,
      new_assessment_template_rest, selenium
  ):
    """Check if Assessments can be generated from Audit page via Assessments
    widget using Assessment template and Controls.
    Preconditions:
    - Program, Controls created via REST API.
    - Controls mapped to Program via REST API.
    - Audit created under Program via REST API.
    - Assessment Template created under Audit via REST API.
    """
    expected_asmts = (AssessmentsFactory().generate(
        objs_under_asmt_tmpl=new_controls_rest, audit=new_audit_rest))
    (webui_service.AssessmentsService(selenium).generate_objs_via_tree_view(
        src_obj=new_audit_rest, asmt_tmpl_obj=new_assessment_template_rest,
        objs_under_asmt=new_controls_rest))
    actual_asmts_tab_count = (webui_service.AssessmentsService(selenium).
                              get_count_objs_from_tab(src_obj=new_audit_rest))
    assert len(expected_asmts) == actual_asmts_tab_count
    actual_asmts = (webui_service.AssessmentsService(selenium).
                    get_list_objs_from_tree_view(src_obj=new_audit_rest))
    assert expected_asmts == actual_asmts, (
        messages.ERR_MSG_FORMAT.format(expected_asmts, actual_asmts))

  @pytest.mark.smoke_tests
  @pytest.mark.cloning
  def test_cloned_audit_contains_new_attrs(
      self, create_and_clone_audit, selenium
  ):
    """Check via UI that cloned Audit contains new predicted attributes.
    Preconditions:
    - Execution and return of fixture 'create_and_clone_audit'.
    """
    expected_audit = create_and_clone_audit["expected_audit"]
    actual_audit = create_and_clone_audit["actual_audit"]
    assert expected_audit == actual_audit, (
        messages.ERR_MSG_FORMAT.format(expected_audit, actual_audit))

  @pytest.mark.smoke_tests
  @pytest.mark.cloning
  def test_non_clonable_objs_donot_move_to_cloned_audit(
      self, create_and_clone_audit, selenium
  ):
    """Check via UI that non clonable objects
    Assessment, Issue do not move to cloned Audit.
    Preconditions:
    - Execution and return of fixture 'create_and_clone_audit'.
    """
    actual_audit = create_and_clone_audit["actual_audit"]
    actual_asmts_tab_count = (webui_service.AssessmentsService(selenium).
                              get_count_objs_from_tab(src_obj=actual_audit))
    actual_issues_tab_count = (webui_service.IssuesService(selenium).
                               get_count_objs_from_tab(src_obj=actual_audit))
    assert actual_asmts_tab_count == actual_issues_tab_count == 0

  @pytest.mark.smoke_tests
  @pytest.mark.cloning
  def test_clonable_audit_related_objs_move_to_cloned_audit(
      self, create_and_clone_audit, selenium
  ):
    """Check via UI that clonable audit related object
    Assessment Template move to cloned Audit.
    Preconditions:
    -Execution and return of fixture 'create_and_clone_audit'.
    """
    actual_audit = create_and_clone_audit["actual_audit"]
    expected_asmt_tmpl = create_and_clone_audit["expected_assessment_template"]
    actual_asmt_tmpls = (webui_service.AssessmentTemplatesService(selenium).
                         get_list_objs_from_tree_view(src_obj=actual_audit))
    assert [expected_asmt_tmpl] == actual_asmt_tmpls, (
        messages.ERR_MSG_FORMAT.format(
            [expected_asmt_tmpl], actual_asmt_tmpls))

  @pytest.mark.smoke_tests
  @pytest.mark.cloning
  def test_clonable_not_audit_related_objs_move_to_cloned_audit(
      self, create_and_clone_audit, selenium
  ):
    """Check via UI that clonable not audit related objects
    Control, Program move to cloned Audit.
    Preconditions:
    -Execution and return of fixture 'create_and_clone_audit'.
    """
    actual_audit = create_and_clone_audit["actual_audit"]
    expected_control = create_and_clone_audit["control"]
    expected_program = create_and_clone_audit["program"]
    actual_controls = (webui_service.ControlsService(selenium).
                       get_list_objs_from_tree_view(src_obj=actual_audit))
    actual_programs = (webui_service.ProgramsService(selenium).
                       get_list_objs_from_tree_view(src_obj=actual_audit))
    expected_objs = [[expected_control], [expected_program]]
    actual_objs = [actual_controls, actual_programs]
    assert expected_objs == actual_objs, (
        messages.ERR_MSG_FORMAT.format(expected_objs, actual_objs))
