# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for locust read tasks."""

import logging
import random

import locust

from performance import base
from performance import generator
from performance import models

random.seed(1)


logger = logging.getLogger()


class AssessmentGET(base.BaseTaskSet):
  """Tests for assessment read operations."""

  @locust.task(1)
  def get_assessments_view(self):
    self.set_random_user(roles=models.GLOBAL_ROLES)
    self.client.get(
        "/assessments_view",
        headers=self.headers_text,
        name="{} /assessments_view".format(self.role),
    )

  @locust.task(1)
  def test_get_single(self):
    self.set_random_user(roles=models.GLOBAL_ROLES)
    assessment = generator.random_object("Assessment", self.objects)
    if assessment:
      self.get_from_slug(assessment)

  def _test_get_multiple(self, count):
    self.set_random_user(roles=models.GLOBAL_ROLES)
    assessments = generator.random_objects("Assessment", count,  self.objects)
    ids = [assessment["id"] for assessment in assessments]
    self.get_multiple("Assessment", ids)

  @locust.task(1)
  def test_get_multiple_10(self):
    self._test_get_multiple(10)

  @locust.task(1)
  def test_get_multiple_100(self):
    self._test_get_multiple(100)

  @locust.task(1)
  def test_get_multiple_1000(self):
    self._test_get_multiple(1000)


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AssessmentGET
  min_wait = 100
  max_wait = 100
