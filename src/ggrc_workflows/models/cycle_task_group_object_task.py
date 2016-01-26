# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

"""Module containing Cycle tasks.
"""

from sqlalchemy import orm
from sqlalchemy import or_

from ggrc import db
from ggrc.models import all_models
from ggrc.models.mixins import Base
from ggrc.models.mixins import Described
from ggrc.models.mixins import Slugged
from ggrc.models.mixins import Stateful
from ggrc.models.mixins import Timeboxed
from ggrc.models.mixins import Titled
from ggrc.models.mixins import WithContact
from ggrc.models.reflection import PublishOnly
from ggrc.models.types import JsonType
from ggrc_workflows.models.cycle import Cycle
from ggrc_workflows.models.cycle_task_group import CycleTaskGroup
from ggrc_workflows.models.cycle_task_group_object import CycleTaskGroupObject


class CycleTaskGroupObjectTask(
        WithContact, Stateful, Slugged, Timeboxed,
        Described, Titled, Base, db.Model):
  """Cycle task model
  """
  __tablename__ = 'cycle_task_group_object_tasks'
  _title_uniqueness = False

  @classmethod
  def generate_slug_prefix_for(cls, obj):
    return "CYCLETASK"

  VALID_STATES = (None, 'InProgress', 'Assigned',
                  'Finished', 'Declined', 'Verified')

  cycle_id = db.Column(
      db.Integer, db.ForeignKey('cycles.id'), nullable=False)
  cycle_task_group_id = db.Column(
      db.Integer, db.ForeignKey('cycle_task_groups.id'), nullable=False)
  cycle_task_group_object_id = db.Column(
      db.Integer, db.ForeignKey('cycle_task_group_objects.id'), nullable=True)
  task_group_task_id = db.Column(
      db.Integer, db.ForeignKey('task_group_tasks.id'), nullable=False)
  task_group_task = db.relationship(
      "TaskGroupTask",
      foreign_keys="CycleTaskGroupObjectTask.task_group_task_id"
  )
  task_type = db.Column(
      db.String(length=250), nullable=False)
  response_options = db.Column(
      JsonType(), nullable=False, default='[]')
  selected_response_options = db.Column(
      JsonType(), nullable=False, default='[]')

  sort_index = db.Column(
      db.String(length=250), default="", nullable=False)

  finished_date = db.Column(db.DateTime)
  verified_date = db.Column(db.DateTime)

  _publish_attrs = [
      'cycle',
      'cycle_task_group_object',
      'cycle_task_group',
      'task_group_task',
      'cycle_task_entries',
      'sort_index',
      'task_type',
      'response_options',
      'selected_response_options',
      PublishOnly('finished_date'),
      PublishOnly('verified_date')
  ]

  default_description = "<ol>"\
                        + "<li>Expand the object review task.</li>"\
                        + "<li>Click on the Object to be reviewed.</li>"\
                        + "<li>Review the object in the Info tab.</li>"\
                        + "<li>Click \"Approve\" to approve the object.</li>"\
                        + "<li>Click \"Decline\" to decline the object.</li>"\
                        + "</ol>"

  _aliases = {
      "title": "Summary",
      "description": "Task Details",
      "contact": {
          "display_name": "Assignee",
          "mandatory": True,
          "filter_by": "_filter_by_contact",
      },
      "secondary_contact": None,
      "start_date": "Start Date",
      "end_date": "End Date",
      "finished_date": "Actual Finish Date",
      "verified_date": "Actual Verified Date",
      "cycle": {
          "display_name": "Cycle",
          "filter_by": "_filter_by_cycle",
      },
      "cycle_task_group": {
          "display_name": "Task Group",
          "mandatory": True,
          "filter_by": "_filter_by_cycle_task_group",
      },
      "task_type": {
          "display_name": "Task Type",
          "mandatory": True,
      },
      "cycle_object": {
          "display_name": "Cycle Object",
          "filter_by": "_filter_by_cycle_object",
      },
  }

  @classmethod
  def _filter_by_cycle(cls, predicate):
    """Get query that filters cycle tasks by related cycles.

    Args:
      predicate: lambda function that excepts a single parameter and returns
      true of false.

    Returns:
      An sqlalchemy query that evaluates to true or false and can be used in
      filtering cycle tasks by related cycles.
    """
    return Cycle.query.filter(
        (Cycle.id == cls.cycle_id) &
        (predicate(Cycle.slug) | predicate(Cycle.title))
    ).exists()

  @classmethod
  def _filter_by_cycle_task_group(cls, predicate):
    """Get query that filters cycle tasks by related cycle task groups.

    Args:
      predicate: lambda function that excepts a single parameter and returns
      true of false.

    Returns:
      An sqlalchemy query that evaluates to true or false and can be used in
      filtering cycle tasks by related cycle task groups.
    """
    return CycleTaskGroup.query.filter(
        (CycleTaskGroup.id == cls.cycle_id) &
        (predicate(CycleTaskGroup.slug) | predicate(CycleTaskGroup.title))
    ).exists()

  @classmethod
  def _filter_by_cycle_object(cls, predicate):
    """Get query that filters cycle tasks by mapped objects.

    Args:
      predicate: lambda function that excepts a single parameter and returns
      true of false.

    Returns:
      An sqlalchemy query that evaluates to true or false and can be used in
      filtering cycle tasks by objects mapped to them.
    """
    parts = []
    for model_name in all_models.__all__:
      model = getattr(all_models, model_name)
      query = getattr(model, "query", None)
      field = getattr(model, "slug", getattr(model, "email", None))
      if query is None or field is None or not hasattr(model, "id"):
        continue
      parts.append(query.filter(
          (CycleTaskGroupObject.object_type == model_name) &
          (model.id == CycleTaskGroupObject.object_id) &
          predicate(field)
      ).exists())
    return CycleTaskGroupObject.query.filter(
        (CycleTaskGroupObject.id == cls.cycle_task_group_object_id) &
        or_(*parts)
    ).exists()

  @classmethod
  def eager_query(cls):
    """Add cycle task entries to cycle task eager query

    This function add cycle_task_entries as a join option when fetching cycles
    tasks, and makes sure that with one query we fetch all cycle task related
    data needed for generating cycle taks json for a response.

    Returns:
      a query object with cycle_task_entries added to joined load options.
    """
    query = super(CycleTaskGroupObjectTask, cls).eager_query()
    return query.options(
        orm.joinedload('cycle_task_entries'),
    )
