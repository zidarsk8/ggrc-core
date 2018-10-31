# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Module for locust read tasks."""

import copy

import locust

from performance import generator
from performance.assessment import const


class AuditTestsBase(locust.TaskSet):
  """Tests for assessment read operations."""

  # glob creator on mihaz acl with mem
  self.session = (
      "session="  # noqa
  )
  self.sacsid = (
      "SACSID="  # noqa
  )
  self.user_id = 402

  def __init__(self, *args, **kwargs):
    super(AssessmentGET, self).__init__(*args, **kwargs)

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

  def post_assessments(self):
    self.post_assessment(49)
    self.post_assessment(4567)

  def post_assessment(self, audit_id=49):
    assessment_json = copy.deepcopy(const.assessment_payload)
    assessment_json[0]["assessment"]["title"] = generator.random_str()
    assessment_json[0]["assessment"]["audit"]["id"] = audit_id
    self.client.post(
        "/api/assessments",
        json=assessment_json,
        headers=self.headers,
        name="Create Assessment on Audit {}".format(audit_id),
    )
    assessment_count = copy.deepcopy(const.audit_assessment_tree_view_query)
    assessment_count[0]["filters"]["expression"]["ids"] = [str(audit_id)]
    self.client.post(
        "/query",
        json=assessment_count,
        headers=self.headers,
        name="Audit 49 Assessments tab query",
    )

  def get_audits(self):
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
        json=const.audit_4567_count,
        headers=self.headers,
        name="Audit 4567 objects count query",
    )
    self.client.get(
        "/api/audits/4567/summary",
        headers=self.headers,
        name=" Audit 4567 summary query",
    )

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
        json=const.audit_49_count,
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
  task_set = AuditTestsBase
  min_wait = 100
  max_wait = 100
