# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for locust read tasks."""

import logging
import random
import json

import locust

from performance import base
from performance import models
from performance import request_templates

random.seed(1)


logger = logging.getLogger()


class AssessmentTest(base.BaseTaskSet):
  """Tests for assessment read operations."""

  @locust.task(10)
  def get_query_related_asssessments(self):
    statuses = [
        "Not Started",
        "In Progress",
        "Ready for Review",
        "Completed",
    ]
    status_sample = random.sample(statuses, random.randint(0, len(statuses)))
    person = self.set_random_user(roles=models.GLOBAL_ROLES)
    query = request_templates.assessment_related_status_query(
        person,
        status_sample,
    )
    response = self.client.post(
        "/query",
        headers=self.headers_text,
        json=query,
        name="{} /query related, status = {}".format(
            self.role,
            len(status_sample),
        ),
    )
    logger.debug(
        "\nrole: {}\n"
        "statuses: {}\n"
        "response_code: {}\n"
        "query:\n{}\n"
        "results:\n{}\n".format(
            self.role,
            status_sample,
            response.status_code,
            json.dumps(query, sort_keys=True, indent=4),
            json.dumps(response.json(), sort_keys=True, indent=4)[:500],
        )
    )


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AssessmentTest
  min_wait = 100
  max_wait = 100
