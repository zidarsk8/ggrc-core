# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Module for locust read tasks."""

import copy

import locust

from performance import generator
from performance.assessment import const


class AuditTestsBase(locust.TaskSet):
  """Tests for assessment read operations."""

  session = (
      "session="  # noqa
  )
  sacsid = (
      "SACSID="  # noqa
  )
  user_id = 402

  def __init__(self, *args, **kwargs):
    super(AuditTestsBase, self).__init__(*args, **kwargs)

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
    self.post_assessment(49, 1)
    self.post_assessment(4567, 1)
    self.post_assessment(49, 10)
    self.post_assessment(4567, 10)
    self.post_assessment(49, 50)
    self.post_assessment(4567, 50)

  def post_audits(self):
    self.post_audit(71, 1)
    self.post_audit(2009, 1)
    self.post_audit(71, 10)
    self.post_audit(2009, 10)
    self.post_audit(71, 50)
    self.post_audit(2009, 50)


  def post_audit(self, program_id, people_count):
    prefix = "Program {:>4}, {:>2} * 3 people".format(program_id, people_count)
    audit_json = copy.deepcopy(const.audit_payload)
    audit = audit_json[0]["audit"]
    audit["title"] = generator.random_str()
    audit["program"]["id"] = program_id
    audit["access_control_list"] = self._get_audit_acl(people_count)
    self.client.post(
        "/api/audits",
        json=audit_json,
        headers=self.headers,
        name="{} - Create Audit".format(prefix),
    )
    audit_count = copy.deepcopy(const.program_audit_tree_view_query)
    audit_count[0]["filters"]["expression"]["ids"] = [str(program_id)]
    self.client.post(
        "/query",
        json=audit_count,
        headers=self.headers,
      name="Program {:>4} - Audits tab query".format(program_id),
    )
    pass

  @classmethod
  def _get_audit_acl(cls, people_count):
    roles = [128, 129]
    people_list = []
    for i in range(people_count):
      for role_id in roles:
        people_list.append(
            {
                "ac_role_id": role_id,
                "person": {
                    "id": const.people_ids[i + role_id]
                },
                "person_id": const.people_ids[i + role_id]
            }
        )
    return people_list

  @classmethod
  def _get_assessment_acl(cls, people_count):
    # creators_role_id = 124
    # assignees_role_id = 120
    # verifiers_role_id = 121
    roles = [124, 120, 121]
    people_list = []
    for i in range(people_count):
      for role_id in roles:
        people_list.append(
            {
                "ac_role_id": role_id,
                "person": {
                    "id": const.people_ids[i + role_id]
                },
                "person_id": const.people_ids[i + role_id]
            }
        )
    return people_list

  def post_assessment(self, audit_id, people_count=1):
    prefix = "Audit {:>4}, {:>2} * 3 people".format(audit_id, people_count)
    assessment_json = copy.deepcopy(const.assessment_payload)
    assessment = assessment_json[0]["assessment"]
    assessment["title"] = generator.random_str()
    assessment["audit"]["id"] = audit_id
    assessment["access_control_list"] = self._get_assessment_acl(people_count)
    self.client.post(
        "/api/assessments",
        json=assessment_json,
        headers=self.headers,
        name="{} - Create Assessment".format(prefix),
    )
    assessment_count = copy.deepcopy(const.audit_assessment_tree_view_query)
    assessment_count[0]["filters"]["expression"]["ids"] = [str(audit_id)]
    self.client.post(
        "/query",
        json=assessment_count,
        headers=self.headers,
      name="Audit {:>4} - Assessments tab query".format(audit_id),
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
