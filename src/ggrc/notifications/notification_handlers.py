# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Notification handlers for object in the ggrc module.

This module contains all function needed for handling notification objects
needed by ggrc notifications.
"""

from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy import and_

from ggrc import db
from ggrc.services.common import Resource
from ggrc.models import request
from ggrc.models import assessment
from ggrc.models import notification


def _add_notification(obj, notif_type, when=None):
  """Add notification for an object.

  Args:
    obj (Model): an object for which we want te add a notification.
    notif_type (NotificationType): type of notification that we want to store.
    when (datetime): date and time when we want the notification to be sent.
      default value is now.
  """
  if not notif_type:
    return
  if not when:
    when = datetime.now()
  db.session.add(notification.Notification(
      object_id=obj.id,
      object_type=obj.type,
      send_on=when,
      notification_type=notif_type,
  ))


def _has_unsent_notifications(notif_type, obj):
  """Helper for searching unsent notifications.

  Args:
    notify_type (NotificationType): type of the notifications we're looking
      for.
    obj (sqlalchemy model): Object for which we're looking for notifications.

  Returs:
    True if there are any unsent notifications of notif_type for the given
    object, and False otherwise.
  """
  return db.session.query(notification.Notification).join(
      notification.NotificationType).filter(and_(
          notification.NotificationType.id == notif_type.id,
          notification.Notification.object_id == obj.id,
          notification.Notification.object_type == obj.type,
          notification.Notification.sent_at.is_(None),
      )).count() > 0


def _add_assignable_declined_notif(obj):
  """Add entries for assignable declined notifications.

  Args:
    obj (Assignable): Any object with assignable mixin for which we want to add
      notifications.
  """
  name = "{}_declined".format(obj._inflector.table_singular)
  notif_type = notification.NotificationType.query.filter_by(name=name).first()

  if not _has_unsent_notifications(notif_type, obj):
    _add_notification(obj, notif_type)


def handle_assignable_modified(obj):
  history = inspect(obj).attrs["status"].history

  # The transition from "finished" to "in progress" only happens when a task is
  # declined. So this is used as a triger for declined notifications.
  if history.deleted == [u'Finished'] and history.added == [u'In Progress']:
    _add_assignable_declined_notif(obj)


def handle_assignable_created(obj):
  name = "{}_open".format(obj._inflector.table_singular)
  notif_type = notification.NotificationType.query.filter_by(name=name).first()
  _add_notification(obj, notif_type)


def handle_assignable_deleted(obj):
  notification.Notification.query.filter_by(
      object_id=obj.id,
      object_type=obj.type,
  ).delete()


def register_handlers():
  """Register listeners for notification handlers"""

  # Variables are used as listeners, and arguments are needed for callback
  # functions.
  # pylint: disable=unused-argument,unused-variable

  @Resource.model_deleted.connect_via(request.Request)
  @Resource.model_deleted.connect_via(assessment.Assessment)
  def assignable_deleted_listener(sender, obj=None, src=None, service=None):
    handle_assignable_deleted(obj)

  @Resource.model_put.connect_via(request.Request)
  @Resource.model_put.connect_via(assessment.Assessment)
  def assignable_modified_listener(sender, obj=None, src=None, service=None):
    handle_assignable_modified(obj)

  @Resource.model_posted_after_commit.connect_via(request.Request)
  @Resource.model_posted_after_commit.connect_via(assessment.Assessment)
  def assignable_created_listener(sender, obj=None, src=None, service=None):
    handle_assignable_created(obj)
