# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for locust update tasks."""

import random

import locust

from performance import base
from performance import generator

random.seed(1)


class ObjectUpdateTests(base.BaseTaskSet):
  """Tests for object update operation."""

  @locust.task(1)
  def test_assessment_update(self):
    states = [
        "In Progress",
        "Ready for Review",
        "Completed",
    ]
    assessment = generator.random_object("Assessment", self.objects)
    self.update_object(assessment)
    self.update_object(assessment, changes={
        "state": random.choice(states),
    })

  @locust.task(1)
  def test_market_update(self):
    market = generator.random_object("Market", self.objects)
    self.update_object(market)


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = ObjectUpdateTests
  min_wait = 100
  max_wait = 200
