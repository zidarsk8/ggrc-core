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
    self.get_objects("Snapshot")

    count = len(self.objects["Assessment"]) / 2
    assessments = generator.random_objects("Assessment", count, self.objects)
    self._edit_assessments(assessments)
    full_assessments = self._edit_assessment_states(assessments[:count / 2])
    self._map_snapshots(full_assessments)

    sys.exit(0)

  def _map_snapshots(self, full_assessments):
    for assessment in full_assessments:
      all_snapshots = self.snapshots[assessment["audit"]["id"]]
      destinations = (
          generator.random_objects("Control", 5, all_snapshots) +
          generator.random_objects("Objective", 5, all_snapshots) +
          generator.random_objects("Regulation", 5, all_snapshots)
      )
      self.create_relationships([slug], destinations)

  def _edit_assessments(self, assessments):
    for assessment in assessments:
      self.update_object(assessment)

  def _edit_assessment_states(self, assessments):
    states = [
        "Ready for Review",
        "Completed",
        "Verified",
    ]
    full_assessments = []
    for assessment in assessments:
      state = random.choice(states)
      response = self.update_object(assessment, changes={
          "status": state,
      })
      full_assessments.append(response.json().values()[0])
    return full_assessments

class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = SetUpAssessments
  min_wait = 2000
  max_wait = 2000
