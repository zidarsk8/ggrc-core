# -*- coding: utf-8 -*-
# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Object review workflow tests."""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=redefined-outer-name
import copy

import pytest

from lib import base, users, factory
from lib.constants import roles, objects, element
from lib.service import webui_facade, rest_facade, webui_service


class TestObjectsReview(base.Test):
  """Tests for objects review workflow."""

  @pytest.fixture()
  def reviewer(self):
    """Create user with role 'Creator'."""
    return rest_facade.create_user_with_role(roles.CREATOR)

  @pytest.fixture()
  def program_with_review(self, reviewer, login_as_creator, program):
    """Returns program instance with assigned review."""
    return rest_facade.request_obj_review(program, reviewer)

  @pytest.fixture()
  def program_with_approved_review(self, reviewer, program_with_review):
    """Approve program review.
    Returns program instance with approved review."""
    users.set_current_user(reviewer)
    return rest_facade.approve_obj_review(program_with_review)

  @pytest.fixture()
  def program_w_approved_via_ui_review(self, reviewer, program_with_review,
                                       selenium):
    """Approve program review via UI.
    Returns program instance with approved review."""
    users.set_current_user(reviewer)
    return webui_facade.approve_obj_review(selenium, program_with_review)

  @pytest.mark.smoke_tests
  def test_request_obj_review(self, reviewer, login_as_creator, program,
                              selenium):
    """Confirm reviewer is displayed on Program Info panel."""
    webui_facade.submit_obj_for_review(selenium, program, reviewer)
    actual_program = webui_facade.get_object(selenium, program)
    self.general_equal_assert(program.repr_ui(), actual_program)

  @pytest.mark.smoke_tests
  def test_obj_mark_reviewed(self, reviewer, program_with_review, selenium):
    """Confirm Reviewer with READ rights for an object
    able to Review an object."""
    users.set_current_user(reviewer)
    webui_facade.approve_obj_review(selenium, program_with_review)
    actual_program = webui_facade.get_object(selenium, program_with_review)
    self.general_equal_assert(program_with_review.repr_ui(), actual_program)

  @pytest.mark.smoke_tests
  def test_reviewed_obj_buttons_state(self, program_with_approved_review,
                                      selenium):
    """Confirm 'Mark reviewed' button is hidden and 'Request review' button is
    visible after review approval."""
    info_page = webui_service.ProgramsService(selenium).open_info_page_of_obj(
        program_with_approved_review)
    expected_buttons_state = {"is_mark_reviewed_btn_visible": False,
                              "is_request_review_btn_visible": True}
    actual_buttons_state = copy.deepcopy(expected_buttons_state)
    actual_buttons_state["is_mark_reviewed_btn_visible"] = (
        info_page.mark_reviewed_btn.exists)
    actual_buttons_state["is_request_review_btn_visible"] = (
        info_page.request_review_btn.exists)
    assert actual_buttons_state == expected_buttons_state

  @pytest.mark.smoke_tests
  def test_message_with_undo_btn_appears(self, reviewer,
                                         program_w_approved_via_ui_review,
                                         selenium):
    """Confirm floating message 'Review is complete' with 'Undo' button
    appears."""
    info_page = factory.get_cls_widget(
        objects.get_plural(program_w_approved_via_ui_review.type),
        is_info=True)(selenium)
    actual_elements_state = {
        "is_floating_message_visible": info_page.floating_message.exists,
        "is_undo_btn_visible": info_page.undo_button.exists}
    expected_elements_state = copy.deepcopy(actual_elements_state)
    expected_elements_state["is_floating_message_visible"] = True
    expected_elements_state["is_undo_btn_visible"] = True
    assert actual_elements_state == expected_elements_state

  @pytest.mark.smoke_tests
  def test_obj_history_is_updated(self, program_with_approved_review,
                                  selenium):
    """Confirm Review history is updated in Change Log."""
    expected_entry = {
        "author": users.current_user().email,
        "Review State": {"original_value": element.ReviewStates.UNREVIEWED,
                         "new_value": element.ReviewStates.REVIEWED}}
    actual_entries = (webui_service.ProgramsService(selenium).
                      open_info_page_of_obj(program_with_approved_review).
                      get_changelog_entries())
    assert (expected_entry == actual_entries.pop(0) and
            expected_entry not in actual_entries)

  @pytest.mark.smoke_tests
  def test_undo_obj_review_approval(self, reviewer,
                                    program_w_approved_via_ui_review,
                                    selenium):
    """Confirm Reviewer with READ rights for an object is able to unreview
    an object."""
    webui_facade.undo_obj_review_approval(selenium,
                                          program_w_approved_via_ui_review)
    actual_program = webui_facade.get_object(selenium,
                                             program_w_approved_via_ui_review)
    self.general_equal_assert(program_w_approved_via_ui_review.repr_ui(),
                              actual_program)
