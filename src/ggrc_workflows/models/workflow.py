# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Workflow object and WorkflowState mixins.

This contains the basic Workflow object and a mixin for determining the state
of the Objects that are mapped to any cycle tasks.
"""

from collections import OrderedDict
from datetime import date
from sqlalchemy import and_
from sqlalchemy import not_
from sqlalchemy import orm

from ggrc import db
from ggrc.login import get_current_user
from ggrc.models import reflection
from ggrc.models.associationproxy import association_proxy
from ggrc.models.computed_property import computed_property
from ggrc.models.context import HasOwnContext
from ggrc.models.mixins import Base
from ggrc.models.mixins import CustomAttributable
from ggrc.models.mixins import Described
from ggrc.models.mixins import Slugged
from ggrc.models.mixins import Stateful
from ggrc.models.mixins import Timeboxed
from ggrc.models.mixins import Titled
from ggrc.models.mixins import deferred
from ggrc.models.person import Person
from ggrc_basic_permissions.models import UserRole
from ggrc_gdrive_integration.models import object_folder
from ggrc_workflows.models import cycle
from ggrc_workflows.models import cycle_task_group_object_task as ctgot
from ggrc_workflows.models import workflow_person


class Workflow(CustomAttributable, HasOwnContext, Timeboxed, Described, Titled,
               Slugged, Stateful, Base, db.Model):
  """Basic Workflow first class object.
  """
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
  def validate_frequency(self, _, value):
    """Make sure that value is listed in valid frequencies.

    Args:
      value: A string value for requested frequency

    Returns:
      default_frequency which is 'one_time' if the value is None, or the value
      itself.

    Raises:
      Value error, if the value is not None or in the VALID_FREQUENCIES array.
    """
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
      reflection.PublishOnly('people'),
      'task_groups',
      'frequency',
      'notify_on_change',
      'notify_custom_message',
      'cycles',
      'object_approval',
      'recurrences',
      reflection.PublishOnly('next_cycle_start_date'),
      reflection.PublishOnly('non_adjusted_next_cycle_start_date'),
      reflection.PublishOnly('workflow_state'),
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
          "type": reflection.AttributeInfo.Type.USER_ROLE,
          "mandatory": True,
          "filter_by": "_filter_by_workflow_owner",
      },
      "workflow_member": {
          "display_name": "Member",
          "type": reflection.AttributeInfo.Type.USER_ROLE,
          "filter_by": "_filter_by_workflow_member",
      },
      "workflow_mapped": {
          "display_name": "No Access",
          "type": reflection.AttributeInfo.Type.USER_ROLE,
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
    """Get query that filters workflows with mapped users.

    Args:
      predicate: lambda function that excepts a single parameter and returns
        true of false.

    Returns:
      An sqlalchemy query that evaluates to true or false and can be used in
      filtering workflows by no_access users.
    """
    is_no_access = not_(UserRole.query.filter(
        (UserRole.person_id == Person.id) &
        (UserRole.context_id == workflow_person.WorkflowPerson.context_id)
    ).exists())
    return workflow_person.WorkflowPerson.query.filter(
        (cls.id == workflow_person.WorkflowPerson.workflow_id) & is_no_access
    ).join(Person).filter(
        (predicate(Person.name) | predicate(Person.email))
    ).exists()

  def copy(self, _other=None, **kwargs):
    """Create a partial copy of the current workflow.
    """
    columns = [
        'title', 'description', 'notify_on_change', 'notify_custom_message',
        'frequency', 'end_date', 'start_date'
    ]
    target = self.copy_into(_other, columns, **kwargs)
    return target

  def copy_task_groups(self, target, **kwargs):
    """Copy all task groups and tasks mapped to this workflow.
    """
    for task_group in self.task_groups:
      obj = task_group.copy(
          workflow=target,
          context=target.context,
          clone_people=kwargs.get("clone_people", False),
          clone_objects=kwargs.get("clone_objects", False),
          modified_by=get_current_user(),
      )
      target.task_groups.append(obj)

      if kwargs.get("clone_tasks"):
        task_group.copy_tasks(
            obj,
            clone_people=kwargs.get("clone_people", False),
            clone_objects=kwargs.get("clone_objects", True)
        )

    return target


class WorkflowState(object):
  """Object state mixin.

  This is a mixin for adding workflow_state to all objects that can be mapped
  to workflow tasks.
  """

  _publish_attrs = [reflection.PublishOnly('workflow_state')]
  _update_attrs = []
  _stub_attrs = []

  @classmethod
  def _get_state(cls, current_objects):
    """Get lowest state of the objects.

    Return the least done state off all objects. Function will work correctly
    only for non Overdue states. If the result is overdue, it should be
    handled outsid of this function.

    Args:
      current_objects: list of objects that are currently a part of an active
        cycle or cycles that are active in an workflow.

    Returns:
      Lowest state of the list of objects, ordered from least done to complete.
      This function does not check the Overdue states. if any object is Overdue
      the result of thi function will not be correct.
    """
    priority_states = OrderedDict([
        # The first True state will be returned
        ("InProgress", False),
        ("Finished", False),
        ("Assigned", False),
        ("Verified", False),
        (None, True),
    ])

    for obj in current_objects:
      status = obj.status or "Assigned"
      priority_states[status] = True

    return next(k for k, v in priority_states.items() if v)

  @classmethod
  def get_object_state(cls, objs):
    """Get lowest state of an object

    Get the lowest possible state of the tasks relevant to one object. States
    are scanned in order: Overdue, InProgress, Finished, Assigned, Verified.

    Args:
      objs: A list of cycle task group objects, which should all be mapped to
        the same object.

    Returns:
      Name of the lowest state of all active cycle tasks that relate to the
      given objects.
    """
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
    """Get lowest state of a workflow

    Get the lowest possible state of the tasks relevant to a given workflow.
    States are scanned in order: Overdue, InProgress, Finished, Assigned,
    Verified.

    Args:
      cycles: list of cycles belonging to a single workflow.

    Returns:
      Name of the lowest workflow state, if there are any active cycles.
      Otherwise it returns None.
    """
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
Workflow.__bases__ = (object_folder.Folderable,) + Workflow.__bases__
Workflow.late_init_folderable()
