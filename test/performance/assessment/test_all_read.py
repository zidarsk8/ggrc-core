# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for locust read tasks."""

import logging
import random
import json

import locust

from performance import base
from performance import request_templates
from performance import generator

random.seed(1)


logger = logging.getLogger()


class AssessmentTest(base.BaseTaskSet):
  """Tests for assessment read operations."""

  # INCLUDE_ROLE = False

  def on_start(self):
    super(AssessmentTest, self).on_start()
    self.person = self.set_random_user(roles=["Editor", "Reader"])
    self.edited_assessments = {}

  def _rp(self):
    if random.randint(1, 10) < 3:
      self.person = self.set_random_user(roles=["Editor", "Reader"])
    return self.person

  @locust.task(1)
  def get_query_related_asssessments_statuses(self):
    all_statuses = [
        "Not Started",
        "In Progress",
        "Ready for Review",
        "Completed",
    ]
    statuses = random.sample(
        all_statuses,
        random.randint(0, len(all_statuses))
    )

    person = self._rp()
    query = request_templates.assessment_related_status_query(
        person,
        statuses,
    )
    response = self.client.post(
        "/query",
        headers=self.headers,
        json=query,
        name="{} /query related, statuses = {}".format(
            self.role,
            len(statuses),
        ),
    )
    logger.debug(
        "\nrole: {}\n"
        "statuses: {}\n"
        "response_code: {}\n"
        "query:\n{}\n"
        "results:\n{}\n".format(
            self.role,
            statuses,
            response.status_code,
            json.dumps(query, sort_keys=True, indent=4),
            json.dumps(response.json(), sort_keys=True, indent=4)[:500],
        )
    )

  @locust.task(1)
  def get_query_related_asssessments(self):
    person = self._rp()
    model = "Assessment"
    query = request_templates.relevant_count(model, person)
    response = self.client.post(
        "/query",
        headers=self.headers,
        json=query,
        name="{} /query count related {}".format(self.role, model),
    )
    logger.debug(
        "\nrole: {}\n"
        "response_code: {}\n"
        "query:\n{}\n"
        "results:\n{}\n".format(
            self.role,
            response.status_code,
            json.dumps(query, sort_keys=True, indent=4),
            json.dumps(response.json(), sort_keys=True, indent=4)[:500],
        )
    )

  @locust.task(1)
  def get_api_relationships_multiple(self):
    self._rp()
    model = "Relationship"
    count = 100
    objects = generator.random_objects(model, count, self.objects)
    ids = [obj["id"] for obj in objects]
    self.get_multiple(model, ids)

  @locust.task(1)
  def get_api_audit_multiple(self):
    self._rp()
    model = "Audit"
    count = 1
    objects = generator.random_objects(model, count, self.objects)
    ids = [obj["id"] for obj in objects]
    self.get_multiple(model, ids)

  @locust.task(1)
  def get_api_audit(self):
    self._rp()
    model = "Audit"
    audit = generator.random_object(model, self.objects)
    self.get_from_slug(audit)

  @locust.task(1)
  def get_people_multiple(self):
    model = "Person"
    count = 20
    objects = generator.random_objects(model, count, self.objects)
    ids = [obj["id"] for obj in objects]
    self.get_multiple(model, ids)

  @locust.task(1)
  def get_query_relade_overdue_cycle_tasks(self):
    person = self._rp()
    query = request_templates.cycle_task_count_and_overdue(person)
    response = self.client.post(
        "/query",
        headers=self.headers,
        json=query,
        name="{} /query related and overdue cycle tasks".format(self.role),
    )
    logger.debug(
        "\nrole: {}\n"
        "response_code: {}\n"
        "query:\n{}\n"
        "results:\n{}\n".format(
            self.role,
            response.status_code,
            json.dumps(query, sort_keys=True, indent=4),
            json.dumps(response.json(), sort_keys=True, indent=4)[:500],
        )
    )

  @locust.task(1)
  def get_assessments_view(self):
    self._rp()
    self.client.get(
        "/assessments_view",
        headers=self.headers_text,
        name="{} /assessments_view".format(self.role),
    )

  @locust.task(1)
  def get_api_assessment(self):
    self._rp()
    model = "Assessment"
    assessment = generator.random_object(model, self.objects)
    self.get_from_slug(assessment)

  @locust.task(1)
  def get_assessment(self):
    self._rp()
    model = "Assessment"
    assessment = generator.random_object(model, self.objects)
    self.client.get(
        "/assessments/{id}".format(**assessment),
        headers=self.headers_text,
        name="{} /assessments/XYZ".format(self.role),
    )

  @locust.task(1)
  def test_put_assessment(self):
    self._rp()
    assessment = generator.random_object("Assessment", self.objects)
    self.update_object(assessment)
    self.edited_assessments[assessment["id"]] = assessment

  @locust.task(1)
  def test_put_assessmnet_state(self):
    if not self.edited_assessments:
      return
    self._rp()
    states = [
        "In Progress",
        "Ready for Review",
        "Completed",
    ]
    assessment_id = random.choice(self.edited_assessments.keys())
    assessment = self.edited_assessments[assessment_id]
    state = random.choice(states)
    self.update_object(
        assessment,
        changes={"status": state},
        postfix="state change",
    )
    logger.debug("\nAssessment: {}\n - state: {}".format(assessment, state))


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AssessmentTest
  min_wait = 100
  max_wait = 100
