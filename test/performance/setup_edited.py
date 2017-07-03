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

    self._edit_assessments()
    self._edit_assessment_states()

    sys.exit(0)

  def _edit_assessments(self):
    for assessment in self.objects["Assessment"][:30]:
      self.update_object(assessment)

  def _edit_assessment_states(self):
    count = len(self.objects["Assessment"])
    edit_count = count / 3
    states = [
        "Ready for Review",
        "Completed",
    ]
    assessments = generator.random_objects(
        "Assessment",
        edit_count,
        self.objects
    )
    for assessment in assessments[:30]:
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
