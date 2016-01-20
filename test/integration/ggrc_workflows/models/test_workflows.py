# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Tests for Workflow model and WorkflowState mixin
"""

import collections
from datetime import date
from freezegun import freeze_time
from integration import ggrc

from ggrc.models import all_models
from ggrc_workflows import models


class PreviousWorkflowState(object):

  """Copy of the original WorkflowState mixin

  This class is used as a base for comparing the refactored workflow_state
  comuputed property.
  """

  @classmethod
  def get_state(cls, objs):
    """Original get_state function.
    """
    priority_states = collections.OrderedDict([
        # The first True state will be returned
        ("Overdue", False),
        ("InProgress", False),
        ("Finished", False),
        ("Assigned", False),
        ("Verified", False)
    ])

    for obj in objs:
      today = date.today()
      cycle = obj if isinstance(obj, models.Cycle) else obj.cycle
      if not cycle.is_current:
        continue
      for task in obj.cycle_task_group_object_tasks:
        if (task.end_date and task.end_date <= today and
                task.status != "Verified"):
          priority_states["Overdue"] = True
      if not obj.status:
        priority_states["Assigned"] = True
      priority_states[obj.status] = True

    for state in priority_states.keys():
      if priority_states[state]:
        return state

    return None

  @classmethod
  def workflow_state(cls, obj):
    """Helper function for workflow_state property.deleter

    Previous workflow state was called with different arguments depending on
    the source class. This is a helper to make sure we always call the
    get_state function with the correct parameters.
    """
    if isinstance(obj, models.Workflow):
      return cls.get_state(obj.cycles)
    else:
      return cls.get_state(obj.cycle_task_group_objects)


class TestWorkflowState(ggrc.TestCase):

  """Test class for workflow state refactor.
  """

  def setUp(self):
    """Set up phase for tests

    This function overrides the clearing of the database before each test is
    run. This is used so users can run a single test in this class with a
    prepopulated database.
    """
    pass

  def test_get_state(self):
    """Compare the refactored workflow_state with the old one.

    This test is meant to be run on its own with a prepopulated database. It
    checks all object states and compares them with states that were returned
    beforet the refactor.
    """

    workflow_models = [model for model in all_models.all_models if
                       hasattr(model, "workflow_state")]

    dates = [
        "2016-01-19 20:39:20",
        "2015-11-17 16:39:20",
        "2016-01-29 22:39:20",
        "2015-12-02 18:39:20",
    ]
    for date_string in dates:
      with freeze_time(date_string):
        for model in workflow_models:
          # if model.__name__ != "Program":
          #   continue
          all_objects = model.query.all()
          print len(all_objects)
          for obj in all_objects:
            self.assertEqual(
                PreviousWorkflowState.workflow_state(obj),
                obj.workflow_state,
                "state missmatch: expected '{}' found '{}' for object "
                "{} - {}".format(
                    PreviousWorkflowState.workflow_state(obj),
                    obj.workflow_state,
                    obj.type,
                    obj.id
                )
            )
