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

    states = [
        "In Progress",
        "Ready for Review",
        "Completed",
    ]
    count = len(self.objects["Assessment"])
    edit_count = count - random.randint(count / 5, count / 2)
    assessments = generator.random_objects(
        "Assessment",
        edit_count,
        self.objects
    )
    logger.debug("Updating {} assessments of {}.".format(edit_count, count))
    for assessment in assessments:
      state = random.choice(states)
      self.update_object(assessment)
      self.update_object(assessment, changes={
          "status": state,
      })
    sys.exit(0)


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = SetUpAssessments
  min_wait = 2000
  max_wait = 2000
