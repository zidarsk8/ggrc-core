# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from datetime import date
# from babel.dates import format_timedelta
from flask import request

from sqlalchemy import and_

from ggrc_workflows.models import (
    Workflow, Cycle, CycleTaskGroupObjectTask, TaskGroupTask
)
from ggrc_basic_permissions.models import Role, UserRole
from ggrc import db
from ggrc.utils import merge_dicts


"""
exposed functions
    get_cycle_data,
    get_workflow_data,
    get_task_group_task_data,
    get_cycle_task_data,
"""


def get_cycle_created_task_data(notification):
  cycle_task = get_object(CycleTaskGroupObjectTask, notification.object_id)
  cycle_task_group = cycle_task.cycle_task_group
  cycle = cycle_task_group.cycle

  task_assignee = get_person_dict(cycle_task.contact)
  task_group_assignee = get_person_dict(cycle_task_group.contact)
  workflow_owner = get_person_dict(get_workflow_owner(cycle.context_id))
  task = {
      cycle_task.id: get_cycle_task_dict(cycle_task)
  }

  assignee_data = {
      task_assignee['email']: {
          "user": task_assignee,
          "cycle_started": {
              cycle.id: {
                  "my_tasks": task
              }
          }
      }
  }
  tg_assignee_data = {
      task_group_assignee['email']: {
          "user": task_group_assignee,
          "cycle_started": {
              cycle.id: {
                  "my_task_groups": {
                      cycle_task_group.id: task
                  }
              }
          }
      }
  }
  wf_owner_data = {
      workflow_owner['email']: {
          "user": workflow_owner,
          "cycle_started": {
              cycle.id: {
                  "cycle_tasks": task
              }
          }
      }
  }
  return merge_dicts(assignee_data, tg_assignee_data, wf_owner_data)


def get_cycle_task_due(notification):
  cycle_task = get_object(CycleTaskGroupObjectTask, notification.object_id)
  notif_name = notification.notification_type.name
  due = "due_today" if notif_name == "cycle_task_due_today" else "due_in"
  return {
      cycle_task.contact.email: {
          "user": get_person_dict(cycle_task.contact),
          due: {
              cycle_task.id: get_cycle_task_dict(cycle_task)
          }
      }
  }


def get_all_cycle_tasks_completed_data(notification, cycle):
  workflow_owner = get_person_dict(get_workflow_owner(cycle.context_id))
  return {
      workflow_owner['email']: {
          "user": workflow_owner,
          "all_tasks_completed": {
              cycle.id: get_cycle_dict(cycle)
          }
      }
  }


def get_cycle_created_data(notification, cycle):

  manual = notification.notification_type.name == "manual_cycle_created"
  result = {}

  for person in cycle.workflow.people:
    result[person.email] = {
        "user": get_person_dict(person),
        "cycle_started": {
            cycle.id: get_cycle_dict(cycle, manual)
        }
    }
  return result


def get_cycle_data(notification):
  cycle = get_object(Cycle, notification.object_id)
  notification_name = notification.notification_type.name
  if notification_name in ["manual_cycle_created", "cycle_created"]:
    return get_cycle_created_data(notification, cycle)
  elif notification_name == "all_cycle_tasks_completed":
    return get_all_cycle_tasks_completed_data(notification, cycle)

  return {}


def get_cycle_task_data(notification):
  notification_name = notification.notification_type.name
  if notification_name in ["manual_cycle_created", "cycle_created"]:
    return get_cycle_created_task_data(notification)
  elif notification_name == "cycle_task_declined":
    return {}
  elif notification_name in ["cycle_task_due_in",
                             "one_time_cycle_task_due_in",
                             "weekly_cycle_task_due_in",
                             "monthly_cycle_task_due_in",
                             "quarterly_cycle_task_due_in",
                             "annually_cycle_task_due_in",
                             "cycle_task_due_today"]:
    return get_cycle_task_due(notification)

  return {}


