# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Workflow smoke tests."""
# pylint: disable=no-self-use
# pylint: disable=unused-argument

from lib import base
from lib.entities import app_entity_factory
from lib.ui import workflow_ui_facade, ui_facade
from lib.utils import test_utils


class TestWorkflowPage(base.Test):
  """Tests for workflow functionality."""

  def test_create_workflow(self, selenium):
    """Tests creation of workflow via UI."""
    workflow = app_entity_factory.create_workflow()
    workflow_ui_facade.create_workflow(workflow)
    actual_task_group_titles = workflow_ui_facade.task_group_titles(workflow)
    assert ui_facade.active_tab_name() == "Setup (1)"
    actual_workflow = ui_facade.get_obj(workflow)
    actual_workflow.first_task_group_title = actual_task_group_titles[0]
    test_utils.obj_assert(actual_workflow, workflow)
