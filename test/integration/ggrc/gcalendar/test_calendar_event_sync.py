# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests sync of calendar events."""

from datetime import date
from freezegun import freeze_time
import mock

from ggrc.gcalendar import calendar_event_sync, calendar_api_service
from integration.ggrc.models import factories
from integration.ggrc.gcalendar import BaseCalendarEventTest


# pylint: disable=protected-access
class TestCalendarEventSync(BaseCalendarEventTest):
  """Test calendar event sync."""

  def setUp(self):
    """Set up test with mocks."""
    super(TestCalendarEventSync, self).setUp()
    self.client.get("/login")
    with mock.patch("ggrc.gcalendar.calendar_api_service"
                    ".CalendarApiService.calendar_auth"):
      self.sync = calendar_event_sync.CalendarEventsSync()

  def test_create_event(self):
    """Test creation of event."""
    create_event_mock = mock.MagicMock()
    calendar_api_service.CalendarApiService.create_event = create_event_mock

    with factories.single_commit():
      person = factories.PersonFactory()
      event = factories.CalendarEventFactory(
          due_date=date(2015, 1, 15),
          attendee_id=person.id,
      )
    with freeze_time("2015-01-1 12:00:00"):
      self.sync._create_event(event)
    create_event_mock.assert_called_with(
        calendar_id="primary",
        summary=event.title,
        description=event.description,
        start="2015-01-15",
        end="2015-01-15",
        timezone="UTC",
        attendees=[person.email],
        send_notifications=False
    )
    self.assertEquals(event.last_synced_at.date(), date(2015, 1, 1))

  def test_update_event(self):
    """Test update of event."""
    update_event_mock = mock.MagicMock()
    get_event_mock = mock.MagicMock(return_value={
        "description": "old description",
        "summary": "summary",
        "eventId": "eventId",
    })
    calendar_api_service.CalendarApiService.update_event = update_event_mock
    calendar_api_service.CalendarApiService.get_event = get_event_mock

    with factories.single_commit():
      person = factories.PersonFactory()
      event = factories.CalendarEventFactory(
          due_date=date(2015, 1, 15),
          attendee_id=person.id,
          description="new description",
          title="summary",
          external_event_id="eventId"
      )
    with freeze_time("2015-01-1 12:00:00"):
      self.sync._update_event(event)
    update_event_mock.assert_called_with(
        event_id="eventId",
        calendar_id="primary",
        description="new description",
        summary="summary",
        start="2015-01-15",
        end="2015-01-15",
        timezone="UTC",
        attendees=[person.email],
    )
    self.assertEquals(event.last_synced_at.date(), date(2015, 1, 1))

  def test_fail_to_sync_event(self):
    """Test that sync job tried to sync the second event after a failure."""
    create_event_mock = mock.MagicMock(side_effect=Exception("test"))
    calendar_api_service.CalendarApiService.create_event = create_event_mock
    with factories.single_commit():
      self.setup_person_task_event(date(2015, 1, 5))
      self.setup_person_task_event(date(2015, 1, 6))
    with freeze_time("2015-01-1 12:00:00"):
      self.sync.sync_cycle_tasks_events()
    self.assertEqual(create_event_mock.call_count, 2)
