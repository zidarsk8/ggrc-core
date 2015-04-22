# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com


from sqlalchemy import and_, or_, inspect
from datetime import timedelta, datetime, date

from ggrc.models import (
    Notification, NotificationType, NotificationConfig, ObjectType)
from ggrc import db


"""
exposed functions
    handle_workflow_modify,
    handle_cycle_task_group_object_task_put,
    handle_cycle_created,
    handle_cycle_task_status_change,
"""


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
        "{}_workflow_starts_in".format(obj.frequency))
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


def add_new_cycle_task_notifications(obj, start_notif_type=None):
  start_notification = Notification(
      object_id=obj.id,
      object_type=get_object_type(obj),
      notification_type=start_notif_type,
      send_on=date.today(),
  )

  due_in_notif_type = get_notification_type("{}_cycle_task_due_in".format(
      obj.cycle_task_group.cycle.workflow.frequency))

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


def add_cycle_task_reassigned_notification(obj):

  # check if the current assignee allready got the first notification
  result = db.session.query(Notification)\
      .join(ObjectType)\
      .join(NotificationType)\
      .filter(and_(Notification.object_id == obj.id,  # noqa
                   ObjectType.name == obj.__class__.__name__,
                   Notification.sent_at != None,
                   or_(NotificationType.name == "cycle_task_reassigned",
                       NotificationType.name == "cycle_created",
                       NotificationType.name == "manual_cycle_created",
                       )))

  if result.count() == 0:
    return

  notification_type = get_notification_type("cycle_task_reassigned"),
  reassign_notification = Notification(
      object_id=obj.id,
      object_type=get_object_type(obj),
      send_on=date.today(),
      notification_type=notification_type)
  db.session.add(reassign_notification)


def modify_cycle_task_notification(obj, notification_name):
  notif = db.session.query(Notification)\
      .join(ObjectType)\
      .join(NotificationType)\
      .filter(and_(Notification.object_id == obj.id,
                   ObjectType.name == obj.__class__.__name__,
                   Notification.sent_at == None,  # noqa
                   NotificationType.name == notification_name,
                   ))
  notif_type = get_notification_type(notification_name)
  send_on = obj.end_date - timedelta(
      notif_type.advance_notice)

  if send_on >= datetime.now():
      # when cycle date is moved in the future, we update the current
      # notification or add a new one.
    if notif.count() == 1:
      notif = notif.one()
      notif.send_on = obj.end_date - timedelta(
          notif.notification_type.advance_notice)
      db.session.add(notif)
    else:
      notif = Notification(
          object_id=obj.id,
          object_type=get_object_type(obj),
          notification_type=notif_type,
          send_on=send_on,
      )
      db.session.add(notif)
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
      add_new_cycle_task_notifications(task, notification_type)


def get_notification(obj):
  # maybe we shouldn't return different thigs here.
  result = db.session.query(Notification).join(ObjectType).filter(
      and_(Notification.object_id == obj.id,
           ObjectType.name == obj.__class__.__name__,
           Notification.sent_at == None))  # noqa
  return result.all()


def get_object_type(obj):
  return db.session.query(ObjectType).filter(
      ObjectType.name == obj.__class__.__name__).one()


def get_notification_type(name):
  return db.session.query(NotificationType).filter(
      NotificationType.name == name).one()


def add_notif(obj, notif_type, send_on=None):
  if not send_on:
    send_on = date.today()
  notif = Notification(
      object_id=obj.id,
      object_type=get_object_type(obj),
      notification_type=notif_type,
      send_on=send_on,
  )
  db.session.add(notif)


def is_instant(workflow, person):
  def is_enabled(notif_type):
    return NotificationConfig.query.filter(
        and_(NotificationConfig.person_id == person.id,
             NotificationConfig.enable_flag == True,  # noqa
             NotificationConfig.notif_type == notif_type)).count() > 0

  if workflow.notify_on_change and is_enabled("Email_Now"):
    return "instant"

  if is_enabled("Email_Digest"):
    return "digest"

  return None
