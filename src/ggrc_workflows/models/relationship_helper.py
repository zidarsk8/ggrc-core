# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc import db
from ggrc_workflows.models import TaskGroup


def workflow_task_group(object_type, related_type, related_ids):
  if {object_type, related_type} != {"Workflow", "TaskGroup"}:
    return None

  if object_type == "Workflow":
    return db.session.query(TaskGroup.workflow_id).filter(
        TaskGroup.id.in_(related_ids))
  else:
    return db.session.query(TaskGroup.id).filter(
        TaskGroup.workflow_id.in_(related_ids))


def get_ids_related_to(object_type, related_type, related_ids):
  return [
      workflow_task_group(object_type, related_type, related_ids),
  ]
