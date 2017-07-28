# Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Assessments Workflow smoke tests."""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments

import copy
import pytest

from lib import base
from lib.base import Test
from lib.constants import messages, roles
from lib.constants.element import AssessmentStates
from lib.entities import entities_factory
from lib.service import webui_service, rest_service
from lib.utils import selenium_utils


class TestAssessmentsWorkflow(base.Test):
  """Tests for Assessments Workflow functionality."""

  @staticmethod
  def create_asmt(
      new_audit_rest, has_verifier, initial_state, assessments_service
  ):
    """Create Assessment with predefined state.
    Preconditions:
    - Program created via REST API.
    - Audit created under Program via REST API.
    - Assessment created under Audit via REST API.
    Returns UI representation of created object.
    """
    additional_params = {"status": initial_state}
    if has_verifier:
      additional_params["verifier"] = [roles.DEFAULT_USER]
    expected_asmt = rest_service.AssessmentsService().create_objs(
        count=1, factory_params=additional_params,
        audit=new_audit_rest.__dict__)[0]
    expected_asmt_to_compare = copy.copy(expected_asmt)
    actual_asmt = assessments_service.get_obj_from_info_page(expected_asmt)
    # due to 'actual_asmt.updated_at = None'
    # due to 'expected_asmt.custom_attributes = {None: None}'
    Test.extended_assert(
        expected_objs=[expected_asmt_to_compare], actual_objs=actual_asmt,
        issue_msg=None, is_skip_xfail=True,
        custom_attributes={None: None}, updated_at=None)
    return expected_asmt

  @pytest.mark.smoke_tests
  def test_add_comment_to_asmt_via_info_panel(
      self, new_program_rest, new_audit_rest, new_assessment_rest, selenium
  ):
    """Check via UI of possibility to correctly add comment to Assessment via
    Info Panel.
    Preconditions:
    - Program created via REST API.
    - Audit created under Program via REST API.
    - Assessment created under Audit via REST API.
    Test parameters: None
    """
    expected_asmt = new_assessment_rest
    expected_asmt_comments = [entities_factory.CommentsFactory().
                              create().repr_ui()]
    # due to 'actual_asmt.updated_at = None'
    (expected_asmt.
     update_attrs(comments=expected_asmt_comments, updated_at=None).repr_ui())
    assessments_service = webui_service.AssessmentsService(selenium)
    asmt_comments_panel = assessments_service.add_comments(
        src_obj=new_audit_rest, obj=expected_asmt,
        comment_objs=expected_asmt_comments)
    assert asmt_comments_panel.is_input_empty is True
    actual_asmt = (
        webui_service.AssessmentsService(selenium).
        get_list_objs_from_info_panels(
            src_obj=new_audit_rest, objs=expected_asmt).update_attrs(
            comments={"created_at": None}, is_replace_dicts_values=True))
    assert expected_asmt == actual_asmt, (
        messages.AssertionMessages.
        format_err_msg_equal(expected_asmt, actual_asmt))

  @pytest.mark.smoke_tests
  def test_asmt_related_asmts(
      self, new_programs_rest, new_control_rest,
      map_new_control_rest_to_new_programs_rest, new_audits_rest,
      new_assessments_rest, selenium
  ):
    """Test for checking Related Assessments. Map two Assessments to one
    snapshot of control. And check second Assessment contains in "Related
    Assessments" Tab of first Assessment. 3 Titles will be compared:
    Assessment, Audit of Assessment, generic Control
    """
    expected_titles = [(new_assessments_rest[1].title,
                        new_control_rest.title,
                        new_audits_rest[1].title)]
    asmt_service = webui_service.AssessmentsService(selenium)
    asmt_service.map_objs_via_tree_view_item(
        src_obj=new_audits_rest[0], dest_objs=[new_control_rest])
    asmt_service.map_objs_via_tree_view_item(
        src_obj=new_audits_rest[1], dest_objs=[new_control_rest])
    related_asmts_objs = (webui_service.AssessmentsService(
        selenium).get_related_asmts_titles(obj=new_assessments_rest[0]))
    assert expected_titles == related_asmts_objs

  @pytest.mark.smoke_tests
  def test_raise_issue(
      self, new_program_rest, new_audit_rest, new_assessment_rest, selenium
  ):
    """Test for checking raising Issues in Related Issues Tab. Open
    Related Issues tab on Assessments Info page. Raise Issue with pre-defined
    attributes via "raise issue" button. Compare expected Issue title and
    actual issue_titles.
    """
    expected_issue = (entities_factory.IssuesFactory().create().repr_ui())
    asmt_service = webui_service.AssessmentsService(selenium)
    asmt_service.raise_issue(new_assessment_rest, expected_issue)
    related_issues_titles = asmt_service.get_related_issues_titles(
        obj=new_assessment_rest)
    assert related_issues_titles == [expected_issue.title]

  @pytest.mark.smoke_tests
  @pytest.mark.parametrize(
      ("initial_state", "has_verifier"),
      [(AssessmentStates.NOT_STARTED, False),
       (AssessmentStates.NOT_STARTED, True),
       (AssessmentStates.IN_PROGRESS, False),
       (AssessmentStates.IN_PROGRESS, True)],
      ids=["Check if state of Assessment w'o verifier is changed from "
           "'Not Started' to 'In Progress' after update",
           "Check if state of Assessment w' verifier is changed from "
           "'Not Started' to 'In Progress' after update",
           "Check if state of Assessment w'o verifier is changed from "
           "'In Progress' to 'In Progress' after update",
           "Check if state of Assessment w' verifier is changed from "
           "'In Progress' to 'In Progress' after update"])
  def test_asmt_state_change_edit(
      self, new_program_rest, new_audit_rest, initial_state, has_verifier,
      selenium
  ):
    """Check Assessment workflow status change to correct state.
    Preconditions:
    - Program created via REST API.
    - Audit created under Program via REST API.
    - Assessment created under Audit via REST API.
    """
    assessments_service = webui_service.AssessmentsService(selenium)
    expected_asmt = (
        self.create_asmt(new_audit_rest, has_verifier, initial_state,
                         assessments_service))
    actual_asmt = (
        assessments_service.edit_obj_title_via_info_widget(
            expected_asmt).get_obj_from_info_page(obj=None))
    assert AssessmentStates.IN_PROGRESS.upper() == actual_asmt.status.upper()

  @pytest.mark.smoke_tests
  @pytest.mark.parametrize(
      ("initial_state", "final_state", "has_verifier"),
      [(AssessmentStates.NOT_STARTED, AssessmentStates.COMPLETED, False),
       (AssessmentStates.IN_PROGRESS, AssessmentStates.COMPLETED, False),
       (AssessmentStates.NOT_STARTED, AssessmentStates.READY_FOR_REVIEW, True),
       (AssessmentStates.IN_PROGRESS, AssessmentStates.READY_FOR_REVIEW, True)
       ],
      ids=["Check if state of Assessment w'o verifier is changed from "
           "'Not Started' to 'Completed' after 'Complete' button been pressed",
           "Check if state of Assessment w'o verifier is changed from "
           "'In Progress' to 'Completed' after 'Complete' button been pressed",
           "Check if state of Assessment w' verifier is changed from "
           "'Not Started' to 'Ready for Review' after 'Complete' button"
           " been pressed",
           "Check if state of Assessment w' verifier is changed from "
           "'In Progress' to 'Ready for Review' after 'Complete' button"
           " been pressed"
           ])
  def test_asmt_state_change_complete(
      self, new_program_rest, new_audit_rest, initial_state, final_state,
      has_verifier, selenium
  ):
    """Check Assessment workflow status change to correct state.
    Preconditions:
    - Program created via REST API.
    - Audit created under Program via REST API.
    - Assessment created under Audit via REST API.
    """
    assessments_service = webui_service.AssessmentsService(selenium)
    expected_asmt = (
        self.create_asmt(new_audit_rest, has_verifier, initial_state,
                         assessments_service))
    actual_asmt = (
        assessments_service.complete_assessment(expected_asmt).
        get_obj_from_info_page(obj=None))
    assert final_state.upper() == actual_asmt.status.upper()

  @pytest.mark.smoke_tests
  @pytest.mark.parametrize(
      ("expected_state", "is_verify"),
      [(AssessmentStates.COMPLETED, True),
       (AssessmentStates.IN_PROGRESS, False)],
      ids=["Check if state of Assessment w' verifier is changed from "
           "'Ready for Review' to 'Completed' after 'Verify' button been"
           " pressed",
           "Check if state of Assessment w' verifier is changed from "
           "'Ready for Review' to 'In Progress' after 'Reject' button been"
           " pressed"
           ])
  def test_asmt_state_change_verify_or_reject(
      self, new_program_rest, new_audit_rest, expected_state, is_verify,
      selenium
  ):
    """Check Assessment workflow status change to correct state.
    Preconditions:
    - Program created via REST API.
    - Audit created under Program via REST API.
    - Assessment created under Audit via REST API.
    """
    assessments_service = webui_service.AssessmentsService(selenium)
    expected_asmt = (
        self.create_asmt(new_audit_rest, True, AssessmentStates.IN_PROGRESS,
                         assessments_service))
    expected_asmt.update_attrs(status=AssessmentStates.READY_FOR_REVIEW)
    rest_service.AssessmentsService().update_obj(expected_asmt)
    selenium_utils.refresh_page(selenium)
    if is_verify:
      info_page = assessments_service.verify_assessment(expected_asmt)
    else:
      info_page = assessments_service.reject_assessment(expected_asmt)
    actual_asmt = info_page.get_obj_from_info_page(expected_asmt)
    assert expected_state.upper() == actual_asmt.status.upper()
