# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Unified mapper tests."""
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods

import pytest

from lib import base
from lib.constants import messages
from lib.service import webui_service


class TestProgramPage(base.Test):
  """Tests of unified mapper."""

  @pytest.mark.smoke_tests
  def test_mapping_controls_to_program_via_unified_mapper(
      self, selenium, new_program_rest, new_controls_rest
  ):
    """Check if Controls can be mapped to Program from Controls widget under
    Program page via unified mapper.
    Preconditions:
    - Program, Controls created via REST API.
    """
    expected_controls = new_controls_rest
    (webui_service.ControlsService(selenium).map_objs_via_tree_view(
        src_obj=new_program_rest, dest_objs=expected_controls))
    actual_controls_tab_count = (
        webui_service.ControlsService(selenium).get_count_objs_from_tab(
            src_obj=new_program_rest))
    assert len(expected_controls) == actual_controls_tab_count
    actual_controls = (webui_service.ControlsService(selenium).
                       get_list_objs_from_tree_view(src_obj=new_program_rest))
    assert sorted(expected_controls) == sorted(actual_controls), (
        messages.ERR_MSG_FORMAT.format(expected_controls, actual_controls))
