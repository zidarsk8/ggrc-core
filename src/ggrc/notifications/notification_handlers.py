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

from ggrc import db
from ggrc.services.common import Resource
from ggrc.models import request
from ggrc.models import notification


def _add_notification(obj, notif_type, when=None):
  if not notif_type:
    return
  if not when:
    when = datetime.now()
  db.session.add(notification.Notification(
      object_id=obj.id,
      object_type=obj.type,
      send_on=datetime.now(),
      notification_type=notif_type,
  ))


def _add_request_declined_notification(obj):
  notif_type = notification.NotificationType.query.filter_by(
      name="request_declined").first()

  _add_notification(obj, notif_type)


def handle_request_modified(obj):
  history = inspect(obj).attrs["status"].history

  # The transition from "finished" to "in progress" only happens when a task is
  # declined. So this is used as a triger for declined notifications.
  if history.deleted == [u'Finished'] and history.added == [u'In Progress']:
    _add_request_declined_notification(obj)


def handle_request_created(obj):
  notif_type = notification.NotificationType.query.filter_by(
      name="request_open").first()

  _add_notification(obj, notif_type)


def handle_request_deleted(rel):
  notification.Notification.query.filter_by(
      object_id=rel.id,
      object_type=rel.type,
  ).delete()


def register_handlers():
  """Register listeners for notification handlers"""

  @Resource.model_deleted.connect_via(request.Request)
  def request_deleted_listener(sender, obj=None, src=None, service=None):
    handle_request_deleted(obj)

  @Resource.model_put.connect_via(request.Request)
  def request_modified_listener(sender, obj=None, src=None, service=None):
    handle_request_modified(obj)

  @Resource.model_posted_after_commit.connect_via(request.Request)
  def request_created_listener(sender, obj=None, src=None, service=None):
    handle_request_created(obj)
