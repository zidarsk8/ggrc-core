# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Module for locust read tasks."""

import copy

import logging
import random

import locust

from performance import generator
from performance.assessment import const

random.seed(1)

logger = logging.getLogger()

COUNT = 1


class AssessmentGET(locust.TaskSet):
  """Tests for assessment read operations."""

  def __init__(self, *args, **kwargs):
    super(AssessmentGET, self).__init__(*args, **kwargs)

    self.session = (
        "session=eyJfZnJlc2giOnRydWUsIl9pZCI6eyIgYiI6Ik9UZzJObVZtTTJFMk1XSXhaRFF3TXpNNE9UUTJOMkk1WlRVME16VmxPREU9In0sInVzZXJfaWQiOiIzNTQifQ.Dq0SOw.Ix5iYjKQMxK6LVdENfJHTNnMXtk"  # noqa
    )
    self.sacsid = (
        "SACSID=~AJKiYcExbXqTjtaoVLy_ZxQbw_VJ-A2oA9Y-bIqD7KnkJHGiQWnHcKlXw5RFWFqs-cYToYakukZsighn-DsNa_gCXVu6NLe-LXr90rkR-C7HJb17Hoaj5QnA-Uc4cdxdwayYIbvClHewzFWXJg_mvY0xAXK0fXJzJVFH8BbKQSNH-kHxeDhCtQtKlc3GhrCzwZ6u2vwNtmDdimmyHas5sLM8SVrhBBboC6NFVmdlU3B6kEbJOrlS6DwvPhmnB5FACtLuuFi0wtwWIHzf-BJTcn-OwkCPAYdOGg6kCC0YfH7HSziw1b19OzhIXx_pdIvcIfagVpofv3OTE1VBWUJ7xpgQk3SzPlERQA"  # noqa
    )
    self.user_id = 354

    self.header_base = {
        "pragma":
        "no-cache",
        "accept-encoding":
        "gzip, deflate, sdch, br",
        "accept-language":
        "en-US,en;q=0.8,sl;q=0.6",
        "upgrade-insecure-requests":
        "1",
        "user-agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWe"
        "bKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "cache-control":
        "no-cache",
        "authority":
        "ggrc-ux-demo.appspot.com",
        "x-requested-by":
        "GGRC",
    }

    self.headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
    }
    self.headers_text = {
        "accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                   "image/webp,*/*;q=0.8"),
    }

    self.headers.update(self.header_base)
    self.headers_text.update(self.header_base)
    self._update_cookie()

  def _update_cookie(self):
    cookie = self.session
    self.headers["cookie"] = cookie
    self.headers_text["cookie"] = cookie

  def on_start(self):
    """ on_start is called when a Locust start before any task is scheduled """

  def get_assessments_view(self):
    self.client.get(
        "/dashboard",
        headers=self.headers_text,
        name=" Dashboard",
    )

  def task_runner(self):
    pass
    # last_assessment_id = self.post_assessment()
    # self.post_comment(last_assessment_id)

  def post_assessment(self, audit_id=49):
    assessment_json = copy.deepcopy(const.assessment_payload)
    assessment_json[0]["assessment"]["title"] = generator.random_str()
    assessment_json[0]["assessment"]["audit"]["id"] = audit_id
    response = self.client.post(
        "/api/assessments",
        json=assessment_json,
        headers=self.headers,
        name="Create Assessment on Audit {}".format(audit_id),
    )
    assessment_count = copy.deepcopy(const.audit_assessment_tree_view_query)
    assessment_count[0]["filters"]["expression"]["ids"] = [str(audit_id)]
    response = self.client.post(
        "/query",
        json=assessment_count,
        headers=self.headers,
        name="Audit 49 Assessments tab query",
    )

  def _get_put_headers(self, response):
    """Generate an object PUT request."""
    if "Etag" not in response.headers["Etag"]:
      print response
      print response.headers
    headers = {
        "If-Match": response.headers["Etag"],
        "If-Unmodified-Since": response.headers["Last-Modified"],
    }
    headers.update(self.headers)
    return headers

  def post_comment(self, new_assessment_id):
    assessment_response = self.client.get(
        "/api/assessments/{}".format(new_assessment_id),
        headers=self.headers,
        name=" Assessment on Audit 49",
    )
    for _ in range(COUNT):
      comment_json = copy.deepcopy(const.assessment_comment_payload)
      comment_response = self.client.post(
          "/api/comments",
          json=comment_json,
          headers=self.headers,
          name="Create Comment on new Assessment on Audit 49 ",
      )
      comment_response_json = comment_response.json()
      comment_id = comment_response_json[0][1]["comment"]["id"]

      comment_map = copy.deepcopy(const.assessment_comment_map_payload)
      comment_map["assessment"]["actions"]["add_related"][0]["id"] = comment_id

      assessment_response = self.client.put(
          "/api/assessments/{}".format(new_assessment_id),
          json=comment_map,
          headers=self._get_put_headers(assessment_response),
          name=" Create Assessment on Audit 49 ",
      )

  @locust.task(1)
  def get_audit_4567(self):
    self.client.get(
        "/audits/4567",
        headers=self.headers_text,
        name=" Audit 4567 html page",
    )
    self.client.get(
        "/api/people/{}/task_count".format(self.user_id),
        headers=self.headers,
        name=" Audit 4567 Person {} task_count".format(self.user_id),
    )
    self.client.get(
        "/api/people/{}/profile".format(self.user_id),
        headers=self.headers,
        name=" Audit 4567 Person {} profile".format(self.user_id),
    )

    self.client.post(
        "/query",
        json=const.audit_counts_query,
        headers=self.headers,
        name="Audit 4567 objects count query",
    )
    self.client.get(
        "/api/audits/4567/summary",
        headers=self.headers,
        name=" Audit 4567 summary query",
    )

  @locust.task(1)
  def get_audit_49(self):
    self.client.get(
        "/audits/49",
        headers=self.headers_text,
        name=" Audit 49 html page",
    )
    self.client.get(
        "/api/people/{}/task_count".format(self.user_id),
        headers=self.headers,
        name=" Audit 49 Person {} task_count".format(self.user_id),
    )
    self.client.get(
        "/api/people/{}/profile".format(self.user_id),
        headers=self.headers,
        name=" Audit 49 Person {} profile".format(self.user_id),
    )

    self.client.post(
        "/query",
        json=const.audit_counts_query,
        headers=self.headers,
        name="Audit 49 objects count query",
    )
    self.client.get(
        "/api/audits/49/summary",
        headers=self.headers,
        name=" Audit 49 summary query",
    )


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AssessmentGET
  min_wait = 100
  max_wait = 100
