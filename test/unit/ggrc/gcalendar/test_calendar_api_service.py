# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test api service for google calendar."""

import unittest
import mock

from ggrc.gcalendar import calendar_api_service


class TestCalendarApiService(unittest.TestCase):
  """Test calendar api service methods."""

  def setUp(self):
    """Set up mocks for testing."""
    calendar_api_service.CalendarApiService.calendar_auth = mock.MagicMock()
    self.service = calendar_api_service.CalendarApiService()
    self.events_mock = mock.MagicMock()
    self.service.calendar_service.events = mock.MagicMock(
        return_value=self.events_mock
    )

  def test_create_event(self):
    """Test creation of an event."""
    self.events_mock.insert = mock.MagicMock()
    self.service.create_event(
        calendar_id="primary",
        summary="test calendar event",
        description="test calendar event description",
        start="2018-01-01",
        end="2018-01-01",
        timezone="UTC",
        attendees=["someuser@example.com"],
        send_notifications=False
    )
    expected_body = {
        "summary": "test calendar event",
        "description": "test calendar event description",
        "start": {
            "date": "2018-01-01",
            "timeZone": "UTC",
        },
        "end": {
            "date": "2018-01-01",
            "timeZone": "UTC",
        },
        "attendees": [{"email": "someuser@example.com"}],
        "sendNotifications": False,
        "guestsCanModify": False,
        "guestsCanInviteOthers": False,
    }
    self.events_mock.insert.assert_called_with(calendarId="primary",
                                               body=expected_body)

  def test_update_event(self):
    """Test update of an event."""
    self.events_mock.update = mock.MagicMock()
    self.service.update_event(
        calendar_id="primary",
        summary="test calendar event",
        description="test calendar event description",
        event_id="SOMEID12345",
        start="2018-01-01",
        end="2018-01-01",
        timezone="UTC",
        attendees=["someuser@example.com"],
    )
    expected_body = {
        "summary": "test calendar event",
        "description": "test calendar event description",
        "start": {
            "date": "2018-01-01",
            "timeZone": "UTC",
        },
        "end": {
            "date": "2018-01-01",
            "timeZone": "UTC",
        },
        "attendees": [{"email": "someuser@example.com"}],
    }
    self.events_mock.update.assert_called_with(
        calendarId="primary",
        eventId="SOMEID12345",
        body=expected_body
    )

  def test_delete_event(self):
    """Test delete of an event."""
    self.events_mock.delete = mock.MagicMock()
    self.service.delete_event(
        calendar_id="primary",
        event_id="SOMEID12345",
    )
    self.events_mock.delete.assert_called_with(
        calendarId="primary",
        eventId="SOMEID12345",
    )

  def test_get_event(self):
    """Test get of an event."""
    self.events_mock.get = mock.MagicMock()
    self.service.get_event(
        calendar_id="primary",
        event_id="SOMEID12345",
    )
    self.events_mock.get.assert_called_with(
        calendarId="primary",
        eventId="SOMEID12345",
    )
