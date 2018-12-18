# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module wuth CalendarEventBuilder class."""

import datetime
import logging
import urllib
from urlparse import urljoin
from sqlalchemy.orm import load_only

from ggrc import db
from ggrc import settings
from ggrc.models import all_models
from ggrc.utils import generate_query_chunks, get_url_root


logger = logging.getLogger(__name__)


def get_event_by_date_and_attendee(attendee_id, due_date):
  """Get calendar events by attendee and due date."""
  events = all_models.CalendarEvent.query.filter(
      all_models.CalendarEvent.attendee_id == attendee_id,
      all_models.CalendarEvent.due_date == due_date,
  )
  return events.first()


def get_active_cycle_tasks_url(due_date):
  """Get CycleTask notification url."""
  base = urljoin(get_url_root(), u"dashboard#!task&query=")
  active_filter = (
      u'(("Task Status" IN ("Finished","Declined")'
      u' and "Needs Verification"=true) or ('
      u'"Task Status" IN ("Assigned","In Progress")'
      u')) and "Task Due Date"={due_date}'
  ).format(due_date=due_date)
  return base + urllib.quote(active_filter.encode('utf-8'))


def get_task_persons_ids_to_notify(task):
  """Returns set of person ids for which calendar event should be created."""
  roles_to_notify = [u"Task Assignees", u"Task Secondary Assignees"]
  person_ids = []
  for role in roles_to_notify:
    person_ids.extend(task.get_person_ids_for_rolename(role))
  return set(person_ids)


# pylint: disable=too-few-public-methods
class CalendarEventBuilder(object):
  """Class with builder methods for CalendarEvent model."""

  DEPRECATED = u"Deprecated"
  VERIFIED = u"Verified"
  FINISHED = u"Finished"
  TASK_DESCRIPTION_HEADER = u"You have due tasks for today.\n"
  TASK_DESCRIPTION_SUMMARY = (
      u"Please click on the link below to review "
      u"and take action on your task(s) due today.\n"
      u"<a href='{link}'>Link</a>")
  TASK_TITLE_TEMPLATE = u"{prefix}Your tasks are due today"

  def __init__(self):
    """Initialize CalendarEventBuilder."""
    self.title_prefix = ""
    if settings.NOTIFICATION_PREFIX:
      self.title_prefix = "[{}] ".format(settings.NOTIFICATION_PREFIX)

  def build_cycle_tasks(self):
    """Builds CalendarEvents based on CycleTaskGroupObjectTasks."""
    logger.info("Generating of events for cycle tasks...")
    self._generate_events()
    self._generate_event_descriptions()
    logger.info("Generating of events is completed.")

  def _generate_events(self):
    """Generates CalendarEvents."""
    columns = all_models.CycleTaskGroupObjectTask.query.options(
        load_only(
            all_models.CycleTaskGroupObjectTask.id,
            all_models.CycleTaskGroupObjectTask.end_date,
            all_models.CycleTaskGroupObjectTask.status,
            all_models.CycleTaskGroupObjectTask.title,
            all_models.CycleTaskGroupObjectTask.verified_date,
        )
    )
    all_count = columns.count()
    handled = 0
    for query_chunk in generate_query_chunks(columns):
      handled += query_chunk.count()
      logger.info("CycleTaskGroupObjectTasks: %s/%s", handled, all_count)
      for task in query_chunk:
        self._generate_events_for_task(task)
        db.session.flush()
      db.session.commit()

  def _generate_events_for_task(self, task):
    """Generates CalendarEvents for CycleTaskGroupObjectTask."""
    events_ids = set()
    for event in task.related_objects(all_models.CalendarEvent.__name__):
      events_ids.add(event.id)
    if self._should_create_event_for(task):
      for person_id in get_task_persons_ids_to_notify(task):
        event = get_event_by_date_and_attendee(attendee_id=person_id,
                                               due_date=task.end_date)
        if not event:
          self._create_event_with_relationship(task, person_id)
        else:
          self._create_event_relationship(task, event)
          if event.id in events_ids:
            events_ids.remove(event.id)
    for event_id in events_ids:
      self._delete_event_relationship(event_id, task)

  @staticmethod
  def _delete_event_relationship(event_id, task):
    """Deletes calendar event relationship to task."""
    if not event_id:
      return
    rel_model = all_models.Relationship
    relationship = rel_model.query.filter(
        rel_model.source_id == task.id,
        rel_model.source_type == all_models.CycleTaskGroupObjectTask.__name__,
        rel_model.destination_id == event_id,
        rel_model.destination_type == all_models.CalendarEvent.__name__,
    ).first()
    if relationship:
      db.session.delete(relationship)

  def _create_event_with_relationship(self, task, person_id):
    """Creates calendar event and relationship based on task and person id."""
    event = all_models.CalendarEvent(
        due_date=task.end_date,
        attendee_id=person_id,
        title=self.TASK_TITLE_TEMPLATE.format(prefix=self.title_prefix),
        modified_by_id=person_id,
    )
    db.session.add(event)
    db.session.add(all_models.Relationship(
        source=task,
        destination=event,
    ))
    return event

  @staticmethod
  def _create_event_relationship(task, event):
    """Creates event relationship is it is not exists."""
    rel_model = all_models.Relationship
    relationship = rel_model.query.filter(
        rel_model.destination_id == event.id,
        rel_model.destination_type == all_models.CalendarEvent.__name__,
        rel_model.source_id == task.id,
        rel_model.source_type == all_models.CycleTaskGroupObjectTask.__name__,
    ).first()
    if not relationship:
      db.session.add(all_models.Relationship(
          source=task,
          destination=event,
      ))

  def _should_create_event_for(self, task):
    """Determines should we create a Calendar Event for the task or not.

    Calendar events should NOT be created for:
    - deprecated cycle tasks.
    - verified cycle tasks (in case it has Verification flow).
    - finished cycle tasks (in case it has no Verification flow).
    - 'in progress' cycle tasks within a cycle that was ended
      (tasks are stored at 'History' tab).
    - overdue cycle tasks.
    - cycle tasks of the archived workflows.
    """

    conditions = [
        task.status in [self.DEPRECATED, self.VERIFIED],
        task.status == self.FINISHED and not task.is_verification_needed,
        task.is_in_history,
        task.is_overdue,
        task.workflow.workflow_archived,
    ]
    return not any(conditions)

  def _generate_event_descriptions(self):
    """Generates CalendarEvents descriptions."""
    columns = all_models.CalendarEvent.query.options(
        load_only(
            all_models.CalendarEvent.id,
            all_models.CalendarEvent.description,
        )
    )
    for query_chunk in generate_query_chunks(columns):
      for event in query_chunk:
        self._generate_description_for_event(event)
      db.session.commit()

  def _generate_description_for_event(self, event):
    """Generates CalendarEvent descriptions based on tasks."""
    tasks = event.related_objects(
        all_models.CycleTaskGroupObjectTask.__name__
    )
    tasks = sorted(tasks, key=lambda x: x.title)
    titles = ["- {}".format(task.title) for task in tasks]

    event.description = (
        self.TASK_DESCRIPTION_HEADER +
        "\n".join(titles) + "\n" + self.TASK_DESCRIPTION_SUMMARY.format(
            link=get_active_cycle_tasks_url(
                due_date=event.due_date.strftime('%m/%d/%Y')
            )
        )
    )
