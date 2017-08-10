# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Main notifications module.

This module is used for coordinating email notifications.
"""

from ggrc import extensions


# changes of some of the attributes are not considered as a modification of
# the obj itself, e.g. metadata not editable by the end user, or changes
# covered by other event types such as "comment created"
# pylint: disable=invalid-name
IGNORE_ATTRS = frozenset((
    u"_notifications", u"comments", u"context", u"context_id", u"created_at",
    u"custom_attribute_definitions", u"custom_attribute_values",
    u"_custom_attribute_values", u"finished_date", u"id", u"modified_by",
    u"modified_by_id", u"object_level_definitions", u"os_state",
    u"related_destinations", u"related_sources", u"status",
    u"task_group_objects", u"updated_at", u"verified_date",
))


def register_notification_listeners():
  listeners = extensions.get_module_contributions("NOTIFICATION_LISTENERS")
  for listener in listeners:
    listener()
