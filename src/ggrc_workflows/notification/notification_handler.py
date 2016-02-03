# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Handlers for workflow notifications.

This module contains all function needed for handling notification objects
needed by workflow notifications. The exposed functions are the entry points
for callback listeners.

exposed functions
    handle_workflow_modify,
    handle_cycle_task_group_object_task_put,
    handle_cycle_created,
    handle_cycle_modify,
    handle_cycle_task_status_change,
"""

from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import inspect
from datetime import timedelta
from datetime import datetime
from datetime import date

from ggrc import db
from ggrc.models.notification import Notification
from ggrc.models.notification import NotificationType


def handle_task_group_task(obj, notif_type=None):
  """Add notification entry for task group tasks.

  Args:
    obj: Instance of a model for which the notification should be scheduled.
    notif_type: The notification type for the scheduled notification.
  """
  if not notif_type:
    return

  notification = get_notification(obj)
  if not notification:
    start_date = obj.task_group.workflow.next_cycle_start_date
    send_on = start_date - timedelta(notif_type.advance_notice)
    add_notif(obj, notif_type, send_on)


def handle_workflow_modify(sender, obj=None, src=None, service=None):
  """Update or add notifications on a workflow update."""
  if obj.status != "Active" or obj.frequency == "one_time":
    return

  if not obj.next_cycle_start_date:
    obj.next_cycle_start_date = date.today()

  notification = get_notification(obj)
  notif_type = get_notification_type(
      "{}_workflow_starts_in".format(obj.frequency))

  if not notification:
    send_on = obj.next_cycle_start_date - timedelta(notif_type.advance_notice)
    add_notif(obj, notif_type, send_on)

    notif_type = get_notification_type("cycle_start_failed")
    add_notif(obj, notif_type, obj.next_cycle_start_date + timedelta(1))

  for task_group in obj.task_groups:
    for task_group_task in task_group.task_group_tasks:
      handle_task_group_task(task_group_task, notif_type)


def add_cycle_task_due_notifications(obj):
  """Add notifications entries for cycle task due dates.

  Create two notification entries, one for X days before the due date and one
  on the due date.

  Args:
    obj: Cycle object for notification generation.
  """
  if obj.status == "Verified":
    return
  if not obj.cycle_task_group.cycle.is_current:
    return

  notif_type = get_notification_type("{}_cycle_task_due_in".format(
      obj.cycle_task_group.cycle.workflow.frequency))
  send_on = obj.end_date - timedelta(notif_type.advance_notice)
  add_notif(obj, notif_type, send_on)

  notif_type = get_notification_type("cycle_task_due_today")
  send_on = obj.end_date - timedelta(notif_type.advance_notice)
  add_notif(obj, notif_type, send_on)


def add_cycle_task_notifications(obj, start_notif_type=None):
  """Add start and due  notification entries for cycle tasks."""
  add_notif(obj, start_notif_type, date.today())
  add_cycle_task_due_notifications(obj)


def add_cycle_task_reassigned_notification(obj):
  """Add or update notifications for reassigned cycle tasks."""
  # check if the current assignee allready got the first notification
  result = db.session.query(Notification)\
      .join(NotificationType)\
      .filter(and_(Notification.object_id == obj.id,  # noqa
                   Notification.object_type == obj.type,
                   Notification.sent_at != None,
                   or_(NotificationType.name == "cycle_task_reassigned",
                       NotificationType.name == "cycle_created",
                       NotificationType.name == "manual_cycle_created",
                       )))

  if result.count() == 0:
    return

  notif_type = get_notification_type("cycle_task_reassigned")
  add_notif(obj, notif_type)


def modify_cycle_task_notification(obj, notification_name):
  notif = db.session.query(Notification)\
      .join(NotificationType)\
      .filter(and_(Notification.object_id == obj.id,
                   Notification.object_type == obj.type,
                   Notification.sent_at == None,  # noqa
                   NotificationType.name == notification_name,
                   ))
  notif_type = get_notification_type(notification_name)
  send_on = obj.end_date - timedelta(
      notif_type.advance_notice)

  today = datetime.combine(date.today(), datetime.min.time())
  if send_on >= today:
      # when cycle date is moved in the future, we update the current
      # notification or add a new one.
    if notif.count() == 1:
      notif = notif.one()
      notif.send_on = obj.end_date - timedelta(
          notif.notification_type.advance_notice)
      db.session.add(notif)
    else:
      add_notif(obj, notif_type, send_on)
  else:
    # this should not be allowed, but if a cycle task is changed to a past
    # date, we remove the current pending notification if it exists
    for notif in notif.all():
      db.session.delete(notif)


def modify_cycle_task_end_date(obj):
  modify_cycle_task_notification(obj, "{}_cycle_task_due_in".format(
      obj.cycle_task_group.cycle.workflow.frequency))
  modify_cycle_task_notification(obj, "cycle_task_due_today")


def check_all_cycle_tasks_finished(cycle):
  statuses = set([task.status for task in cycle.cycle_task_group_object_tasks])
  acceptable_statuses = set(['Verified'])
  return statuses.issubset(acceptable_statuses)


def handle_cycle_task_status_change(obj, new_status, old_status):
  if obj.status == "Declined":
    notif_type = get_notification_type("cycle_task_declined")
    add_notif(obj, notif_type)

  elif obj.status == "Verified":
    for notif in get_notification(obj):
      db.session.delete(notif)

    cycle = obj.cycle_task_group.cycle
    if check_all_cycle_tasks_finished(cycle):
      notif_type = get_notification_type("all_cycle_tasks_completed")
      add_notif(cycle, notif_type)
    db.session.flush()


def handle_cycle_task_group_object_task_put(obj):
  if inspect(obj).attrs.contact.history.has_changes():
    add_cycle_task_reassigned_notification(obj)
  if inspect(obj).attrs.end_date.history.has_changes():
    modify_cycle_task_end_date(obj)


def remove_all_cycle_task_notifications(obj):
  for cycle_task in obj.cycle_task_group_object_tasks:
    for notif in get_notification(cycle_task):
      db.session.delete(notif)


def handle_cycle_modify(sender, obj=None, src=None, service=None):
  if not obj.is_current:
    remove_all_cycle_task_notifications(obj)


def handle_cycle_created(sender, obj=None, src=None, service=None,
                         manually=False):

  notification = get_notification(obj)

  if not notification:
    db.session.flush()
    notification_type = get_notification_type(
        "manual_cycle_created" if manually else "cycle_created"
    )
    add_notif(obj, notification_type)

  for cycle_task_group in obj.cycle_task_groups:
    for task in cycle_task_group.cycle_task_group_tasks:
      add_cycle_task_notifications(task, notification_type)


def get_notification(obj):
  # maybe we shouldn't return different thigs here.
  result = Notification.query.filter(
      and_(Notification.object_id == obj.id,
           Notification.object_type == obj.type,
           Notification.sent_at == None))  # noqa
  return result.all()


def get_notification_type(name):
  return db.session.query(NotificationType).filter(
      NotificationType.name == name).first()


def add_notif(obj, notif_type, send_on=None):
  if not send_on:
    send_on = date.today()
  notif = Notification(
      object_id=obj.id,
      object_type=obj.type,
      notification_type=notif_type,
      send_on=send_on,
  )
  db.session.add(notif)
