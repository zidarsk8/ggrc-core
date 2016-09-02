# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

import json
import time
from urlparse import urlparse
from integration.ggrc import services

COLLECTION_ALLOWED = ["HEAD", "GET", "POST", "OPTIONS"]
RESOURCE_ALLOWED = ["HEAD", "GET", "PUT", "DELETE", "OPTIONS"]


class TestServices(services.TestCase):

  def get_location(self, response):
    """Ignore the `http://localhost` prefix of the Location"""
    return response.headers["Location"][16:]

  def assertRequiredHeaders(self, response,
                            headers={"Content-Type": "application/json"}):
    self.assertIn("Etag", response.headers)
    self.assertIn("Last-Modified", response.headers)
    self.assertIn("Content-Type", response.headers)
    for k, v in headers.items():
      self.assertEqual(v, response.headers.get(k))

  def assertAllow(self, response, allowed=None):
    self.assert405(response)
    self.assertIn("Allow", response.headers)
    if allowed:
      self.assertItemsEqual(allowed, response.headers["Allow"].split(", "))

  def assertOptions(self, response, allowed):
    self.assertIn("Allow", response.headers)
    self.assertItemsEqual(allowed, response.headers["Allow"].split(", "))

  def headers(self, *args, **kwargs):
    ret = list(args)
    ret.append(("X-Requested-By", "Unit Tests"))
    ret.extend(kwargs.items())
    return ret

  def test_X_Requested_By_required(self):
    response = self.client.post(self.mock_url())
    self.assert400(response)
    response = self.client.put(self.mock_url() + "/1", data="blah")
    self.assert400(response)
    response = self.client.delete(self.mock_url() + "/1")
    self.assert400(response)

  def test_empty_collection_get(self):
    response = self.client.get(self.mock_url(), headers=self.headers())
    self.assert200(response)

  def test_missing_resource_get(self):
    response = self.client.get(self.mock_url("foo"), headers=self.headers())
    self.assert404(response)

  def test_collection_put(self):
    self.assertAllow(
        self.client.put(self.mock_url(), headers=self.headers()),
        COLLECTION_ALLOWED)

  def test_collection_delete(self):
    self.assertAllow(
        self.client.delete(self.mock_url(), headers=self.headers()),
        COLLECTION_ALLOWED)

  def test_put_successful(self):
    mock = self.mock_model(foo="buzz")
    response = self.client.get(self.mock_url(mock.id), headers=self.headers())
    self.assert200(response)
    self.assertRequiredHeaders(response)
    obj = response.json
    self.assertEqual("buzz", obj["services_test_mock_model"]["foo"])
    obj["services_test_mock_model"]["foo"] = "baz"
    url = urlparse(obj["services_test_mock_model"]["selfLink"]).path
    original_headers = dict(response.headers)
    # wait a moment so that we can be sure to get differing Last-Modified
    # after the put - the lack of latency means it's easy to end up with
    # the same HTTP timestamp thanks to the standard's lack of precision.
    time.sleep(1.1)
    response = self.client.put(
        url,
        data=json.dumps(obj),
        headers=self.headers(
            ("If-Unmodified-Since", original_headers["Last-Modified"]),
            ("If-Match", original_headers["Etag"]),
        ),
        content_type="application/json",
    )
    self.assert200(response)
    response = self.client.get(url, headers=self.headers())
    self.assert200(response)
    self.assertNotEqual(
        original_headers["Last-Modified"], response.headers["Last-Modified"])
    self.assertNotEqual(
        original_headers["Etag"], response.headers["Etag"])
    self.assertEqual("baz", response.json["services_test_mock_model"]["foo"])

  def test_put_value_error(self):
    """Test response code for put request with value errors."""
    mock = self.mock_model(foo="buzz")
    response = self.client.get(self.mock_url(mock.id), headers=self.headers())
    obj = response.json
    obj["services_test_mock_model"]["validated"] = "Value Error"
    url = urlparse(obj["services_test_mock_model"]["selfLink"]).path
    original_headers = dict(response.headers)
    response = self.client.put(
        url,
        data=json.dumps(obj),
        headers=self.headers(
            ("If-Unmodified-Since", original_headers["Last-Modified"]),
            ("If-Match", original_headers["Etag"]),
        ),
        content_type="application/json",
    )
    self.assertEqual(response.status_code, 400)

  def test_put_bad_request(self):
    mock = self.mock_model(foo="tough")
    response = self.client.get(self.mock_url(mock.id), headers=self.headers())
    self.assert200(response)
    self.assertRequiredHeaders(response)
    url = urlparse(response.json["services_test_mock_model"]["selfLink"]).path
    response = self.client.put(
        url,
        content_type="application/json",
        data="This is most definitely not valid content.",
        headers=self.headers(
            ("If-Unmodified-Since", response.headers["Last-Modified"]),
            ("If-Match", response.headers["Etag"]))
    )
    self.assert400(response)

  def test_options(self):
    mock = self.mock_model()
    response = self.client.open(
        self.mock_url(mock.id), method="OPTIONS", headers=self.headers())
    self.assertOptions(response, RESOURCE_ALLOWED)

  def test_collection_options(self):
    response = self.client.open(
        self.mock_url(), method="OPTIONS", headers=self.headers())
    self.assertOptions(response, COLLECTION_ALLOWED)

  def test_get_bad_accept(self):
    mock1 = self.mock_model(foo="baz")
    response = self.client.get(
        self.mock_url(mock1.id),
        headers=self.headers(("Accept", "text/plain")))
    self.assertStatus(response, 406)
    self.assertEqual("text/plain", response.headers.get("Content-Type"))
    self.assertEqual("application/json", response.data)

  def test_collection_get_bad_accept(self):
    response = self.client.get(
        self.mock_url(),
        headers=self.headers(("Accept", "text/plain")))
    self.assertStatus(response, 406)
    self.assertEqual("text/plain", response.headers.get("Content-Type"))
    self.assertEqual("application/json", response.data)

  def test_get_if_none_match(self):
    mock1 = self.mock_model(foo="baz")
    response = self.client.get(
        self.mock_url(mock1.id),
        headers=self.headers(("Accept", "application/json")))
    self.assert200(response)
    previous_headers = dict(response.headers)
    response = self.client.get(
        self.mock_url(mock1.id),
        headers=self.headers(
            ("Accept", "application/json"),
            ("If-None-Match", previous_headers["Etag"]),
        ),
    )
    self.assertStatus(response, 304)
    self.assertIn("Etag", response.headers)
