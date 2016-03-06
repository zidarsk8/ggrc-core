# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jost@reciprocitylabs.com
# Maintained By: jost@reciprocitylabs.com

"""Unit Tests for Workflow model and WorkflowState mixin
"""

from datetime import date
import unittest

from freezegun import freeze_time

from ggrc_workflows.models import cycle_task_group_object_task as cycle_task
from ggrc_workflows.models import cycle
from ggrc_workflows.models import workflow


class TestWorkflowState(unittest.TestCase):

  def test_get_state(self):

    scenario_list = [
        {
            "task_states": ["Assigned", "Assigned", "Assigned"],
            "result": "Assigned"
        },
        {
            "task_states": ["InProgress", "Assigned", "Assigned"],
            "result": "InProgress"
        },
        {
            "task_states": ["Finished", "Assigned", "Assigned"],
            "result": "InProgress"
        },
        {
            "task_states": ["Verified", "Assigned", "Assigned"],
            "result": "InProgress"
        },
        {
            "task_states": ["InProgress", "InProgress", "InProgress"],
            "result": "InProgress"
        },
        {
            "task_states": ["Finished", "InProgress", "Assigned"],
            "result": "InProgress"
        },
        {
            "task_states": ["Finished", "Declined", "Assigned"],
            "result": "InProgress"
        },
        {
            "task_states": ["Finished", "Finished", "Finished"],
            "result": "Finished"
        },
        {
            "task_states": ["Verified", "Finished", "Finished"],
            "result": "Finished"
        },
        {
            "task_states": ["Verified", "Verified", "Verified"],
            "result": "Verified"
        },
    ]

    for scenario in scenario_list:
      tasks_on_object = []
      for task_status in scenario["task_states"]:
        tasks_on_object.append(
            cycle_task.CycleTaskGroupObjectTask(status=task_status),
        )
      self.assertEqual(scenario["result"], workflow
                       .WorkflowState._get_state(tasks_on_object))

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
      self.assertEqual("Overdue", workflow
                       .WorkflowState.get_object_state(tasks_on_object))
