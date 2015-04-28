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
from ggrc.models import NotificationConfig


"""
exposed functions
    get_cycle_data,
    get_workflow_data,
    get_task_group_task_data,
    get_cycle_task_data,
"""


def get_cycle_created_task_data(notification):
  cycle_task = get_object(CycleTaskGroupObjectTask, notification.object_id)
  if not cycle_task:
    return {}

  cycle_task_group = cycle_task.cycle_task_group
  cycle = cycle_task_group.cycle

  task_assignee = get_person_dict(cycle_task.contact)
  task_group_assignee = get_person_dict(cycle_task_group.contact)
  workflow_owners = get_workflow_owners_dict(cycle.context_id)
  task = {
      cycle_task.id: get_cycle_task_dict(cycle_task)
  }

  result = {}

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
  for workflow_owner in workflow_owners.itervalues():
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
    result = merge_dicts(result, wf_owner_data)
  return merge_dicts(result, assignee_data, tg_assignee_data)


def get_cycle_task_due(notification):
  cycle_task = get_object(CycleTaskGroupObjectTask, notification.object_id)
  if not cycle_task:
    return {}

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
  workflow_owners = get_workflow_owners_dict(cycle.context_id)
  result = {}
  for workflow_owner in workflow_owners.itervalues():
    wf_data = {
        workflow_owner['email']: {
            "user": workflow_owner,
            "all_tasks_completed": {
                cycle.id: get_cycle_dict(cycle)
            }
        }
    }
    result = merge_dicts(result, wf_data)
  return result


def get_cycle_created_data(notification, cycle):
  if not cycle.is_current:
    return {}

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
  if not cycle:
    return {}

  notification_name = notification.notification_type.name
  if notification_name in ["manual_cycle_created", "cycle_created"]:
    return get_cycle_created_data(notification, cycle)
  elif notification_name == "all_cycle_tasks_completed":
    return get_all_cycle_tasks_completed_data(notification, cycle)

  return {}


def get_cycle_task_declined_data(notification):
  cycle_task = get_object(CycleTaskGroupObjectTask, notification.object_id)
  if not cycle_task:
    return {}

  return {
      cycle_task.contact.email: {
          "user": get_person_dict(cycle_task.contact),
          "task_declined": {
              cycle_task.id: get_cycle_task_dict(cycle_task)
          }
      }
  }


def get_cycle_task_data(notification):
  notification_name = notification.notification_type.name
  if notification_name in ["manual_cycle_created", "cycle_created"]:
    return get_cycle_created_task_data(notification)
  elif notification_name == "cycle_task_declined":
    return get_cycle_task_declined_data(notification)
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
  if not task_group_task:
    return {}

  task_group = task_group_task.task_group
  workflow = task_group.workflow

  tasks = {}

  task_assignee = get_person_dict(task_group_task.contact)
  task_group_assignee = get_person_dict(task_group.contact)
  workflow_owners = get_workflow_owners_dict(workflow.context_id)

  for task_group_object in task_group.task_group_objects:
    tasks[task_group_task.id, task_group_object.id] = {
        "task_title": task_group_task.title,
        "object_title": task_group_object.object.title,
    }

  result = {}
  assignee_data = {
      task_assignee['email']: {
          "user": task_assignee,
          "cycle_starts_in": {
              workflow.id: {
                  "my_tasks": tasks
              }
          }
      }
  }
  tg_assignee_data = {
      task_group_assignee['email']: {
          "user": task_group_assignee,
          "cycle_starts_in": {
              workflow.id: {
                  "my_task_groups": {
                      task_group.id: tasks
                  }
              }
          }
      }
  }
  for workflow_owner in workflow_owners.itervalues():
    wf_owner_data = {
        workflow_owner['email']: {
            "user": workflow_owner,
            "cycle_starts_in": {
                workflow.id: {
                    "workflow_tasks": tasks
                }
            }
        }
    }
    result = merge_dicts(result, wf_owner_data)

  return merge_dicts(result, tg_assignee_data, assignee_data)


