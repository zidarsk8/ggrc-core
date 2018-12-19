# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

""" Module contains CalendarEventSync class."""

import logging
import datetime
from sqlalchemy.orm import load_only

from ggrc import db
from ggrc.models import all_models
from ggrc.gcalendar import calendar_api_service, utils


logger = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class CalendarEventsSync(object):
  """Class with methods for sync CalendarEvents to Calendar API."""

  def __init__(self):
    self.service = calendar_api_service.CalendarApiService()
    self.calendar_id = "primary"

  def sync_cycle_tasks_events(self):
    """Generates Calendar Events descriptions."""
    events = all_models.CalendarEvent.query.options(
        load_only(
            all_models.CalendarEvent.id,
            all_models.CalendarEvent.external_event_id,
            all_models.CalendarEvent.description,
            all_models.CalendarEvent.attendee_id,
            all_models.CalendarEvent.due_date,
            all_models.CalendarEvent.last_synced_at
        )
    ).all()
    _, event_mappings = utils.get_related_mapping(
        left=all_models.CalendarEvent,
        right=all_models.CycleTaskGroupObjectTask
    )
    for event in events:
      if event.id not in event_mappings or not event_mappings[event.id]:
        self._delete_event(event)
        db.session.delete(event)
        continue
      if not event.is_synced:
        self._create_event(event)
        continue
      self._update_event(event)
    db.session.commit()
    logger.info("Sync of Calendar Events is finished.")

  def _update_event(self, event):
    """Updates the provided event using CalendarApiService."""
    response = self.service.get_event(
        calendar_id=self.calendar_id,
        event_id=event.external_event_id
    )
    if not event.json_equals(response):
      self.service.update_event(
          event_id=event.external_event_id,
          calendar_id=self.calendar_id,
          description=event.description,
          summary=event.title,
          start=event.due_date.strftime("%Y-%m-%d"),
          end=event.due_date.strftime("%Y-%m-%d"),
          timezone="UTC",
          attendees=[event.attendee.email],
      )
      event.last_synced_at = datetime.datetime.utcnow()

  def _delete_event(self, event):
    """Deletes the provided event using CalendarApiService."""
    self.service.delete_event(calendar_id=self.calendar_id,
                              event_id=event.external_event_id)

  def _create_event(self, event):
    """Creates new event using CalendarApiService."""
    response = self.service.create_event(
        calendar_id=self.calendar_id,
        summary=event.title,
        description=event.description,
        start=event.due_date.strftime("%Y-%m-%d"),
        end=event.due_date.strftime("%Y-%m-%d"),
        timezone="UTC",
        attendees=[event.attendee.email],
        send_notifications=False
    )
    event.external_event_id = response['id']
    event.last_synced_at = datetime.datetime.utcnow()
