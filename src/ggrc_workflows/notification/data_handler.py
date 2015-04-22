
from datetime import date
# from babel.dates import format_timedelta

from sqlalchemy import and_

from ggrc_workflows.models import (
    Workflow, Cycle, CycleTaskGroupObjectTask, TaskGroupTask
)
from ggrc_basic_permissions.models import Role, UserRole
from ggrc import db


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

  return {
      task_assignee['email']: {
          "user": task_assignee,
          "cycle_started": {
              cycle.id: {
                  "my_tasks": task
              }
          }
      },
      task_group_assignee['email']: {
          "user": task_group_assignee,
          "cycle_started": {
              cycle.id: {
                  "my_task_groups": {
                      cycle_task_group.id: task
                  }
              }
          }
      },
      workflow_owner['email']: {
          "user": workflow_owner,
          "cycle_started": {
              cycle.id: {
                  "workflow_tasks": task
              }
          }
      },
  }


def get_cycle_task_due(notification):
  cycle_task = get_object(CycleTaskGroupObjectTask, notification.object_id)
  notification_name = notification.notification_type.name
  due = "due_today" if notification_name == "cycle_task_due_today" else "due_in"
  return {
      cycle_task.contact.email: {
          "user": get_person_dict(cycle_task.contact),
          due: {
              cycle_task.id: get_cycle_task_dict(cycle_task)
          }
      }
  }



def get_cycle_data(notification):
  cycle = get_object(Cycle, notification.object_id)
  manual = notification.notification_type.name == "manual_cycle_created"
  result = {}

  workflow_owner = get_person_dict(get_workflow_owner(cycle.context_id))

  for person in cycle.workflow.people:
    result[person.email] = {
        "user": get_person_dict(person),
        "cycle_started": {
            cycle.id: {
                "manually": manual,
                "custom_message": cycle.workflow.notify_custom_message,
                "cycle_title": cycle.title,
                "workflow_owner": workflow_owner,
            }
        }
    }
  return result


def get_cycle_task_data(notification):
  notification_name = notification.notification_type.name
  if notification_name in ["manual_cycle_created", "cycle_created"]:
    return get_cycle_created_task_data(notification)
  return get_cycle_task_due(notification)


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


def get_workflow_owner(context_id):
  return db.session.query(UserRole).join(Role).filter(
      and_(UserRole.context_id == context_id,
           Role.name == "WorkflowOwner")).one().person


def get_cycle_task_dict(cycle_task):

  object_title = ""
  if cycle_task.cycle_task_group_object:
    object_title = cycle_task.cycle_task_group_object.object.title

  return {
      "title": cycle_task.title,
      "object_title": object_title,
      "end_date": cycle_task.end_date.strftime("%m/%d/%Y"),
      "fuzzy_due_in": get_fuzzy_date(cycle_task.end_date),
  }

def get_fuzzy_date(end_date):
  delta = date.today() - end_date
  if delta.days == 0:
    return "today"
  # TODO: use format_timedelta from babel package.
  return "in {} days".format(delta.days)


def get_person_dict(person):
  if person:
    return {
        "email": person.email,
        "name": person.name,
        "id": person.id,
    }

  return {"email": "", "name": "", "id": -1}
