# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com


from datetime import date
from collections import OrderedDict
from sqlalchemy import orm
from sqlalchemy import not_

from ggrc import db
from ggrc.login import get_current_user
from ggrc.models.associationproxy import association_proxy
from ggrc.models.computed_property import computed_property
from ggrc.models.context import HasOwnContext
from ggrc.models.person import Person
from ggrc.models.reflection import AttributeInfo
from ggrc.models.mixins import (
    deferred, Base, Titled, Slugged, Described, Timeboxed, Stateful,
    CustomAttributable
)
from ggrc.models.reflection import PublishOnly
from ggrc_gdrive_integration.models.object_folder import Folderable
from ggrc_workflows.models import cycle
from ggrc_workflows.models.workflow_person import WorkflowPerson
from ggrc_basic_permissions.models import UserRole


from ggrc_workflows.models import cycle_task_group_object_task as ctgot
from sqlalchemy import and_


class Workflow(CustomAttributable, HasOwnContext, Timeboxed, Described, Titled,
               Slugged, Stateful, Base, db.Model):
  __tablename__ = 'workflows'
  _title_uniqueness = False

  VALID_STATES = [u"Draft", u"Active", u"Inactive"]

  VALID_FREQUENCIES = [
      "one_time",
      "weekly",
      "monthly",
      "quarterly",
      "annually"
  ]

  @classmethod
  def default_frequency(cls):
    return 'one_time'

  @orm.validates('frequency')
  def validate_frequency(self, key, value):
    if value is None:
      value = self.default_frequency()
    if value not in self.VALID_FREQUENCIES:
      message = u"Invalid state '{}'".format(value)
      raise ValueError(message)
    return value

  notify_on_change = deferred(
      db.Column(db.Boolean, default=False, nullable=False), 'Workflow')
  notify_custom_message = deferred(
      db.Column(db.Text, nullable=True), 'Workflow')

  frequency = deferred(
      db.Column(db.String, nullable=True, default=default_frequency),
      'Workflow'
  )

  object_approval = deferred(
      db.Column(db.Boolean, default=False, nullable=False), 'Workflow')

  recurrences = db.Column(db.Boolean, default=False, nullable=False)

  workflow_people = db.relationship(
      'WorkflowPerson', backref='workflow', cascade='all, delete-orphan')
  people = association_proxy(
      'workflow_people', 'person', 'WorkflowPerson')

  task_groups = db.relationship(
      'TaskGroup', backref='workflow', cascade='all, delete-orphan')

  cycles = db.relationship(
      'Cycle', backref='workflow', cascade='all, delete-orphan')

  next_cycle_start_date = db.Column(db.Date, nullable=True)

  non_adjusted_next_cycle_start_date = db.Column(db.Date, nullable=True)

  @computed_property
  def workflow_state(self):
    return WorkflowState.get_workflow_state(self.cycles)

  _sanitize_html = [
      'notify_custom_message',
  ]

  _publish_attrs = [
      'workflow_people',
      PublishOnly('people'),
      'task_groups',
      'frequency',
      'notify_on_change',
      'notify_custom_message',
      'cycles',
      'object_approval',
      'recurrences',
      PublishOnly('next_cycle_start_date'),
      PublishOnly('non_adjusted_next_cycle_start_date'),
      PublishOnly('workflow_state'),
  ]

  _aliases = {
      "frequency": {
          "display_name": "Frequency",
          "mandatory": True,
      },
      "notify_custom_message": "Custom email message",
      "notify_on_change": "Force real-time email updates",
      "workflow_owner": {
          "display_name": "Manager",
          "type": AttributeInfo.Type.USER_ROLE,
          "mandatory": True,
          "filter_by": "_filter_by_workflow_owner",
      },
      "workflow_member": {
          "display_name": "Member",
          "type": AttributeInfo.Type.USER_ROLE,
          "filter_by": "_filter_by_workflow_member",
      },
      "workflow_mapped": {
          "display_name": "No Access",
          "type": AttributeInfo.Type.USER_ROLE,
          "filter_by": "_filter_by_no_access",
      },
      "status": None,
      "start_date": None,
      "end_date": None,
  }

  @classmethod
  def _filter_by_workflow_owner(cls, predicate):
    return cls._filter_by_role("WorkflowOwner", predicate)

  @classmethod
  def _filter_by_workflow_member(cls, predicate):
    return cls._filter_by_role("WorkflowMember", predicate)

  @classmethod
  def _filter_by_no_access(cls, predicate):
    is_no_access = not_(UserRole.query.filter(
        (UserRole.person_id == Person.id) &
        (UserRole.context_id == WorkflowPerson.context_id)
    ).exists())
    return WorkflowPerson.query.filter(
        (cls.id == WorkflowPerson.workflow_id) & is_no_access
    ).join(Person).filter(
        (predicate(Person.name) | predicate(Person.email))
    ).exists()

  def copy(self, _other=None, **kwargs):
    columns = [
        'title', 'description', 'notify_on_change', 'notify_custom_message',
        'frequency', 'end_date', 'start_date'
    ]
    target = self.copy_into(_other, columns, **kwargs)
    return target

  def copy_task_groups(self, target, **kwargs):
    for task_group in self.task_groups:
      obj = task_group.copy(
          workflow=target,
          context=target.context,
          clone_people=kwargs.get("clone_people", False),
          clone_objects=kwargs.get("clone_objects", False),
          modified_by=get_current_user(),
      )
      target.task_groups.append(obj)

      if(kwargs.get("clone_tasks", False)):
        task_group.copy_tasks(
            obj,
            clone_people=kwargs.get("clone_people", False),
            clone_objects=kwargs.get("clone_objects", True)
        )

    return target


