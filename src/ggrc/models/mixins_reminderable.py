# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com


class Reminderable(object):
  REMINDERABLE_HANDLERS = {}

  @staticmethod
  def handle_state_to_person_reminder(obj, data):
    from ggrc.notifications import notification_handlers
    from ggrc.models import notification

    if obj.status in data:
      assessor_type = data[obj.status]
      notif_name = "{}_{}_reminder".format(obj.type, assessor_type)
      notif_type = notification.NotificationType.query.filter_by(
          name=notif_name).first()
      notification_handlers._add_notification(obj, notif_type)
