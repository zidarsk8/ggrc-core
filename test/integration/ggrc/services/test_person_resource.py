# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for /api/people endpoints."""

from datetime import date

import ddt
from freezegun import freeze_time

from ggrc.models import all_models
from ggrc.utils import create_stub

from integration.ggrc.models import factories
from integration.ggrc.services import TestCase
from integration.ggrc_workflows.generator import WorkflowsGenerator


@ddt.ddt
class TestPersonResource(TestCase):
  """Tests for special people api endpoints."""

  def setUp(self):
    super(TestPersonResource, self).setUp()
    self.client.get("/login")

  @ddt.data(
      (True, [
          ("task 1", "Finished", 3, True),
          ("task 1", "Verified", 2, True),
          ("task 2", "Declined", 2, True),
          ("task 2", "Verified", 1, False),
          ("task 2", "Finished", 2, True),
          ("task 3", "Verified", 1, True),
          ("task 2", "Verified", 0, False),
      ]),
      (False, [
          ("task 1", "Finished", 2, True),
          ("task 2", "InProgress", 2, True),
          ("task 2", "Finished", 1, False),
          ("task 3", "Finished", 0, False),
      ]),
  )
  @ddt.unpack
  def test_task_count(self, is_verification_needed, transitions):
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

    wf_generator = WorkflowsGenerator()

    user = all_models.Person.query.first()
    dummy_user = factories.PersonFactory()
    user_id = user.id
    one_time_workflow = {
        "title": "Person resource test workflow",
        "notify_on_change": True,
        "description": "some test workflow",
        "owners": [create_stub(user)],
        "is_verification_needed": is_verification_needed,
        "task_groups": [{
            "title": "one time task group",
            "contact": create_stub(user),
            "task_group_tasks": [{
                "title": "task 1",
                "description": "some task",
                "contact": create_stub(user),
                "start_date": date(2017, 5, 5),
                "end_date": date(2017, 8, 15),
            }, {
                "title": "task 2",
                "description": "some task 3",
                "contact": create_stub(user),
                "start_date": date(2017, 5, 5),
                "end_date": date(2017, 9, 16),
            }, {
                "title": "task 3",
                "description": "some task 4",
                "contact": create_stub(user),
                "start_date": date(2017, 6, 5),
                "end_date": date(2017, 11, 16),
            }, {
                "title": "dummy task 4",  # task should not counted
                "description": "some task 4",
                "contact": create_stub(dummy_user),
                "start_date": date(2017, 6, 5),
                "end_date": date(2017, 11, 17),
            }, {
                "title": "dummy task 5",  # task should not counted
                "description": "some task 4",
                "contact": create_stub(dummy_user),
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
                "contact": create_stub(user),
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

      for task, status, count, overdue in transitions:
        print task, status, count, overdue
        wf_generator.modify_object(tasks[task], data={"status": status})
        response = self.client.get("/api/people/{}/task_count".format(user_id))
        self.assertEqual(
            response.json,
            {"open_task_count": count, "has_overdue": overdue}
        )

  def test_task_count_multiple_wfs(self):
    """Test task count with both verified and non verified workflows.

    This checks task counts with 4 tasks
        2017, 8, 15  - verification needed
        2017, 11, 18  - verification needed
        2017, 8, 15  - No verification needed
        2017, 11, 18  - No verification needed
    """

    wf_generator = WorkflowsGenerator()
    user = all_models.Person.query.first()
    user_id = user.id
    workflow_template = {
        "title": "verified workflow",
        "owners": [create_stub(user)],
        "is_verification_needed": True,
        "task_groups": [{
            "title": "one time task group",
            "contact": create_stub(user),
            "task_group_tasks": [{
                "title": "task 1",
                "description": "some task",
                "contact": create_stub(user),
                "start_date": date(2017, 5, 5),
                "end_date": date(2017, 8, 15),
            }, {
                "title": "dummy task 5",
                "description": "some task 4",
                "contact": create_stub(user),
                "start_date": date(2017, 6, 5),
                "end_date": date(2017, 11, 18),
            }],
            "task_group_objects": []
        }]
    }

    with freeze_time("2017-10-16 05:09:10"):
      self.client.get("/login")
      verified_workflow = workflow_template.copy()
      verified_workflow["is_verification_needed"] = True
      _, workflow = wf_generator.generate_workflow(verified_workflow)
      _, cycle = wf_generator.generate_cycle(workflow)
      verified_tasks = {
          task.title: task
          for task in cycle.cycle_task_group_object_tasks
      }
      _, workflow = wf_generator.activate_workflow(workflow)

      non_verified_workflow = workflow_template.copy()
      non_verified_workflow["is_verification_needed"] = False
      _, workflow = wf_generator.generate_workflow(non_verified_workflow)
      _, cycle = wf_generator.generate_cycle(workflow)
      non_verified_tasks = {
          task.title: task
          for task in cycle.cycle_task_group_object_tasks
      }
      _, workflow = wf_generator.activate_workflow(workflow)

    with freeze_time("2017-7-16 07:09:10"):
      self.client.get("/login")
      response = self.client.get("/api/people/{}/task_count".format(user_id))
      self.assertEqual(
          response.json,
          {"open_task_count": 4, "has_overdue": False}
      )

    with freeze_time("2017-10-16 08:09:10"):
      self.client.get("/login")
      response = self.client.get("/api/people/{}/task_count".format(user_id))
      self.assertEqual(
          response.json,
          {"open_task_count": 4, "has_overdue": True}
      )

      # transition 1, task that needs verification goes to finished state. This
      # transition should not change anything
      wf_generator.modify_object(
          verified_tasks["task 1"],
          data={"status": "Finished"}
      )
      response = self.client.get("/api/people/{}/task_count".format(user_id))
      self.assertEqual(
          response.json,
          {"open_task_count": 4, "has_overdue": True}
      )

      # transition 2, task that needs verification goes to verified state. This
      # transition should reduce task count.
      wf_generator.modify_object(
          verified_tasks["task 1"],
          data={"status": "Verified"}
      )
      response = self.client.get("/api/people/{}/task_count".format(user_id))
      self.assertEqual(
          response.json,
          {"open_task_count": 3, "has_overdue": True}
      )

      # transition 3, task that does not need verification goes into Finished
      # state. This transition should reduce task count and remove all overdue
      # tasks
      wf_generator.modify_object(
          non_verified_tasks["task 1"],
          data={"status": "Finished"}
      )
      response = self.client.get("/api/people/{}/task_count".format(user_id))
      self.assertEqual(
          response.json,
          {"open_task_count": 2, "has_overdue": False}
      )
