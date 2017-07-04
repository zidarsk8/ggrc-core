# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Base module for locust setup tasks."""

import random

import locust

from performance import base

random.seed(1)


class AutogenerateAssessmentTaskSet(base.BaseTaskSet):
  """Base class for locust setup tasks."""

  @locust.task(1)
  def test_autogenerate_assessments(self):
    self.autogenerate_assessments(
        audits=self.objects["Audit"][:1],
        template_models=["Control"],
        count=10,
    )


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AutogenerateAssessmentTaskSet
  min_wait = 10000
  max_wait = 10000
