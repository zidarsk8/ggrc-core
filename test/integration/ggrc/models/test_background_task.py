# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for background_task model."""
from integration.ggrc import api_helper
from integration.ggrc import TestCase
from integration.ggrc.generator import Generator
from integration.ggrc.generator import ObjectGenerator


class TestBackgroundTask(TestCase):
  """Tests for background task model."""

  def setUp(self):
    """setUp, nothing else to add."""
    super(TestBackgroundTask, self).setUp()
    self.api = api_helper.Api()

  def test_bg_task_from_post(self):
    """Test filtering of GET response for BackgroundTask"""
    from ggrc.models import all_models

    control_dict = {
        "control": {
            "title": "Control title",
            "context": None,
        },
    }
    response = self.api.send_request(
        self.api.client.post,
        all_models.Control,
        control_dict,
        {"X-GGRC-BackgroundTask": "true"},
    )
    self.assertEqual(response.status_code, 201)
    bg_tasks = all_models.BackgroundTask.query.all()
    self.assertEqual(len(bg_tasks), 1)

    content = self.api.client.get("/api/background_tasks")
    self.assert200(content)
    bg_tasks_content = \
        content.json['background_tasks_collection']['background_tasks']
    self.assertEqual(len(bg_tasks_content), 1)
    self.assertEqual(set(bg_tasks_content[0].keys()),
                     {"id", "selfLink", "status", "type"})

    task_id = bg_tasks[0].id
    content = self.api.client.get("/api/background_tasks/{}".format(task_id))
    self.assert200(content)
    bg_task_content = \
        content.json['background_task']
    self.assertEqual(set(bg_task_content.keys()),
                     {"id", "selfLink", "status", "type"})


class TestPermissions(TestCase):
  """Test permissions for background tasks"""

  def setUp(self):
    super(TestPermissions, self).setUp()
    self.generator = Generator()
    self.api = api_helper.Api()
    self.object_generator = ObjectGenerator()
    self.init_users()

  def init_users(self):
    """ Init users needed by the test cases """
    users = [("reader", "Reader"),
             ("admin", "Administrator"),
             ("creator", "Creator")]
    self.users = {}
    for (name, role) in users:
      _, user = self.object_generator.generate_person(
          data={"name": name}, user_role=role)
      self.users[name] = user

  def test_bg_tasks_access(self):
    """Only admin can use admin requirement"""
    from ggrc.models import all_models

    control_dict = {
        "control": {
            "title": "Control title",
            "context": None,
        },
    }
    response = self.api.send_request(
        self.api.client.post,
        all_models.Control,
        control_dict,
        {"X-GGRC-BackgroundTask": "true"},
    )
    self.assertEqual(response.status_code, 201)

    for role in ("reader", "creator", "admin"):
      self.api.set_user(self.users[role])
      content = self.api.client.get("/api/background_tasks")
      self.assert200(content)
      bg_tasks_content = \
          content.json['background_tasks_collection']['background_tasks']
      self.assertEqual(len(bg_tasks_content), 1)
