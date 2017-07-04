# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for locust update tasks."""

import random
import logging

import locust

from performance import base
from performance import generator

random.seed(1)

logger = logging.getLogger()


class AssessmentPUT(base.BaseTaskSet):
  """Tests for object update operation."""

  @locust.task(1)
  def test_put(self):
    states = [
        "In Progress",
        "Ready for Review",
        "Completed",
    ]
    assessment = generator.random_object("Assessment", self.objects)
    state = random.choice(states)
    self.set_random_user(roles=["Administrator", "Editor"])
    self.update_object(assessment)
    self.update_object(assessment, changes={
        "status": state,
    })
    logger.debug("\nAssessment: {}\n - state: {}".format(assessment, state))


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AssessmentPUT
  min_wait = 100
  max_wait = 200
