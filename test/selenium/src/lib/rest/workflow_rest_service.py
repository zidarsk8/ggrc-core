# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""REST facade for Workflow objects."""
from lib.rest import rest_convert, base_rest_service


def create_workflow(workflow):
  """Creates workflow via REST."""
  return base_rest_service.create_obj(
      workflow,
      access_control_list=rest_convert.build_access_control_list(workflow),
      title=workflow.title,
      context=rest_convert.default_context())


def create_task_group(task_group):
  """Creates task group via REST."""
  return base_rest_service.create_obj(
      task_group,
      contact=rest_convert.to_basic_rest_obj(task_group.assignee),
      title=task_group.title,
      workflow=rest_convert.to_basic_rest_obj(task_group.workflow),
      context=task_group.workflow.rest_context
  )
