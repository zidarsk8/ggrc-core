# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Workflow UI facade."""
from lib import url
from lib.page import dashboard
from lib.page.widget import tree_widget
from lib.ui import internal_ui_operations
from lib.utils import selenium_utils


def create_workflow(workflow):
  """Creates a workflow `workflow`."""
  selenium_utils.open_url(url.dashboard())
  dashboard.Dashboard().start_workflow()
  internal_ui_operations.submit_obj(workflow)


def task_group_titles(workflow):
  """Returns task group titles of `workflow`."""
  selenium_utils.open_url(url.obj_tab_url(workflow, "Setup"))
  return [item.title() for item in tree_widget.TreeWidget().tree_items()]
