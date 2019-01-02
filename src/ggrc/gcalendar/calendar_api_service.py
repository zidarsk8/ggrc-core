# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module contains service for Google Calendar API."""

import logging
from apiclient import discovery


logger = logging.getLogger(__name__)


class CalendarApiService(object):
  """Service for Google Calendar API."""

  SCOPE = 'https://www.googleapis.com/auth/calendar'

  def __init__(self):
    """Initializes service object."""
    self.calendar_service = self.calendar_auth()

  @staticmethod
  def calendar_auth(version='v3'):
    """Authentication to Google Calendar.

    Requires a Service Account to be configured.

    Args:
        version: Set Calendar API version.
    Returns:
        Calendar build authenticated service object.
    """
    return discovery.build('calendar', version)

  def create_event(self, calendar_id, attendees, start, end, **kwargs):
    """Creates an event in a given Google Calendar.

    Args:
        calendar_id: Calendar ID where event will be created.
        start: event start datetime string.
        end: event start datetime string.
        attendees: comma-separated list of email attendees.
        kwargs: other event arguments.
    Returns:
        New event information.
    """

    event = {
        'summary': kwargs.get('summary', ''),
        'description': kwargs.get('description', ''),
        'start': {
            'date': start,
            'timeZone': kwargs.get('timezone', 'UTC'),
        },
        'end': {
            'date': end,
            'timeZone': kwargs.get('timezone', 'UTC'),
        },
        'attendees': [{'email': x} for x in attendees],
        'sendNotifications': kwargs.get('send_notifications', False),
        'guestsCanModify': kwargs.get('guests_can_modify', False),
        'guestsCanInviteOthers': kwargs.get('guests_can_invite', False),
    }
    return self.calendar_service.events().insert(
        calendarId=calendar_id, body=event).execute()

  # pylint: disable=too-many-arguments
  def update_event(self, event_id, calendar_id, attendees,
                   start, end, **kwargs):
    """Updates event in the given Google Calendar.

    Args:
        calendar_id: Calendar ID where event will be created.
        event_id: External event id
        attendees: attendees of the event.
        start: event start datetime string.
        end: event start datetime string.
        kwargs: other event arguments.
    Returns:
        New event information.
    """
    event = {
        'summary': kwargs.get('summary', ''),
        'description': kwargs.get('description', ''),
        'start': {
            'date': start,
            'timeZone': kwargs.get('timezone', 'UTC'),
        },
        'end': {
            'date': end,
            'timeZone': kwargs.get('timezone', 'UTC'),
        },
        'attendees': [{'email': x} for x in attendees],
    }
    return self.calendar_service.events().update(
        calendarId=calendar_id, body=event, eventId=event_id).execute()

  def delete_event(self, calendar_id, event_id):
    """Deletes an event in a given Google Calendar.

     Args:
        calendar_id: Calendar ID from which event will be deleted.
        event_id: Google Calendar Event id.
    """
    calendar = self.calendar_auth()
    calendar.events().delete(calendarId=calendar_id,
                             eventId=event_id).execute()

  def get_event(self, calendar_id, event_id):
    """Gets an event in given Google Calendar.

     Args:
        calendar_id: Calendar ID from which event will be fetched.
        event_id: Google Calendar Event id.
    """
    return self.calendar_service.events().get(calendarId=calendar_id,
                                              eventId=event_id).execute()
