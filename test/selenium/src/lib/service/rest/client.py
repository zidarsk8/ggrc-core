# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""The module contains classes for working with REST API."""
# pylint: disable=redefined-builtin

import Cookie
import json
import urlparse

import requests

from lib import environment
from lib.constants import url, objects
from lib.service.rest.template_provider import TemplateProvider


class RestClient(object):
  """Client for HTTP interactions with GGRC's REST API."""
  BASIC_HEADERS = {'X-Requested-By': 'GGRC',
                   'Content-Type': 'application/json',
                   'Accept-Encoding': 'gzip, deflate'}

  def __init__(self, endpoint):
    self.url = urlparse.urljoin(environment.APP_URL,
                                "/".join([url.API, endpoint]))
    self._count = objects.COUNT
    self.session_cookie = None

  def get_session_cookie(self):
    """Send a GET request to the login URL, get a response and return the
    session cookie from response headers for further usage.
    """
    resp = requests.get(urlparse.urljoin(environment.APP_URL, "/login"))
    cookies = Cookie.SimpleCookie()
    cookies.load(resp.headers["Set-Cookie"])
    self.session_cookie = cookies["session"].value

  def generate_req_headers(self, resp_headers=None):
    """Create a request headers for the further HTTP calls.
    If 'resp_headers' is 'None' than return a request headers from a predefined
    basic headers and session cookie.
    If 'resp_headers' is not 'None' than return a request headers from a
    predefined basic headers, session cookie and response headers.
    """
    req_headers = self.BASIC_HEADERS
    if self.session_cookie is None:
      self.get_session_cookie()
    req_headers["Cookie"] = "session={value}".format(value=self.session_cookie)
    if resp_headers:
      req_headers["If-Match"] = resp_headers["Etag"]
      req_headers["If-Unmodified-Since"] = resp_headers["Last-Modified"]
    return req_headers

  def create_object(self, type, **kwargs):
    """Create an object or make other operations used a POST request and
    return the raw response.
    """
    if type == self._count:
      self.url = urlparse.urljoin(environment.APP_URL, url.QUERY)
    req_headers = self.generate_req_headers()
    req_body = self.generate_body(type=type, **kwargs)
    resp = requests.post(url=self.url, data=req_body, headers=req_headers)
    return resp

  def update_object(self, href, **kwargs):
    """Update an object used a GET, POST requests and return the raw response.
    """
    obj_url = urlparse.urljoin(environment.APP_URL, href)
    obj_resp_headers = self.get_object(obj_url)["resp_headers"]
    obj_resp_body = self.get_object(obj_url)["resp_body"]
    new_obj_req_headers = self.generate_req_headers(
        resp_headers=obj_resp_headers)
    new_obj_req_body = self.update_body(body=obj_resp_body, **kwargs)
    new_obj_resp = requests.put(url=obj_url, data=new_obj_req_body,
                                headers=new_obj_req_headers)
    return new_obj_resp

  def get_object(self, obj_url):
    """Get an object used a GET request and return a dictionary:
    {"resp_body": resp.text, "resp_headers": resp.headers}.
    """
    req_headers = self.generate_req_headers()
    resp = requests.get(url=obj_url, headers=req_headers)
    return {"resp_body": resp.text, "resp_headers": resp.headers}

  def generate_body(self, type, **kwargs):
    """Generate a body of HTTP request based on JSON representation."""
    if type == self._count:
      return json.dumps(
          [TemplateProvider.generate_template_as_dict(
              template=type, **kwargs)[self._count]]
      )
    else:
      return json.dumps(
          [TemplateProvider.generate_template_as_dict(template=type, **kwargs)]
      )

  @staticmethod
  def update_body(body, **kwargs):
    """Update a body of HTTP request based on JSON representation."""
    return json.dumps(
        TemplateProvider.update_template_as_dict(
            template=body, **kwargs)
    )
