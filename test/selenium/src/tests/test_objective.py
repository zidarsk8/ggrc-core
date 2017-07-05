# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Objectives tests."""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods

import pytest

from lib import base

from lib.service import rest_service
from lib.service import webui_service
from lib.service.rest.client import RestClient


class TestObjectivePage(base.Test):
  """Tests of objectives."""

  @pytest.mark.smoke_tests
  @pytest.mark.parametrize(
      "is_map_again", [False, True],
      ids=["Check if Objective can be mapped to Control",
           "Check if Objective can't be mapped to Control twice"])
  def test_mapping_objective_to_control_via_rest(
      self, new_objective_rest, new_control_rest,
      map_new_control_rest_to_new_objective_rest, is_map_again, selenium
  ):
    """Check if Objective can be mapped to Control.
    Check if mapping of the same Objective to the same Control proceeds
    without exception but doesn't increase count of mapped entities
    Preconditions:
    - Objective, Control created and mapped via REST API.
    """
    # pylint: disable=no-self-use
    # pylint: disable=too-many-arguments

    status = RestClient.STATUS_CODES["OK"]
    assert map_new_control_rest_to_new_objective_rest[0].status_code == status
    if is_map_again:
      assert (rest_service.RelationshipsService().map_objs(
          src_obj=new_control_rest,
          dest_objs=[new_objective_rest]))[0].status_code == status

    actual_objectives_tab_count = (
        webui_service.ObjectivesService(selenium).get_count_objs_from_tab(
            src_obj=new_control_rest))
    assert len([new_objective_rest]) == actual_objectives_tab_count

  @pytest.mark.smoke_tests
  def test_mapping_multiple_objectives_to_control_via_rest(
      self, new_objectives_rest, new_control_rest,
      map_new_control_rest_to_new_objectives_rest, selenium
  ):
    """Check if multiple Objectives can be mapped to Control:
    number of mapped entities should become two
    Preconditions:
    - Objective, Control created and mapped via REST API.
    """
    # pylint: disable=no-self-use

    assert (
        map_new_control_rest_to_new_objectives_rest[0].status_code ==
        RestClient.STATUS_CODES["OK"])

    actual_objectives_tab_count = (
        webui_service.ObjectivesService(selenium).get_count_objs_from_tab(
            src_obj=new_control_rest))
    assert len(new_objectives_rest) == actual_objectives_tab_count
