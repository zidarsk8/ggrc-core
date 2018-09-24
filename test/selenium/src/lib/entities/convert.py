# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Conversion of entities of different types."""
from lib.entities import app_entity


def ui_to_app(ui_obj):
  """Converts ui_entity to app_entity."""
  method_name = {
      "workflow": workflow_ui_to_app
  }[ui_obj.obj_type()]
  return method_name(ui_obj)


def workflow_ui_to_app(ui_obj):
  """Converts Workflow ui_entity to app_entity."""
  return app_entity.Workflow(
      obj_id=ui_obj.obj_id,
      title=ui_obj.title,
      admins=emails_to_app_people(ui_obj.admins),
      wf_members=emails_to_app_people(ui_obj.workflow_members),
      repeat_wf=None,
      first_task_group_title=None,
      code=ui_obj.code
  )


def emails_to_app_people(emails):
  """Converts emails to app people."""
  return [app_entity.Person(obj_id=None, email=email) for email in emails]
