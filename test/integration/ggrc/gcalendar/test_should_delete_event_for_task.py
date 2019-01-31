# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test should_delete_event_for method."""

from datetime import date
import ddt
from freezegun import freeze_time

from ggrc.models import all_models
from ggrc.gcalendar import calendar_event_builder
from integration.ggrc.models import factories
from integration.ggrc.gcalendar import BaseCalendarEventTest
from integration.ggrc_workflows.models import factories as wf_factories


# pylint: disable=protected-access
@ddt.ddt
class TestShouldDeleteEventForTask(BaseCalendarEventTest):
  """Tests for _should_delete_event_for method."""

  def setUp(self):
    """Set up test."""
    super(TestShouldDeleteEventForTask, self).setUp()
    self.client.get("/login")
    self.builder = calendar_event_builder.CalendarEventBuilder()

  @ddt.data((u"Deprecated", False, True),
            (u"In Progress", False, False),
            (u"Assigned", False, False),
            (u"Finished", False, True),

            (u"Declined", True, False),
            (u"Verified", True, True),
            (u"Deprecated", True, True),
            (u"In Progress", True, False),
            (u"Finished", True, False),
            (u"Assigned", True, False))
  @ddt.unpack
  def test_task_status(
      self, task_status, is_verification_needed, should_delete_event
  ):
    """Check that the overdue event should be deleted for
       specified task statuses."""
    _, task, _ = self.setup_person_task_event(date(2015, 1, 5))
    task.cycle = wf_factories.CycleFactory(
        is_verification_needed=is_verification_needed,
    )
    task.status = task_status
    with freeze_time("2015-01-10 12:00:00"):
      self.assertEquals(self.builder._should_delete_event_for(task),
                        should_delete_event)

  def test_overdue_task(self):
    """Check that the event should not be deleted for overdue tasks."""
    _, task, _ = self.setup_person_task_event(date(2015, 1, 1))
    task.status = u"In Progress"
    with freeze_time("2015-01-05 12:00:00"):
      self.assertEquals(self.builder._should_delete_event_for(task), False)

  def test_is_in_history_task(self):
    """Check that the overdue event should be deleted is_in_history tasks."""
    _, task, _ = self.setup_person_task_event(date(2015, 1, 5))
    task.cycle = wf_factories.CycleFactory(is_current=False)
    task.status = u"In Progress"
    with freeze_time("2015-01-10 12:00:00"):
      self.assertEquals(self.builder._should_delete_event_for(task), True)

  @ddt.data((False, True), (True, False))
  @ddt.unpack
  def test_task_archived(self, recurrence, should_delete_event):
    """Check deletion of overdue event based on workflow archived states."""
    _, task, _ = self.setup_person_task_event(date(2015, 1, 6))
    with factories.single_commit():
      workflow = wf_factories.WorkflowFactory(
          unit=all_models.Workflow.WEEK_UNIT,
          recurrences=recurrence,
          next_cycle_start_date=date(2015, 1, 6),
      )
      task.cycle = wf_factories.CycleFactory(workflow=workflow)
      task.status = u"In Progress"
    with freeze_time("2015-01-10 12:00:00"):
      self.assertEquals(self.builder._should_delete_event_for(task),
                        should_delete_event)