def get_workflow_data(notification):
  workflow = get_object(Workflow, notification.object_id)
  if not workflow:
    return {}

  if workflow.frequency == "one_time":
    # one time workflows get cycles manually created and that triggers
    # the instant notification.
    return {}

  result = {}

  workflow_owners = get_workflow_owners_dict(workflow.context_id)

  for wf_person in workflow.workflow_people:
    result[wf_person.person.email] = {
        "user": get_person_dict(wf_person.person),
        "cycle_starts_in": {
            workflow.id: {
                "workflow_owners": workflow_owners,
                "workflow_url": get_workflow_url(workflow),
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
  result = db.session.query(obj_class).filter(obj_class.id == obj_id)
  if result.count() == 1:
    return result.one()
  return None


def get_fuzzy_date(end_date):
  delta = end_date - date.today()
  if delta.days == 0:
    return "today"
  # TODO: use format_timedelta from babel package.
  return "in {} day{}".format(delta.days, "s" if delta.days > 1 else "")


def get_workflow_owners_dict(context_id):
  owners = db.session.query(UserRole).join(Role).filter(
      and_(UserRole.context_id == context_id,
           Role.name == "WorkflowOwner")).all()
  return {user_role.person.id: get_person_dict(user_role.person)
          for user_role in owners}


def get_cycle_task_url(cycle_task):
  return ("{base}workflows/{workflow_id}#current_widget/cycle/{cycle_id}"
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
    if cycle_task.cycle_task_group_object.object:
      object_title = cycle_task.cycle_task_group_object.object.title
    else:
      object_title = "{} [deleted]".format(
          cycle_task.cycle_task_group_object.title)

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
  return "{base}workflows/{workflow_id}#current_widget/cycle/{cycle_id}"\
      .format(
          base=request.url_root,
          workflow_id=cycle.workflow.id,
          cycle_id=cycle.id,
      )


def get_cycle_dict(cycle, manual=False):
  workflow_owners = get_workflow_owners_dict(cycle.context_id)
  return {
      "manually": manual,
      "custom_message": cycle.workflow.notify_custom_message,
      "cycle_title": cycle.title,
      "workflow_owners": workflow_owners,
      "cycle_url": get_cycle_url(cycle),
  }


def get_workflow_url(workflow):
  return "{base}workflows/{workflow_id}#current_widget".format(
      base=request.url_root,
      workflow_id=workflow.id,
  )


def should_recieve(notif, workflow, person, nightly_cron=True):
  """
  nigtly_cron - There are two types of cron jobs, nightly for email digest
  and a 5 minute cron job for instant notifications. This field is true if
  the current notification will be sent as part of the digest email, and false
  otherwise.

  send_on - In digest notifications this field is always set to a certain date.
  In instant notifications it can be set to today, or NULL. If the field is
  set, then the instant notification should be sent as part of the digest email
  for users who don't have instant notificaitons enabled. If the field is not
  set, the notification will be sent to users with instant notifications with
  the 5 minute cron job.

  """
  def is_enabled(notif_type):
    return NotificationConfig.query.filter(
        and_(NotificationConfig.person_id == person.id,
             NotificationConfig.enable_flag == True,  # noqa
             NotificationConfig.notif_type == notif_type)).count() > 0

  has_instant = is_enabled("Email_Now") or workflow.notify_on_change
  has_digest = is_enabled("Email_Digest") or has_instant

  if not nightly_cron and\
          has_instant and\
          notif.notification_type.instant and\
          not notif.send_on:
    return True

  if nightly_cron and\
          not has_instant and\
          has_digest and\
          notif.notification_type.instant and\
          notif.send_on:
    return True

  if nightly_cron and\
          not notif.notification_type.instant and\
          has_digest:
    return True

  return False

  # This if statetemt is equivalent to the tree statements above but
  # harder to read
  # if nightly_cron:
  #   if notif.notification_type.instant:
  #     return notif.send_on and\
  #       person_digest and\
  #       not has_instant
  #   else:
  #     return person_digest
  # else:
  #   return notif.notification_type.instant and\
  #     not notif.send_on and\
  #     has_instant
