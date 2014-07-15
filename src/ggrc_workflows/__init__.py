# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from datetime import date, timedelta
import calendar
from flask import Blueprint
from sqlalchemy import inspect

from ggrc import settings, db
from ggrc.login import get_current_user
#from ggrc.rbac import permissions
from ggrc.services.registry import service
from ggrc.views.registry import object_view
import ggrc_workflows.models as models


# Initialize signal handler for status changes
from blinker import Namespace
signals = Namespace()
status_change = signals.signal(
  'Status Changed',
  """
  This is used to signal any listeners of any changes in model object status
  attribute
  """)

# Initialize Flask Blueprint for extension
blueprint = Blueprint(
  'ggrc_workflows',
  __name__,
  template_folder='templates',
  static_folder='static',
  static_url_path='/static/ggrc_workflows',
)


from ggrc.models import all_models

_workflow_object_types = [
    "Program",
    "Regulation", "Standard", "Policy", "Contract",
    "Objective", "Control", "Section", "Clause",
    "System", "Process",
    "DataAsset", "Facility", "Market", "Product", "Project"
    ]

for type_ in _workflow_object_types:
  model = getattr(all_models, type_)
  model.__bases__ = (
    models.workflow_object.Workflowable,
    models.task_group_object.TaskGroupable,
    models.workflow.WorkflowState,
    ) + model.__bases__
  model.late_init_workflowable()
  model.late_init_task_groupable()


def get_public_config(current_user):
  """Expose additional permissions-dependent config to client.
  """
  return {}
#  public_config = {}
#  if permissions.is_admin():
#    if hasattr(settings, 'RISK_ASSESSMENT_URL'):
#      public_config['RISK_ASSESSMENT_URL'] = settings.RISK_ASSESSMENT_URL
#  return public_config


# Initialize service endpoints

def contributed_services():
  return [
      service('workflows', models.Workflow),
      service('workflow_objects', models.WorkflowObject),
      service('workflow_people', models.WorkflowPerson),
      service('tasks', models.Task),
      service('workflow_tasks', models.WorkflowTask),
      service('task_groups', models.TaskGroup),
      service('task_group_tasks', models.TaskGroupTask),
      service('task_group_objects', models.TaskGroupObject),

      service('cycles', models.Cycle),
      service('cycle_task_entries', models.CycleTaskEntry),
      service('cycle_task_groups', models.CycleTaskGroup),
      service('cycle_task_group_objects', models.CycleTaskGroupObject),
      service('cycle_task_group_object_tasks', models.CycleTaskGroupObjectTask)
      ]


def contributed_object_views():
  from . import models

  return [
      object_view(models.Workflow),
      object_view(models.Task),
      ]


def next_weekday(_date, direction='up'):
  '''
  _date.weekday() is 0 for Monday and 6 for Sunday.
  Must adjust any weekday that is larger than 4 (Friday)
  up to Monday or down to Friday
  '''
  if _date.weekday() > 4:
    return _date + timedelta(
      days=7 - _date.weekday() if direction == 'up' else 4 - _date.weekday()
      )
  else:
    return _date


def calc_start_date(frequency, _date, base_date=None):
  if base_date is None:
    base_date = date.today()
  direction = 'up'
  ret = None
  if frequency == "one_time":
    return next_weekday(_date, direction=direction)
  if frequency == "annually":
    ret = adjust_days(base_date.year, _date.month, _date.day)
  if frequency == "monthly":
    ret = adjust_days(
        base_date.year,
        base_date.month,
        _date.day
      )
  if frequency == "quarterly":
    ret = adjust_days(
        base_date.year,
        (base_date.month - 1) / 3 * 3 + 1 + (_date.month - 1) % 3,
        _date.day
      )
  if frequency == "weekly":
    if base_date.weekday() == _date.weekday():
      ret = base_date
    else:
      ret = base_date \
            - timedelta(days=base_date.weekday()) \
            + timedelta(days=_date.weekday())

  return next_weekday(ret, direction=direction)


def adjust_days(year, month, day):
  if(month > 12):
    year = year + 1
    month = month - 12
  if(calendar.monthrange(year, month)[1] < day):
    day = calendar.monthrange(year, month)[1]
  return date(year, month, day)


def calc_end_date(frequency, _date, start_date):
  direction = 'down'
  ret = None
  if frequency == "one_time":
    ret = _date
  if frequency == "annually":
    if start_date.month > _date.month \
       or (start_date.month == _date.month \
           and start_date.day >= _date.day):
      ret = adjust_days(start_date.year + 1, _date.month, _date.day)
    else:
      ret = adjust_days(start_date.year, _date.month, _date.day)
  if frequency == "monthly":
    ret = adjust_days(
        start_date.year,
        start_date.month \
          + 1 if start_date.day >= _date.day else start_date.month,
        _date.day
        )
  if frequency == "quarterly":
    month_in_quarter = (_date.month - 1) % 3 + 1
    start_month_in_quarter = (start_date.month - 1) % 3 + 1
    ret = adjust_days(
        start_date.year,
        ((start_date.month - 1) / 3 \
          + (1 if start_month_in_quarter > month_in_quarter
                  or start_month_in_quarter == month_in_quarter
                  and start_date.day > _date.day
              else 0)) \
          * 3 + month_in_quarter,
        _date.day
        )
  if frequency == "weekly":
    if _date.weekday() == start_date.weekday():
      ret = start_date + timedelta(days=7)
    elif start_date.weekday() < _date.weekday():
      ret = start_date \
            - timedelta(days=start_date.weekday()) \
            + timedelta(days=_date.weekday())
    else:
      ret = start_date \
            + timedelta(days=7 - start_date.weekday()) \
            + timedelta(days=_date.weekday())

  return next_weekday(ret, direction=direction)


