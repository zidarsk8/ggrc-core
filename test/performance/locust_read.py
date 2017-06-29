# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for locust read tasks."""

import random

import locust

from performance import base
from performance import models
from performance import request_templates

random.seed(1)


class AssessmentTest(base.BaseTaskSet):
  """Tests for assessment read operations."""

  @locust.task(1)
  def get_assessments_view(self):
    role = random.choice(models.GLOBAL_ROLES)
    self.set_random_user(role=role)
    self.client.get(
        "/assessments_view",
        headers=self.headers_text,
        name="{} /assessments_view".format(role),
    )

  @locust.task(1)
  def get_query_related_asssessments(self):
    statuses = [
        "Not Started",
        "In Progress",
        "Ready for Review",
        "Completed",
    ]
    role = random.choice(models.GLOBAL_ROLES)
    person = self.set_random_user(role=role)
    request_templates.assessment_related_status_query(person, statuses)
    self.client.get(
        "/assessments_view",
        headers=self.headers_text,
        name="/query rel person - {}".format(role),
    )


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AssessmentTest
  min_wait = 500
  max_wait = 1000
