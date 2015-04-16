# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import random
from tests.ggrc import TestCase
from freezegun import freeze_time

import os
from ggrc import notification
from ggrc.models import Person
from tests.ggrc_workflows.generator import WorkflowsGenerator
from tests.ggrc.api_helper import Api
from tests.ggrc.generator import GgrcGenerator


if os.environ.get('TRAVIS', False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestBasicWorkflowActions(TestCase):

  def setUp(self):
    self.api = Api()
    self.generator = WorkflowsGenerator()
    self.ggrc_generator = GgrcGenerator()

    self.create_test_cases()

  def tearDown(self):
    pass

  def test_cycle_starts_in_less_than_X_days(self):

    with freeze_time("2015-02-01"):
      _, wf = self.generator.generate_workflow(self.quarterly_wf_1)
      response, wf = self.generator.activate_workflow(wf)

      self.assert200(response)

      assignee = Person.query.get(self.assignee.id)

    with freeze_time("2015-01-01"):
      notifications = notification.get_todays_notifications()
      self.assertNotIn(assignee.email, notifications)

    with freeze_time("2015-01-29"):
      notifications = notification.get_todays_notifications()
      self.assertIn(assignee.email, notifications)

    with freeze_time("2015-02-01"):
      notifications = notification.get_todays_notifications()
      self.assertIn(assignee.email, notifications)

  def create_test_cases(self):
    _, self.assignee = self.ggrc_generator.generate_person(
      data={"name": "hello world", "email": "hello@world.com"},
      user_role="gGRC Admin")

    self.quarterly_wf_1 = {
        "title": "quarterly wf 1",
        "description": "",
        "frequency": "quarterly",
        "task_groups": [{
            "title": "tg_1",
            "task_group_tasks": [{
                "contact": {
                    "href": "/api/people/%d" % self.assignee.id,
                    "id": self.assignee.id,
                    "type": "Person"
                },
                "description": self.generator.random_str(100),
                "relative_start_day": 5,
                "relative_start_month": 2,
                "relative_end_day": 25,
                "relative_end_month": 2,
            },
            ],
        },
        ]
    }

    self.all_workflows = [
        self.quarterly_wf_1,
    ]
