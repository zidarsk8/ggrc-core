# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


from datetime import date, timedelta

from sqlalchemy import and_

from ggrc_workflows.models import (
    Workflow, Cycle, CycleTaskGroupObjectTask, TaskGroupTask
)
from ggrc.services.common import Resource
from ggrc.models import (
    Notification, NotificationType, ObjectType)
from ggrc_basic_permissions.models import Role, UserRole
from ggrc import db

"""
All notifications handle the following structure:

  notifications = {
      "some@email.com": {
          "user": { user_info },

          "cycle_starts_in": {
              workflow.id: {
                  "custom_message": ""

                  "my_tasks" : # list of all tasks assigned to the user
                      { (task.id, object.id): { task_info, obj_info}, ... }

                  # list of all task groups assigned to the user, including
                  # tasks
                  "my_task_groups" :
                      { task_group.id:
                          { (task.id, object.id): { task_info, obj_info}, ... }
                      }

                  "workflow_tasks" : # list of all tasks in the workflow
                      { (task.id, object.id): { task_info, obj_info}, ... }
              }
              , ...
          }

          "cycle_started": {
              cycle.id: {
                  # manually started cycles have instant notification
                  "manually": False

                  "custom_message": ""

                  "my_tasks" : # list of all tasks assigned to the user
                      { task.id: { task_info }, ...}

                  # list of all task groups assigned to the user, including
                  # tasks
                  "my_task_groups" :
                      { task_group.id:
                          { task.id: { task_info }, ... }, ...
                      }

                  "cycle_tasks" : # list of all tasks in the workflow
                      { task.id: { task_info }, ...}

              }
              , ...
          }

          "task_declined":
              { task.id: { task_info }, ...}

          "task_reassigned":
              { task.id: { task_info }, ...}

          "due_in": # tasks due in X days (x depends on notification type)
              { task.id: { task_info }, ...}

          "due_today":
              { task.id: { task_info }, ...}

          "all_tasks_completed": # only workflow owner gets this
              { workflow.id: { workflow_info }, ... }
      }
  }

  """


