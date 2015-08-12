# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc import db
from ggrc_workflows.models import Cycle
from ggrc_workflows.models import CycleTaskGroup
from ggrc_workflows.models import CycleTaskGroupObjectTask as CycleTask
from ggrc_workflows.models import TaskGroup
from ggrc_workflows.models import TaskGroupTask
from ggrc_workflows.models import WORKFLOW_OBJECT_TYPES


def tg_task(object_type, related_type, related_ids):
  """ relationships between Task Groups and Task Group Tasks """

  if object_type == "TaskGroup":
    return db.session.query(TaskGroupTask.task_group_id).filter(
        TaskGroupTask.id.in_(related_ids))
  else:
    return db.session.query(TaskGroupTask.id).filter(
        TaskGroupTask.task_group_id.in_(related_ids))


def cycle_workflow(object_type, related_type, related_ids):
  """ relationships between Workflows and Cycles """

  if object_type == "Workflow":
    return db.session.query(Cycle.workflow_id).filter(
        Cycle.id.in_(related_ids))
  else:
    return db.session.query(Cycle.id).filter(
        Cycle.workflow_id.in_(related_ids))


def workflow_tg(object_type, related_type, related_ids):
  """ relationships between Workflows and Task Groups """

  if object_type == "Workflow":
    return db.session.query(TaskGroup.workflow_id).filter(
        TaskGroup.id.in_(related_ids))
  else:
    return db.session.query(TaskGroup.id).filter(
        TaskGroup.workflow_id.in_(related_ids))

def tg_tgo(object_type, related_type, related_ids):
  """ relationships between Task Groups and Objects """
  pass

def cycle_ctg(object_type, related_type, related_ids):
  """ relationships between Cycle and Cycle Task Group """

  if object_type == "Cycle":
    return db.session.query(CycleTaskGroup.cycle_id).filter(
        CycleTaskGroup.id.in_(related_ids))
  else:
    return db.session.query(CycleTaskGroup.id).filter(
        CycleTaskGroup.cycle_id.in_(related_ids))


def ctg_ctgot(object_type, related_type, related_ids):
  """ relationships between Cycle Task Groups and Cycle Tasks """
  if object_type == "CycleTaskGroup":
    return db.session.query(CycleTask.cycle_task_group_id).filter(
        CycleTask.id.in_(related_ids))
  else:
    return db.session.query(CycleTask.id).filter(
        CycleTask.cycle_task_group_id.in_(related_ids))

_function_map = {
    ("TaskGroup", "Workflow"): workflow_tg,
    ("TaskGroup", "TGO"): tg_tgo,
    ("TaskGroup", "TaskGroupTask"): tg_task,
    ("Cycle", "Workflow"): cycle_workflow,
    ("Cycle", "CycleTaskGroup"): cycle_ctg,
    ("CycleTaskGroup", "CycleTaskGroupObjectTask"): ctg_ctgot,
}


def get_ids_related_to(object_type, related_type, related_ids):
  if object_type in WORKFLOW_OBJECT_TYPES:
    key = tuple(sorted(["TGO", related_type]))
  elif related_type in WORKFLOW_OBJECT_TYPES:
    key = tuple(sorted([object_type, "TGO"]))
  else:
    key = tuple(sorted([object_type, related_type]))

  query_function = _function_map.get(key)
  if callable(query_function):
    return query_function(object_type, related_type, related_ids)
  return None
