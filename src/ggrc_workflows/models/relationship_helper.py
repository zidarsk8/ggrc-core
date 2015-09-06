# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from sqlalchemy import and_

from ggrc import db
from ggrc_workflows.models import Cycle
from ggrc_workflows.models import CycleTaskGroup
from ggrc_workflows.models import CycleTaskGroupObjectTask as CycleTask
from ggrc_workflows.models import CycleTaskGroupObject
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


def workflow_tgt(object_type, related_type, related_ids):
  """ indirect relationships between Workflows and Tasks """

  if object_type == "Workflow":
    return db.session.query(TaskGroup.workflow_id).join(TaskGroupTask).filter(
        TaskGroupTask.id.in_(related_ids))
  else:
    return db.session.query(TaskGroupTask.id).join(TaskGroup).filter(
        TaskGroup.workflow_id.in_(related_ids))


def workflow_ctg(object_type, related_type, related_ids):
  """ indirect relationships between Workflows and Cycle Task Groups """

  if object_type == "Workflow":
    return db.session.query(Cycle.workflow_id).join(CycleTaskGroup).filter(
        CycleTaskGroup.id.in_(related_ids))
  else:
    return db.session.query(CycleTaskGroup.id).join(Cycle).filter(
        Cycle.workflow_id.in_(related_ids))


def workflow_ctgot(object_type, related_type, related_ids):
  """ indirect relationships between Workflows and Cycle Tasks """

  if object_type == "Workflow":
    return db.session.query(Cycle.workflow_id) \
        .join(CycleTaskGroup).join(CycleTask).filter(
            CycleTask.id.in_(related_ids))
  else:
    return db.session.query(CycleTask.id) \
        .join(CycleTaskGroup).join(Cycle).filter(
            Cycle.workflow_id.in_(related_ids))


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


def ctgot_wot(object_type, related_type, related_ids):
  """ relationships between Cycle Task and Cycle Task Objects """
  if object_type == "CycleTaskGroupObjectTask":
    return db.session.query(CycleTask.id).join(CycleTaskGroupObject).filter(
        and_(
            CycleTaskGroupObject.object_type == related_type,
            CycleTaskGroupObject.object_id.in_(related_ids)
        ))
  else:
    return db.session.query(CycleTaskGroupObject.object_id).join(CycleTask)\
        .filter(CycleTask.id.in_(related_ids))

_function_map = {
    ("Cycle", "CycleTaskGroup"): cycle_ctg,
    ("Cycle", "Workflow"): cycle_workflow,
    ("CycleTaskGroup", "CycleTaskGroupObjectTask"): ctg_ctgot,
    ("CycleTaskGroup", "Workflow"): workflow_ctg,
    ("CycleTaskGroupObjectTask", "Workflow"): workflow_ctgot,
    ("TaskGroup", "TaskGroupTask"): tg_task,
    ("TaskGroup", "Workflow"): workflow_tg,
    ("TaskGroupTask", "Workflow"): workflow_tgt,
}

# add mappings for cycle tasks and cycle task objects
for wot in WORKFLOW_OBJECT_TYPES:
  obj = "CycleTaskGroupObjectTask"
  key = tuple(sorted([obj, wot]))
  _function_map[key] = ctgot_wot


def get_ids_related_to(object_type, related_type, related_ids):
  key = tuple(sorted([object_type, related_type]))
  query_function = _function_map.get(key)
  if callable(query_function):
    return query_function(object_type, related_type, related_ids)
  return None