def get_task_group_task_data(notification):
  task_group_task = get_object(TaskGroupTask, notification.object_id)
  task_group = task_group_task.task_group
  workflow = task_group.workflow

  tasks = {}

  task_assignee = get_person_dict(task_group_task.contact)
  task_group_assignee = get_person_dict(task_group.contact)
  workflow_owner = get_person_dict(get_workflow_owner(workflow.context_id))

  for task_group_object in task_group.task_group_objects:
    tasks[task_group_task.id, task_group_object.id] = {
        "task_title": task_group_task.title,
        "object_title": task_group_object.object.title,
    }

  return {
      task_assignee['email']: {
          "user": task_assignee,
          "cycle_starts_in": {
              workflow.id: {
                  "my_tasks": tasks
              }
          }
      },
      task_group_assignee['email']: {
          "user": task_group_assignee,
          "cycle_starts_in": {
              workflow.id: {
                  "my_task_groups": {
                      task_group.id: tasks
                  }
              }
          }
      },
      workflow_owner['email']: {
          "user": workflow_owner,
          "cycle_starts_in": {
              workflow.id: {
                  "workflow_tasks": tasks
              }
          }
      },
  }


def get_workflow_data(notification):
  workflow = get_object(Workflow, notification.object_id)

  if workflow.frequency == "one_time":
    # one time workflows get cycles manually created and that triggers
    # the instant notification.
    return {}

  result = {}

  workflow_owner = get_person_dict(get_workflow_owner(workflow.context_id))

  for wf_person in workflow.workflow_people:
    result[wf_person.person.email] = {
        "user": get_person_dict(wf_person.person),
        "cycle_starts_in": {
            workflow.id: {
                "workflow_owner": workflow_owner,
                "start_date": workflow.next_cycle_start_date,
                "fuzzy_start_date": get_fuzzy_date(
                    workflow.next_cycle_start_date),
                "custom_message": workflow.notify_custom_message,
                "title": workflow.title,
            }
        }
    }
  return result


def get_object(obj_class, obj_id):
  return db.session.query(obj_class).filter(obj_class.id == obj_id).one()


def get_fuzzy_date(end_date):
  delta = end_date - date.today()
  if delta.days == 0:
    return "today"
  # TODO: use format_timedelta from babel package.
  return "in {} day{}".format(delta.days, "s" if delta.days > 1 else "")


def get_workflow_owner(context_id):
  return db.session.query(UserRole).join(Role).filter(
      and_(UserRole.context_id == context_id,
           Role.name == "WorkflowOwner")).one().person


def get_cycle_task_url(cycle_task):
  return ("{base}workflows/{workflow_id}#current_widget/cicle/{cycle_id}"
          "/cycle_task_group/{cycle_task_group_id}/"
          "/cycle_task_group_object_task/{cycle_task_id}").format(
      base=request.url_root,
      workflow_id=cycle_task.cycle_task_group.cycle.workflow.id,
      cycle_id=cycle_task.cycle_task_group.cycle.id,
      cycle_task_group_id=cycle_task.cycle_task_group.id,
      cycle_task_id=cycle_task.id,
  )


def get_cycle_task_dict(cycle_task):

  object_title = ""
  if cycle_task.cycle_task_group_object:
    object_title = cycle_task.cycle_task_group_object.object.title

  return {
      "title": cycle_task.title,
      "object_title": object_title,
      "end_date": cycle_task.end_date.strftime("%m/%d/%Y"),
      "fuzzy_due_in": get_fuzzy_date(cycle_task.end_date),
      "cycle_task_url": get_cycle_task_url(cycle_task),
  }


def get_person_dict(person):
  if person:
    return {
        "email": person.email,
        "name": person.name,
        "id": person.id,
    }

  return {"email": "", "name": "", "id": -1}


def get_cycle_url(cycle):
  return "{base}workflows/{workflow_id}#current_widget/cicle/{cycle_id}".format(
      base=request.url_root,
      workflow_id=cycle.workflow.id,
      cycle_id=cycle.id,
  )


def get_cycle_dict(cycle, manual=False):
  workflow_owner = get_person_dict(get_workflow_owner(cycle.context_id))
  return {
      "manually": manual,
      "custom_message": cycle.workflow.notify_custom_message,
      "cycle_title": cycle.title,
      "workflow_owner": workflow_owner,
      "cycle_url": get_cycle_url(cycle),
  }
