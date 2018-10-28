# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Module for locust read tasks."""

import locust


class AssessmentGET(locust.TaskSet):
  """Tests for assessment read operations."""

  def __init__(self, *args, **kwargs):
    super(AssessmentGET, self).__init__(*args, **kwargs)

    # glob creator on mihaz acl with mem
    self.session = (
        "session="  # noqa
    )
    self.sacsid = (
        "SACSID="  # noqa
    )
    self.user_id = 402

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
        json=audit_4567_count,
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
        json=audit_49_count,
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


audit_49_count = [{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"AccessGroup"}}},"type":"count"},{"object_name":"Assessment","filters":{"expression":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]}},"type":"count"},{"object_name":"AssessmentTemplate","filters":{"expression":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Contract"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Control"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"DataAsset"}}},"type":"count"},{"object_name":"Evidence","filters":{"expression":{"object_name":"Audit","op":{"name":"related_evidence"},"ids":["49"]}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Facility"}}},"type":"count"},{"object_name":"Issue","filters":{"expression":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Market"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Metric"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Objective"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"OrgGroup"}}},"type":"count"},{"object_name":"Person","filters":{"expression":{"object_name":"Audit","op":{"name":"related_people"},"ids":["49"]}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Policy"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Process"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Product"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"ProductGroup"}}},"type":"count"},{"object_name":"Program","filters":{"expression":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Regulation"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Requirement"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Risk"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Standard"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"System"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"TechnologyEnvironment"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Threat"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["49"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Vendor"}}},"type":"count"}]  # noqa
audit_4567_count = [{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"AccessGroup"}}},"type":"count"},{"object_name":"Assessment","filters":{"expression":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]}},"type":"count"},{"object_name":"AssessmentTemplate","filters":{"expression":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Contract"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Control"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"DataAsset"}}},"type":"count"},{"object_name":"Evidence","filters":{"expression":{"object_name":"Audit","op":{"name":"related_evidence"},"ids":["4567"]}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Facility"}}},"type":"count"},{"object_name":"Issue","filters":{"expression":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Market"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Metric"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Objective"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"OrgGroup"}}},"type":"count"},{"object_name":"Person","filters":{"expression":{"object_name":"Audit","op":{"name":"related_people"},"ids":["4567"]}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Policy"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Process"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Product"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"ProductGroup"}}},"type":"count"},{"object_name":"Program","filters":{"expression":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Regulation"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Requirement"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Risk"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Standard"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"System"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"TechnologyEnvironment"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Threat"}}},"type":"count"},{"object_name":"Snapshot","filters":{"expression":{"left":{"object_name":"Audit","op":{"name":"relevant"},"ids":["4567"]},"op":{"name":"AND"},"right":{"left":"child_type","op":{"name":"="},"right":"Vendor"}}},"type":"count"}]  # noqa
