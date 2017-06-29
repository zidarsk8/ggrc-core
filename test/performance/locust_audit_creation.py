# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Base module for locust setup tasks."""

import random

import locust

from performance import base

random.seed(1)


class AuditCreation(base.BaseTaskSet):
  """Base class for locust setup tasks."""

  GAE = True

  _program_mapping_models = [
      "Control",
      "Regulation",
      "Objective",
      "Facility",
  ]

  def __init__(self, *args, **kwargs):
    super(AuditCreation, self).__init__(*args, **kwargs)
    self.programs = []

  def set_up(self):
    super(AuditCreation, self).set_up()
    self._extend_programs()

  def _extend_programs(self):
    self.programs.extend(self.create_programs_with_mappings(
        models_=self._program_mapping_models,
        mapping_count=500,
        count=5,
    ))

  @locust.task(10)
  def create_audit_task(self):
    self.create_audits(
        programs=[random.choice(self.programs)],
        count=1,
        get_snapshots=False,
    )


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AuditCreation
  min_wait = 1000
  max_wait = 2000
