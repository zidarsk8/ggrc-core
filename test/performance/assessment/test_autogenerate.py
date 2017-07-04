# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Base module for locust setup tasks."""

import random

import locust

from performance import base
from performance import generator

random.seed(1)


class AutogenerateAssessmentTaskSet(base.BaseTaskSet):
  """Base class for locust setup tasks."""

  def set_up(self):
    super(AutogenerateAssessmentTaskSet, self).set_up()
    self.get_objects("Relationship")
    self.get_objects("AssessmentTemplate")
    self.get_objects("Snapshot")

  def _genarate(self, count):
    audits = generator.random_objects("Audit", 1, self.objects)
    self.autogenerate_assessments(
        audits=audits,
        template_models=["Control"],
        count=count,
    )

  @locust.task(1)
  def test_generate_10(self):
    self._genarate(10)

  @locust.task(1)
  def test_generate_100(self):
    self._genarate(100)

  @locust.task(1)
  def test_generate_1000(self):
    self._genarate(1000)


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AutogenerateAssessmentTaskSet
  min_wait = 100
  max_wait = 200
