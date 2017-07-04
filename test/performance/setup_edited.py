# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Base module for locust setup tasks."""

import random
import sys
import logging

import locust

from performance import base
from performance import generator

random.seed(1)

logger = logging.getLogger()


class SetUpAssessments(base.BaseTaskSet):
  """Base class for locust setup tasks."""

  def set_up(self):
    super(SetUpAssessments, self).set_up()

    count = len(self.objects["Assessment"]) / 10
    assessments = generator.random_objects("Assessment", count, self.objects)
    self._edit_assessments(assessments)
    self._edit_assessment_states(assessments[:count / 2])

    sys.exit(0)

  def _edit_assessments(self, assessments):
    for assessment in assessments:
      self.update_object(assessment)

  def _edit_assessment_states(self, assessments):
    states = [
        "Ready for Review",
        "Completed",
        "Verified",
    ]
    for assessment in assessments:
      state = random.choice(states)
      self.update_object(assessment, changes={
          "status": state,
      })


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = SetUpAssessments
  min_wait = 2000
  max_wait = 2000