class WorkflowState(object):

  _publish_attrs = [PublishOnly('workflow_state')]
  _update_attrs = []
  _stub_attrs = []

  @classmethod
  def _get_state(cls, current_objects):
    priority_states = OrderedDict([
        # The first True state will be returned
        ("InProgress", False),
        ("Finished", False),
        ("Assigned", False),
        ("Verified", False)
    ])

    for obj in current_objects:
      status = obj.status or "Assigned"
      priority_states[status] = True

    for state in priority_states.keys():
      if priority_states[state]:
        return state

    return None

  @classmethod
  def get_object_state(cls, objs):
    current_objects = [o for o in objs if o.cycle.is_current]

    if not current_objects:
      return None

    object_ids = [o.id for o in current_objects]
    overdue_tasks = db.session.query(
        ctgot.CycleTaskGroupObjectTask.id).join(
        cycle.Cycle).filter(
        and_(
            cycle.Cycle.is_current,
            ctgot.CycleTaskGroupObjectTask.status != "Verified",
            ctgot.CycleTaskGroupObjectTask.end_date <= date.today(),
            ctgot.CycleTaskGroupObjectTask.cycle_task_group_object_id.in_(
                object_ids),
        )
    ).count()
    if overdue_tasks:
      return "Overdue"

    return cls._get_state(current_objects)


  @classmethod
  def get_workflow_state(cls, cycles):
    current_cycles = [c for c in cycles if c.is_current]

    if not current_cycles:
      return None

    cycle_ids = [c.id for c in current_cycles]
    overdue_tasks = db.session.query(
        ctgot.CycleTaskGroupObjectTask.id).join(
        cycle.Cycle).filter(
        and_(
            cycle.Cycle.id.in_(cycle_ids),
            ctgot.CycleTaskGroupObjectTask.status != "Verified",
            ctgot.CycleTaskGroupObjectTask.end_date <= date.today()
        )
    ).count()
    if overdue_tasks:
      return "Overdue"

    return cls._get_state(current_cycles)


  @computed_property
  def workflow_state(self):
    return WorkflowState.get_object_state(self.cycle_task_group_objects)

  @classmethod
  def eager_query(cls):

    query = super(WorkflowState, cls).eager_query()
    return query.options(
        orm.subqueryload('cycle_task_group_objects')
        .undefer_group('CycleTaskGroupObject_complete'),
        orm.subqueryload_all('cycle_task_group_objects.cycle'),
    )


# TODO: This makes the Workflow module dependant on Gdrive. It is not pretty.
Workflow.__bases__ = (Folderable,) + Workflow.__bases__
Workflow.late_init_folderable()
