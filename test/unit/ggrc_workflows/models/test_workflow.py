# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Unit Tests for Workflow model and WorkflowState mixin
"""

import ddt
from datetime import date
import unittest

from freezegun import freeze_time

from ggrc_workflows.models import cycle_task_group_object_task as cycle_task
from ggrc_workflows.models import cycle
from ggrc_workflows.models import workflow


@ddt.ddt
class TestWorkflowState(unittest.TestCase):

  @ddt.data(
      (["Assigned", "Assigned", "Assigned"], "Assigned"),
      ([None, None, None], "Assigned"),
      (["InProgress", "Assigned", "Assigned"], "InProgress"),
      (["Finished", "Assigned", "Assigned"], "InProgress"),
      (["Verified", "Assigned", "Assigned"], "InProgress"),
      (["InProgress", "InProgress", "InProgress"], "InProgress"),
      (["Finished", "InProgress", "Assigned"], "InProgress"),
      (["Finished", "Declined", "Assigned"], "InProgress"),
      (["Finished", "Finished", "Finished"], "Finished"),
      (["Verified", "Finished", "Finished"], "Finished"),
      (["Verified", "Verified", "Verified"], "Verified"),
      (["Declined", "Declined", "Declined"], "InProgress"),
      ([], None),
  )
  @ddt.unpack
  def test_get_state(self, task_states, result):
    self.assertEqual(
        result,
        workflow.WorkflowState._get_state([
            cycle_task.CycleTaskGroupObjectTask(status=s) for s in task_states
        ])
    )

  def test_get_object_state(self):

    tasks_on_object = [
        cycle_task.CycleTaskGroupObjectTask(
            end_date=date(2015, 2, 1),
            cycle=cycle.Cycle(is_current=True)
        ),
        cycle_task.CycleTaskGroupObjectTask(
            end_date=date(2015, 1, 10),
            cycle=cycle.Cycle(is_current=True)
        ),
    ]
    with freeze_time("2015-02-01 13:39:20"):
      self.assertEqual(
          "Overdue", workflow.WorkflowState.get_object_state(tasks_on_object)
      )
