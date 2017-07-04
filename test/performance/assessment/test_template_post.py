# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Base module for locust setup tasks."""

import random

import locust

from performance import base

random.seed(1)


class AssessmentTemplateTaskSet(base.BaseTaskSet):
  """Base class for locust setup tasks."""

  GAE = True
  _assessment_template_models = [
      "Control",
      "Objective",
      "Facility",
      "Regulation",
      "OrgGroup",
      "Market",
  ]

  @locust.task(1)
  def one_cad_prefix(self):
    self.create_at(
        audits=[random.choice(self.objects["Audit"])],
        at_models=[random.choice(self._assessment_template_models)],
        prefixes=["1"],
        name="cad 6",
    )

  @locust.task(1)
  def two_cad_prefixes(self):
    self.create_at(
        audits=[random.choice(self.objects["Audit"])],
        at_models=[random.choice(self._assessment_template_models)],
        prefixes=["1", "2"],
        name="cad 12",
    )

  @locust.task(1)
  def four_cad_prefixes(self):
    self.create_at(
        audits=[random.choice(self.objects["Audit"])],
        at_models=[random.choice(self._assessment_template_models)],
        prefixes=["1", "2", "3", "4"],
        name="cad 24",
    )

  @locust.task(1)
  def eight_cad_prefixes(self):
    self.create_at(
        audits=[random.choice(self.objects["Audit"])],
        at_models=[random.choice(self._assessment_template_models)],
        prefixes=["1", "2", "3", "4", "5", "6", "7", "8"],
        name="cad 48",
    )


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AssessmentTemplateTaskSet
  min_wait = 100
  max_wait = 200
