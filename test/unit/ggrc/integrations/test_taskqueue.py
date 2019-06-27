# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Unit tests for cloud taskqueue api."""

import unittest

import mock

from ggrc import db
from ggrc.app import app
from ggrc.cloud_api.task_queue import get_app_engine_tasks
from ggrc.models import all_models

from integration.ggrc.models import factories


class TestTaskQueueAPI(unittest.TestCase):
  """Test class for TaskQueue api."""

  def setUp(self):
    super(TestTaskQueueAPI, self).setUp()

    self.cloud_tasks = {
        "tasks": [
            {
                "scheduleTime": "2018-11-20T10:43:52.011503Z",
                "appEngineHttpRequest": {
                    "httpMethod": "POST",
                    "appEngineRouting": {
                        "host": "example.com"
                    },
                    "relativeUri": "/_background_tasks/reindex",
                    "headers": {
                        "Origin": "https://example.appspot.com",
                        "Content-Length": "13",
                        "Accept-Language": "en-US,en;q=0.9",
                        "X-Usertimezoneoffset": "180",
                        "Accept": "*/*",
                        "Referer": "https://example.com/admin/reindex",
                        "Cookie": "some cookie",
                        "X-Task-Id": "29764",
                        "X-Cloud-Trace-Context": "123",
                        "X-Requested-With": "XMLHttpRequest",
                        "User-Agent": "Mozilla/5.0",
                        "content-type": "application/x-www-form-urlencoded"
                    }
                },
                "view": "BASIC",
                "name": "projects/ggrc-perf/locations/us-central1/queues/"
                        "ggrc/tasks/reindex1542710631_29764",
                "createTime": "2018-11-20T10:43:52Z"
            }
        ]
    }

  def test_taskqueue(self):
    """Test if task name correctly grabbed from cloud task list."""
    with mock.patch(
        "ggrc.cloud_api.task_queue.request_taskqueue_data",
        return_value=self.cloud_tasks
    ):
      tasks = get_app_engine_tasks("ggrc")
    self.assertEqual(tasks, ["reindex1542710631_29764"])


class TestBackgroundTaskQueue(unittest.TestCase):
  """Test class for background tasks in queue."""

  def setUp(self):
    super(TestBackgroundTaskQueue, self).setUp()

    all_models.BackgroundTask.query.delete()
    db.session.commit()

  def test_bg_error_task(self):
    """Test error BackgroundTask for success response."""
    from ggrc.views import create_missing_revisions

    with mock.patch(
        "ggrc.views.app.make_response",
        return_value=app.make_response(
            ("error", 500, [("Content-Type", "text/html")])
        )
    ):
      with mock.patch("ggrc.utils.revisions.do_missing_revisions"):
        bg_task = factories.BackgroundTaskFactory(name="test_error_task_queue")
        response = create_missing_revisions(bg_task)
        self.assertEqual(response.status_code, 200)
        db.session.delete(bg_task)
        db.session.commit()

  def test_bg_success_task(self):
    """Test success BackgroundTask for success response."""
    from ggrc.views import create_missing_revisions

    with mock.patch("ggrc.utils.revisions.do_missing_revisions"):
      bg_task = factories.BackgroundTaskFactory(name="test_success_task_queue")
      response = create_missing_revisions(bg_task)
      self.assertEqual(response.status_code, 200)
      db.session.delete(bg_task)
      db.session.commit()
