# Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Tests to Audit object."""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

import pytest

from lib import base
from lib.constants import messages
from lib.entities.entities_factory import AsmtTmplFactory, AsmtFactory
from lib.service.webui_service import (AsmtTmplService, AsmtService,
                                       ControlService)


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
    AsmtTmplService(selenium).create(audit, expected_asmt_tmpl)
    asmt_tmpls_tab_count = AsmtTmplService(selenium).get_count(audit)
    assert len([expected_asmt_tmpl]) == asmt_tmpls_tab_count
    actual_asmt_tmpls = AsmtTmplService(selenium).get_list_of_objs(audit)
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
    AsmtService(selenium).create(audit, expected_asmt)
    asmts_tab_count = AsmtService(selenium).get_count(audit)
    assert len([expected_asmt]) == asmts_tab_count
    actual_asmts = AsmtService(selenium).get_list_of_objs(audit)
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
    AsmtService(selenium).generate(
        audit, asmt_tmpl, objs_under=new_controls_rest)
    asmts_tab_count = AsmtService(selenium).get_count(audit)
    assert len(expected_asmts) == asmts_tab_count
    actual_asmts = AsmtService(selenium).get_list_of_objs(audit)
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
    controls_tab_count = ControlService(selenium).get_count(audit)
    assert len([expected_control]) == controls_tab_count
    actual_controls = ControlService(selenium).get_list_of_objs(audit)
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
    expected_updated_control = update_control_rest
    ControlService(selenium).update(audit, old_control=new_control_rest)
    updated_controls_tab_count = ControlService(selenium).get_count(audit)
    assert len([expected_updated_control]) == updated_controls_tab_count
    actual_updated_controls = ControlService(selenium).get_list_of_objs(audit)
    assert [expected_updated_control] == actual_updated_controls, (
        messages.ERR_MSG_FORMAT.format(
            [expected_updated_control], actual_updated_controls))
