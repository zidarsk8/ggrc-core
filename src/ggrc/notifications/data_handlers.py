# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Data handlers for notifications for objects in ggrc module."""

from ggrc.models import request


def request_open_data(notif):
  """Get data for open requests.

  Args:
    notif (Notification): Notification entry for a request with request_open
      notification type.

  Returns:
    A dict containing all notification data for the given notification.
  """
  req = request.Request.query.get(notif.object_id)
  data = {}
  for person, _ in req.assignees:
    data[person.email] = {
        "request_open": {
            req.id: {
                "title": req.title
            }
        }
    }
  return data


def request_declined_data(notif):
  """Get data for declined requests.

  Args:
    notif (Notification): Notification entry for a request with
      request_declined notification type.

  Returns:
    A dict containing all notification data for the given notification.
  """
  req = request.Request.query.get(notif.object_id)
  data = {}
  requesters = [person for person, role in req.assignees
                if "Requester" in role]
  for person in requesters:
    data[person.email] = {
        "request_open": {
            req.id: {
                "title": req.title
            }
        }
    }
  return data


def get_request_data(notif):
  """Return data for request notifications.

  Args:
    notif (Notification): notification with Request object_type.

  Returns:
    Dict with all data fro the request notification or an empty dict if the
    notification is not for requests.
  """
  if notif.object_type != "Request":
    return {}
  elif notif.notification_type.name == "request_open":
    return request_open_data(notif)
  elif notif.notification_type.name == "request_declined":
    return request_declined_data(notif)
  return {}
