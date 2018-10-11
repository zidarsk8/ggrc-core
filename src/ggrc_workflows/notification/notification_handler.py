# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Handlers for workflow notifications.

This module contains all functions needed for handling notification objects
needed by workflow notifications. The exposed functions are the entry points
for callback listeners.

exposed functions
    handle_workflow_modify,
    handle_cycle_task_group_object_task_put,
    handle_cycle_created,
    handle_cycle_modify,
    handle_cycle_task_status_change,
"""
import datetime
import collections

from sqlalchemy import inspect

from ggrc.models.notification import Notification
from ggrc.models import all_models
from ggrc import db

from ggrc_workflows.notification import pusher


def get_notif_name_by_wf(workflow):
    if not workflow.unit:
      return "cycle_task_due_in"
    return "{}_cycle_task_due_in".format(workflow.unit)


def handle_workflow_modify(sender, obj=None, src=None, service=None):
  """Update or add notifications on a workflow update."""
  if obj.status != obj.ACTIVE or obj.unit is None:
    return
  if not obj.next_cycle_start_date:
    obj.next_cycle_start_date = obj.min_task_start_date
  pusher.update_or_create_notifications(
      obj,
      obj.next_cycle_start_date,
      "{}_workflow_starts_in".format(obj.unit),
      "cycle_start_failed")
  query = pusher.get_notification_query(
      *list(obj.tasks),
      **{"notification_names": ["cycle_start_failed"]})
  notif_type = pusher.get_notification_type("cycle_start_failed")
  exist_task_ids = set(query.distinct(Notification.object_id))
  for task in obj.tasks:
    if task.id not in exist_task_ids:
      pusher.push(task, notif_type, task.start_date)


def done_tasks_notify(tasks, day):
  """Notification handling for tasks that moved in done state.

  It will
    - delete all notifications for done tasks
    - create notification for related cycle if all tasks in done state
  """
  if not tasks:
    return
  pusher.get_notification_query(*tasks).delete(
      synchronize_session=False
  )
  cycle_tasks_dict = collections.defaultdict(list)
  cycles_dict = {}
  task_ids = []
  for obj in tasks:
    cycle_tasks_dict[obj.cycle].append(obj)
    cycles_dict[obj.cycle.id] = obj.cycle
    task_ids.append(obj.id)

  task_query = all_models.CycleTaskGroupObjectTask.query.filter(
      all_models.CycleTaskGroupObjectTask.cycle_id.in_(cycles_dict.keys()),
      all_models.CycleTaskGroupObjectTask.id.notin_(task_ids),
  ).options(
      db.Load(
          all_models.CycleTaskGroupObjectTask
      ).undefer_group(
          "CycleTaskGroupObjectTask_complete"
      )
  ).all()
  for task in task_query:
    cycle_tasks_dict[cycles_dict[task.cycle_id]].append(task)

  done_cycles = [cycle for cycle, cycle_tasks in cycle_tasks_dict.iteritems()
                 if all(task.is_done for task in cycle_tasks)]

  # this filtration is required for correct work of
  # '/admin/generate_wf_tasks_notifications' endpoint
  existing_notifications = pusher.get_notification_query(
      *done_cycles,
      **{"notification_names": ["all_cycle_tasks_completed"]}
  ).all()
  cycles_with_notifications_ids = [notif.object_id
                                   for notif in existing_notifications]
  done_cycles_without_notifs = [cycle for cycle in done_cycles
                                if cycle.id not in
                                cycles_with_notifications_ids]

  pusher.create_notifications_for_objects("all_cycle_tasks_completed",
                                          datetime.date.today(),
                                          *done_cycles_without_notifs,
                                          day=day)


def not_done_tasks_notify(tasks, day):
  """Notification handling for tasks that moved to active state.

  It will
    - create notification for tasks if it's needed
    - delete all notifications for related cycles
  """
  if not tasks:
    return
  cycles = {task.cycle for task in tasks}
  # delete all notifications for cycles about all tasks completed
  if cycles:
    pusher.get_notification_query(
        *(list(cycles)),
        **{"notification_names": ["all_cycle_tasks_completed"]}
    ).delete(
        synchronize_session=False
    )
  # recreate notifications if it's necessary
  for task in tasks:
    pusher.update_or_create_notifications(
        task,
        task.end_date,
        get_notif_name_by_wf(task.cycle.workflow),
        "cycle_task_due_today",
        "cycle_task_overdue",
        day=day
    )


def handle_cycle_task_created(ctask):
  """Create notifications on CycleTask POST operation.

  Args:
    ctask: CycleTask instance
  """
  notification_types = [get_notif_name_by_wf(ctask.workflow),
                        "cycle_task_due_today",
                        "cycle_task_overdue"]
  notification_type_query = pusher.get_notification_types(*notification_types)
  notification_types_dict = {t.name: t for t in notification_type_query}
  for n_type in notification_types:
    pusher.create_notifications_for_objects(notification_types_dict[n_type],
                                            ctask.end_date, *[ctask])


def handle_cycle_task_status_change(*objs):
  """Notification handling for task's status change."""
  declined_status = all_models.CycleTaskGroupObjectTask.DECLINED
  declined_tasks = {obj for obj in objs
                    if obj.status == declined_status}
  pusher.create_notifications_for_objects(
      pusher.get_notification_type("cycle_task_declined"),
      datetime.date.today(), *(declined_tasks)
  )


def handle_cycle_task_group_object_task_put(obj):
  if obj.has_acl_changes():
    types = ["cycle_task_reassigned", "cycle_created", "manual_cycle_created"]
    if not pusher.notification_exists_for(obj, notification_names=types):
      pusher.push(obj, pusher.get_notification_type("cycle_task_reassigned"))
  if inspect(obj).attrs.end_date.history.has_changes() and not obj.is_done:
    # if you change end date to past than overdue
    # notification should be sent today
    pusher.update_or_create_notifications(
        obj,
        obj.end_date,
        get_notif_name_by_wf(obj.cycle.workflow),
        "cycle_task_due_today",
        "cycle_task_overdue")


def handle_cycle_modify(obj):
  if not inspect(obj).attrs.is_current.history.has_changes():
    return
  if not obj.is_current:
    # delete all notifications for cycle tasks
    pusher.get_notification_query(
        *list(obj.cycle_task_group_object_tasks)
    ).delete(synchronize_session="fetch")


def handle_cycle_created(obj, manually):
  today = datetime.date.today()
  if manually:
    create_notification = "manual_cycle_created"
  else:
    create_notification = "cycle_created"
  pusher.update_or_create_notifications(obj, today, create_notification)
  if not obj.is_current:
    return
  notification_names = [get_notif_name_by_wf(obj.workflow),
                        create_notification,
                        "cycle_task_overdue",
                        "cycle_task_due_today"]
  tasks = list(obj.cycle_task_group_object_tasks)
  query = pusher.get_notification_query(
      *tasks,
      **{"notification_names": notification_names})
  exists_notifications = collections.defaultdict(set)
  for notification in query:
    exists_notifications[notification.notification_type_id].add(
        notification.object_id)
  for notification_type in pusher.get_notification_types(*notification_names):
    object_ids = exists_notifications[notification_type.id]
    notify_tasks = [t for t in tasks if not (t.id in object_ids or t.is_done)]
    if create_notification == notification_type.name:
      pusher.create_notifications_for_objects(notification_type,
                                              today,
                                              *notify_tasks)
    else:
      for task in notify_tasks:
        pusher.create_notifications_for_objects(notification_type,
                                                task.end_date,
                                                task)
