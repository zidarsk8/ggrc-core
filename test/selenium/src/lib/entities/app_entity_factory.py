# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Factories for app_entity."""
from lib import users
from lib.entities import app_entity
from lib.utils import random_utils


def create_workflow():
  """Creates Workflow app_entity."""
  return app_entity.Workflow(
      obj_id=None,
      title=random_utils.get_title("workflow"),
      admins=[users.current_person()],
      wf_members=[],
      repeat_wf=None,
      first_task_group_title=random_utils.get_title("task_group"),
      code=None
  )


def create_person():
  """Creates Person app_entity"""
  return app_entity.Person(obj_id=None, email=random_utils.get_email())
