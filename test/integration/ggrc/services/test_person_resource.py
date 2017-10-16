# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for /api/people endpoints."""

from datetime import date

from freezegun import freeze_time

from ggrc.models import all_models
from ggrc.utils import create_stub

from integration.ggrc.models import factories
from integration.ggrc.services import TestCase
from integration.ggrc_workflows.generator import WorkflowsGenerator


class TestPersonResource(TestCase):
  """Tests for special people api endpoints."""

  def setUp(self):
    super(TestPersonResource, self).setUp()
    self.client.get("/login")

  def test_task_count(self):
    """Test person task counts.

    This tests checks for correct task counts
     - with inactive workflows and
     - with overdue tasks
     - without overdue tasks
     - with finished overdue tasks

    The four checks are done in a single test due to complex differences
    between tests that make ddt cumbersome and the single test also improves
    integration test performance due to slow workflow setup stage.
    """

    role_id = all_models.AccessControlRole.query.filter(
        all_models.AccessControlRole.name == "Task Assignees",
        all_models.AccessControlRole.object_type == "TaskGroupTask",
    ).one().id

    wf_generator = WorkflowsGenerator()

    user = all_models.Person.query.first()
    dummy_user = factories.PersonFactory()
    user_id = user.id
    one_time_workflow = {
        "title": "Person resource test workflow",
        "notify_on_change": True,
        "description": "some test workflow",
        "owners": [create_stub(user)],
        "task_groups": [{
            "title": "one time task group",
            "contact": create_stub(user),
            "task_group_tasks": [{
                "title": "task 1",
                "description": "some task",
                "access_control_list": [{
                    "person": create_stub(user),
                    "ac_role_id": role_id,
                }],
                "start_date": date(2017, 5, 5),
                "end_date": date(2017, 8, 15),
            }, {
                "title": "task 2",
                "description": "some task 3",
                "access_control_list": [{
                    "person": create_stub(user),
                    "ac_role_id": role_id,
                }],
                "start_date": date(2017, 5, 5),
                "end_date": date(2017, 9, 16),
            }, {
                "title": "task 3",
                "description": "some task 4",
                "access_control_list": [{
                    "person": create_stub(user),
                    "ac_role_id": role_id,
                }, {
                    "person": create_stub(dummy_user),
                    "ac_role_id": role_id,
                }],
                "start_date": date(2017, 6, 5),
                "end_date": date(2017, 11, 16),
            }, {
                "title": "dummy task 4",  # task should not counted
                "description": "some task 4",
                "access_control_list": [{
                    "person": create_stub(dummy_user),
                    "ac_role_id": role_id,
                }],
                "start_date": date(2017, 6, 5),
                "end_date": date(2017, 11, 17),
            }, {
                "title": "dummy task 5",  # task should not counted
                "description": "some task 4",
                "access_control_list": [{
                    "person": create_stub(dummy_user),
                    "ac_role_id": role_id,
                }],
                "start_date": date(2017, 6, 5),
                "end_date": date(2017, 11, 18),
            }],
            "task_group_objects": []
        }]
    }

    inactive_workflow = {
        "title": "Activated workflow with archived cycles",
        "notify_on_change": True,
        "description": "Extra test workflow",
        "owners": [create_stub(user)],
        "task_groups": [{
            "title": "Extra task group",
            "contact": create_stub(user),
            "task_group_tasks": [{
                "title": "not counted existing task",
                "description": "",
                "access_control_list": [{
                    "person": create_stub(user),
                    "ac_role_id": role_id,
                }],
                "start_date": date(2017, 5, 5),
                "end_date": date(2017, 8, 15),
            }],
            "task_group_objects": []
        }]
    }

    with freeze_time("2017-10-16 05:09:10"):
      self.client.get("/login")
      # Activate normal one time workflow
      _, workflow = wf_generator.generate_workflow(one_time_workflow)
      _, cycle = wf_generator.generate_cycle(workflow)
      tasks = {t.title: t for t in cycle.cycle_task_group_object_tasks}
      _, workflow = wf_generator.activate_workflow(workflow)

      # Activate and close the inactive workflow
      _, workflow = wf_generator.generate_workflow(inactive_workflow)
      _, cycle = wf_generator.generate_cycle(workflow)
      _, workflow = wf_generator.activate_workflow(workflow)
      wf_generator.modify_object(cycle, data={"is_current": False})

    with freeze_time("2017-7-16 07:09:10"):
      self.client.get("/login")
      response = self.client.get("/api/people/{}/task_count".format(user_id))
      self.assertEqual(
          response.json,
          {"open_task_count": 3, "has_overdue": False}
      )

    with freeze_time("2017-10-16 08:09:10"):
      self.client.get("/login")
      response = self.client.get("/api/people/{}/task_count".format(user_id))
      self.assertEqual(
          response.json,
          {"open_task_count": 3, "has_overdue": True}
      )

      wf_generator.modify_object(tasks["task 1"], data={"status": "Verified"})
      response = self.client.get("/api/people/{}/task_count".format(user_id))
      self.assertEqual(
          response.json,
          {"open_task_count": 2, "has_overdue": True}
      )

      wf_generator.modify_object(tasks["task 2"], data={"status": "Finished"})
      response = self.client.get("/api/people/{}/task_count".format(user_id))
      self.assertEqual(
          response.json,
          {"open_task_count": 2, "has_overdue": True}
      )

      wf_generator.modify_object(tasks["task 2"], data={"status": "Verified"})
      response = self.client.get("/api/people/{}/task_count".format(user_id))
      self.assertEqual(
          response.json,
          {"open_task_count": 1, "has_overdue": False}
      )
