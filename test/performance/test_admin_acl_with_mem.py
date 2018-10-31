# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Module for locust read tasks."""

import locust

from performance import audit_tests_base


class AssessmentGET(audit_tests_base.AuditTestsBase):
  """Tests for assessment read operations."""

  # zidarsk8 on dev with mem
  session = (
      "session="
  )
  user_id = 354

  @locust.task(1)
  def test_assessment_post(self):
    self.post_assessments()


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AssessmentGET
  min_wait = 1000
  max_wait = 1000