def get_cycle_data(notification):
  cycle = get_object(Cycle, notification.object_id)
  manual = notification.notification_type.name == "manual_cycle_created"
  result = {}
  for person in cycle.workflow.people:
    result[person.email] = {
        "user" : get_person_dict(person),
        "cycle_started": {
            cycle.id: {
                "manually": manual,
                "custom_message": cycle.workflow.notify_custom_message,
            }
        }
    }
  return result


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
          "user" : task_assignee,
          "cycle_started": {
              cycle.id: {
                  "my_tasks": task
              }
          }
      },
      task_group_assignee['email']: {
          "user" : task_group_assignee,
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
  due = "due_in" if notification_name == "cycle_task_due_in" else "due_today"
  return {
      cycle_task.contact.email: {
          "user": get_person_dict(cycle_task.contact),
          due: {
              cycle_task.id: get_cycle_task_dict(cycle_task)
          }
      }
  }


def get_cycle_task_group_object_task_data(notification):
  notification_name = notification.notification_type.name
  if notification_name == "manual_cycle_created":
    return get_cycle_created_task_data(notification)
  elif notification_name in ["cycle_task_due_today", "cycle_task_due_in"]:
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
          "user" : task_assignee,
          "cycle_starts_in": {
              workflow.id: {
                  "my_tasks": tasks
              }
          }
      },
      task_group_assignee['email']: {
          "user" : task_group_assignee,
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

  for person in workflow.workflow_people:
    result[person.email] = {
        "user": get_person_dict(person),
        "cycle_starts_in": {
            workflow.id: {
                "custom_message": workflow.notify_custom_message
            }
        }
    }
  return result


def handle_task_group_task(obj, notification_type=None):
  if not notification_type:
    return

  notification = get_notification(obj)
  if not notification:
    notification = Notification(
        object_id=obj.id,
        object_type=get_object_type(obj),
        notification_type=notification_type,
        send_on=obj.task_group.workflow.next_cycle_start_date -
        timedelta(notification_type.advance_notice),
    )

    db.session.add(notification)


def handle_workflow_modify(sender, obj=None, src=None, service=None):
  if obj.status != "Active" or obj.frequency == "one_time":
    return

  if not obj.next_cycle_start_date:
    obj.next_cycle_start_date = date.today()

  notification = get_notification(obj)

  if not notification:
    notification_type = get_notification_type(
        "%s_workflow_starts_in" % obj.frequency)
    notification = Notification(
        object_id=obj.id,
        object_type=get_object_type(obj),
        notification_type=notification_type,
        send_on=obj.next_cycle_start_date -
        timedelta(notification_type.advance_notice),
    )

  db.session.add(notification)

  for task_group in obj.task_groups:
    for task_group_task in task_group.task_group_tasks:
      handle_task_group_task(task_group_task, notification_type)


def handle_cycle_task_group_object_task_put(obj, start_notif_type=None):
  notification = get_notification(obj)
  if not notification and start_notif_type:
    start_notification = Notification(
        object_id=obj.id,
        object_type=get_object_type(obj),
        notification_type=start_notif_type,
        send_on=date.today(),
    )
    due_in_notif_type = get_notification_type("cycle_task_due_in")
    due_in_notification = Notification(
        object_id=obj.id,
        object_type=get_object_type(obj),
        notification_type=due_in_notif_type,
        send_on=obj.end_date - timedelta(due_in_notif_type.advance_notice)
    )
    due_today_notif_type = get_notification_type("cycle_task_due_today")
    due_today_notification = Notification(
        object_id=obj.id,
        object_type=get_object_type(obj),
        notification_type=due_today_notif_type,
        send_on=obj.end_date - timedelta(due_today_notif_type.advance_notice)
    )
    db.session.add(start_notification)
    db.session.add(due_in_notification)
    db.session.add(due_today_notification)

  else:
    # handle task finished, reassigned and other stuff
    pass


def handle_cycle_created(sender, obj=None, src=None, service=None,
                         manually=False):

  notification = get_notification(obj)

  if not notification:
    db.session.flush()
    notification_type = get_notification_type(
        "manual_cycle_created" if manually else "cycle_created"
    )
    notification = Notification(
        object_id=obj.id,
        object_type=get_object_type(obj),
        notification_type=notification_type,
        send_on=date.today(),
    )
    db.session.add(notification)

  for cycle_task_group in obj.cycle_task_groups:
    for task in cycle_task_group.cycle_task_group_tasks:
      handle_cycle_task_group_object_task_put(task, notification_type)


def contributed_notifications():
  """ return handler functions for all object types
  """
  return {
      'Cycle': get_cycle_data,
      'Workflow': get_workflow_data,
      'TaskGroupTask': get_task_group_task_data,
      'CycleTaskGroupObjectTask': get_cycle_task_group_object_task_data,
  }


def register_listeners():

  @Resource.model_put.connect_via(Workflow)
  def workflow_put_listener(sender, obj=None, src=None, service=None):
    handle_workflow_modify(sender, obj, src, service)

  @Resource.model_put.connect_via(CycleTaskGroupObjectTask)
  def cycle_task_group_object_task_put_listener(
          sender, obj=None, src=None, service=None):
    handle_cycle_task_group_object_task_put(sender, obj, src, service, True)

  @Resource.model_posted.connect_via(Cycle)
  def cycle_post_listener(sender, obj=None, src=None, service=None):
    handle_cycle_created(sender, obj, src, service, True)


# Helper functions

def get_object(obj_class, obj_id):
  return db.session.query(obj_class).filter(obj_class.id == obj_id).one()


def get_object_type(obj):
  return db.session.query(ObjectType)\
      .filter(ObjectType.name == obj.__class__.__name__).one()


def get_notification_type(name):
  return db.session.query(NotificationType)\
      .filter(NotificationType.name == name).one()


def get_workflow_owner(context_id):
  return db.session.query(UserRole).join(Role).filter(
      and_(UserRole.context_id == context_id,
           Role.name == "WorkflowOwner")).one().person


def get_cycle_task_dict(cycle_task):
  return {
      "title": cycle_task.title,
      "object_title": cycle_task.cycle_task_group_object.object.title if
      cycle_task.cycle_task_group_object else "",
  }

def get_person_dict(person):
  return {
    "email": person.email,
    "name": person.name,
    "id": person.id,
  }


def get_notification(obj):
  # maybe we shouldn't return different thigs here.
  result = db.session.query(Notification).join(ObjectType).filter(
      Notification.object_id == obj.id,
      ObjectType.name == obj.__class__.__name__)
  if result.count() == 1:
    return result.one()
  else:
    return result.all()
