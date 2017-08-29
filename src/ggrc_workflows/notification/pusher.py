import datetime
from dateutil import relativedelta

from sqlalchemy import or_
from sqlalchemy import tuple_
from sqlalchemy.sql.expression import true

from ggrc import db
from ggrc.models.notification import Notification
from ggrc.models.notification import NotificationType


REPEATABLE_NOTIFICATIONS = {"cycle_task_overdue", }


def get_notification_query(*objs, **kwargs):
  # maybe we shouldn't return different thigs here.
  keys = [(obj.id, obj.type) for obj in objs]
  notif_key = tuple_(Notification.object_id, Notification.object_type)
  query = Notification.query.filter(
      or_(Notification.sent_at.is_(None), Notification.repeating == true())
  ).filter(
      notif_key.in_(keys)
  )
  notification_names = kwargs.get('notification_names') or []
  if notification_names:
    type_ids = [get_notification_type(n).id for n in notification_names]
    query = query.filter(
        Notification.notification_type_id.in_(type_ids)
    )
  return query


def notification_exists_for(*obj, **kwargs):
  return db.session.query(
      get_notification_query(*obj, **kwargs).exists()
  ).scalar()


def get_notification_type(name):
  # NOTE: add cache here
  return NotificationType.query.filter(NotificationType.name == name).first()


def push(obj, notif_type, send_on=None, repeating=False):
  return Notification(
      object=obj,
      notification_type=notif_type,
      send_on=send_on or datetime.date.today(),
      repeating=repeating,
  )


def update_or_create_notifications(obj, send_at, *notification_names):
  today = datetime.datetime.combine(datetime.date.today(),
                                    datetime.datetime.min.time())
  for notification_name in notification_names:
    notif_type = get_notification_type(notification_name)
    repeatable_notification = notification_name in REPEATABLE_NOTIFICATIONS
    send_on_date = send_at - relativedelta.relativedelta(
        days=notif_type.advance_notice
    )
    send_on = datetime.datetime.combine(send_on_date,
                                        datetime.datetime.min.time())
    if repeatable_notification:
      send_on = max(send_on, today)
    query = get_notification_query(
        obj, notification_names=[notification_name]
    )
    if send_on < today:
      # this should not be allowed, but if a cycle task is changed to a past
      # date, we remove the current pending notification if it exists
      query.delete(synchronize_session="fetch")
    elif not query.update({Notification.send_on: send_on},
                          synchronize_session="fetch"):
      # when cycle date is moved in the future and no current create new
      # notification
      push(obj, notif_type, send_on, repeatable_notification)