from ggrc.services.common import Resource

@Resource.model_posted.connect_via(models.Cycle)
def handle_cycle_post(sender, obj=None, src=None, service=None):
  current_user = get_current_user()

  if not src.get('autogenerate'):
    return

  # Determine the relevant Workflow
  workflow = obj.workflow

  # Populate the top-level Cycle object
  obj.title = workflow.title
  obj.description = workflow.description
  obj.status = 'InProgress'

  obj.start_date = calc_start_date(
    workflow.frequency,
    workflow.start_date
    )
  obj.end_date = calc_end_date(
    workflow.frequency,
    workflow.end_date,
    obj.start_date
    )

  status_change.send(obj.__class__, obj=obj, new_status=obj.status, old_status=None)

  # Populate CycleTaskGroups based on Workflow's TaskGroups
  for task_group in workflow.task_groups:
    cycle_task_group = models.CycleTaskGroup(
        cycle=obj,
        task_group=task_group,
        title=task_group.title,
        description=task_group.description,
        end_date=obj.end_date,
        modified_by=current_user,
        contact=task_group.contact,
        )

    for task_group_object in task_group.task_group_objects:
      object = task_group_object.object

      cycle_task_group_object = models.CycleTaskGroupObject(
          cycle=obj,
          cycle_task_group=cycle_task_group,
          task_group_object=task_group_object,
          title=object.title,
          modified_by=current_user,
          )

      for task_group_task in task_group.task_group_tasks:
        task = task_group_task.task

        cycle_task_group_object_task = models.CycleTaskGroupObjectTask(
          cycle=obj,
          cycle_task_group_object=cycle_task_group_object,
          task_group_task=task_group_task,
          title=task.title,
          description=task.description,
          sort_index=task_group_task.sort_index,
          end_date=obj.end_date,
          contact=task_group.contact,
          status="Assigned",
          modified_by=current_user,
          )


# 'InProgress' states propagate via these links
_cycle_object_parent_attr = {
    models.CycleTaskGroupObjectTask: 'cycle_task_group_object',
    models.CycleTaskGroupObject: 'cycle_task_group',
    models.CycleTaskGroup: 'cycle'
    }

# 'Finished' and 'Verified' states are determined via these links
_cycle_object_children_attr = {
    models.CycleTaskGroupObject: 'cycle_task_group_object_tasks',
    models.CycleTaskGroup: 'cycle_task_group_objects',
    models.Cycle: 'cycle_task_groups'
    }


def update_cycle_object_parent_state(obj):
  parent_attr = _cycle_object_parent_attr.get(type(obj), None)
  if not parent_attr:
    return

  parent = getattr(obj, parent_attr, None)
  if not parent:
    return

  # If any child is `InProgress`, then parent should be `InProgress`
  if obj.status == 'InProgress' or obj.status == 'Declined':
    if parent.status != 'InProgress':
      old_status = parent.status
      parent.status = 'InProgress'
      db.session.add(parent)
      status_change.send(
          parent.__class__,
          obj=parent,
          new_status=parent.status,
          old_status=old_status
          )
      update_cycle_object_parent_state(parent)
  # If all children are `Finished` or `Verified`, then parent should be same
  elif obj.status == 'Finished' or obj.status == 'Verified':
    children_attr = _cycle_object_children_attr.get(type(parent), None)
    if children_attr:
      children = getattr(parent, children_attr, None)
      children_finished = True
      children_verified = True
      for child in children:
        if child.status != 'Verified':
          children_verified = False
          if child.status != 'Finished':
            children_finished = False
      if children_verified:
        old_status=parent.status
        parent.status = 'Verified'
        status_change.send(
            parent.__class__,
            obj=parent,
            new_status=parent.status,
            old_status=old_status
            )
        update_cycle_object_parent_state(parent)
      elif children_finished:
        old_status=parent.status
        parent.status = 'Finished'
        status_change.send(
            parent.__class__,
            obj=parent,
            new_status=parent.status,
            old_status=old_status
            )
        update_cycle_object_parent_state(parent)


@Resource.model_put.connect_via(models.CycleTaskGroupObjectTask)
def handle_cycle_task_group_object_task_put(
    sender, obj=None, src=None, service=None):
  if inspect(obj).attrs.status.history.has_changes():
    update_cycle_object_parent_state(obj)
