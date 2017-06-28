# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for locust read tasks."""

import random

import locust

from performance import base
from performance import request_templates

random.seed(1)


class AssessmentTest(base.BaseTaskSet):
  """Tests for assessment read operations."""

  @locust.task(1)
  def get_assessments_view(self):
    self.client.get("/assessments_view", headers=self.headers_text)

  @locust.task(1)
  def get_cycle_task_count(self):
    self.client.post(
        "/query",
        json=request_templates.query_cycle_task_count_and_overdue,
        headers=self.headers,
        name="/query cycle_task count and overdue task count",
    )

  @locust.task(1)
  def get_assessment_state_filter(self):
    """Test assessment query calls."""
    self.client.post(
        "/query",
        json=request_templates.query_not_started_in_progress_relevant_user,
        headers=self.headers,
        name="/query assessment state in (not started, in progress)",
    )

    self.client.post(
        "/query",
        json=request_templates.query_assessment_relevant_to_person,
        headers=self.headers,
        name="/query assessment count relevant to user",
    )

    self.client.get(
        "/api/people",
        params={"id__in": ("94,4,83,120,93,16,92,43,12,28,91,112,63,114,27,79,"
                           "65,72,20")},
        headers=self.headers,
        name="/api/people id__in"
    )

  @locust.task(1)
  def user_action_2(self):
    """Test calls from user action 2 in performance grid."""

    self.client.get("/assessments/5", headers=self.headers_text)

    self.client.post(
        "/query",
        json=request_templates.query_assessment_relevant_count,
        headers=self.headers,
        name="/query assessment relevant count",
    )

    self.client.post(
        "/query",
        json=request_templates.query_all_original_related_ids,
        headers=self.headers,
        name="/query all related original object ids",
    )

    self.client.get(
        "/api/relationships",
        params={"id__in": "276230,276229,276231,276232,276233,276234,276235"},
        headers=self.headers,
        name="/api/relationships id__in"
    )

    self.client.post(
        "/query",
        json=request_templates.query_aud_snap_comment_document,
        headers=self.headers,
        name="/query related audit snapshot comment document",
    )

    self.client.get(
        "/api/people",
        params={"id__in": ("94,4,83,120,93,16,92,43,12,28,91,112,63,114,27,79,"
                           "65,72,20")},
        headers=self.headers,
        name="/api/people id__in"
    )

    self.client.get(
        "/api/audits",
        params={"id__in": "1"},
        headers=self.headers,
        name="/api/audits id__in"
    )


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AssessmentTest
  min_wait = 500
  max_wait = 2000
