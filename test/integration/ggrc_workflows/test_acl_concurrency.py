# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for workflow cycle state propagation between tasks and task groups"""

# pylint: disable=invalid-name
import Queue
from threading import Thread

from ggrc.access_control import role
from ggrc.models import all_models
from integration.ggrc import TestCase
from integration.ggrc_workflows.generator import WorkflowsGenerator
from integration.ggrc.api_helper import Api
from integration.ggrc.generator import ObjectGenerator
from integration.ggrc.models import factories


class TestWorkflowCycleStatePropagation(TestCase):
  """Test case for cycle task to cycle task group status propagation"""

  def setUp(self):
    super(TestWorkflowCycleStatePropagation, self).setUp()
    self.api = Api()
    self.generator = WorkflowsGenerator()
    self.object_generator = ObjectGenerator()

    self.weekly_wf = {
        "title": "weekly thingy",
        "description": "start this many a time",
        "unit": "week",
        "repeat_every": 1,
        "task_groups": [{
            "title": "weekly task group",
        }]
    }

  def test_async_request_state_transitions(self):
    """Test asynchronous transitions"""

    tgt_roles = role.get_ac_roles_for("TaskGroupTask")

    queue = Queue.Queue()
    _, wf = self.generator.generate_workflow(self.weekly_wf)
    context_id = wf.context.id

    tg_id = all_models.TaskGroup.query.first().id
    obj_count = 5

    with factories.single_commit():
      person_id = factories.PersonFactory().id
      controls = [factories.ControlFactory().id for i in range(obj_count)]

    def create_tgo(context_id, tg_id, control_id):
      queue.put(self.api.post(
          all_models.TaskGroupObject,
          [{
              "task_group_object": {
                  "context": {
                      "id": context_id,
                      "type": "Context"
                  },
                  "task_group": {
                      "id": tg_id,
                      "type": "TaskGroup"
                  },
                  "object": {
                      "id": control_id,
                      "type": "Control"
                  },
              },
          }]
      ))

    def create_tgt(context_id, tg_id):
      queue.put(self.api.post(
          all_models.TaskGroupTask,
          [{
              "task_group_task": {
                  "response_options": [],
                  "start_date":"2018-03-29",
                  "end_date":"2018-04-05T00:23:41.000Z",
                  "minStartDate":"2018-03-29T00:23:41.576Z",
                  "access_control_list":[{
                      "ac_role_id": tgt_roles["Task Assignees"].id,
                      "person": {"id": person_id, "type": "Person"}
                  }],
                  "contact": {"id": person_id, "type": "Person"},
                  "task_group": {"id": tg_id, "type": "TaskGroup"},
                  "context": {"id": context_id, "type": "Context"},
                  "sort_index": "1",
                  "modal_title": "Create New Task",
                  "title": "Dummy task title",
                  "task_type": "text",
                  "description": "",
                  "slug": "",
              }
          }]
      ))

    # Move all tasks to In Progress
    threads = []
    for control_id in controls:
      threads.append(Thread(
          target=create_tgo,
          args=(context_id, tg_id, control_id)
      ))
      threads.append(Thread(
          target=create_tgt,
          args=(context_id, tg_id)
      ))

    for t in threads:
      t.start()
    for t in threads:
      t.join()

    while not queue.empty():
      response = queue.get()
      self.assert200(response, response.data)
