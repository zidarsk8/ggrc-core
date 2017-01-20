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
  """Used for HTTP interactions with App's REST API"""
  BASIC_HEADERS = {'X-Requested-By': 'GGRC',
                   'Content-Type': 'application/json',
                   'Accept-Encoding': 'gzip, deflate'}

  def __init__(self, endpoint):
    self.url = urlparse.urljoin(environment.APP_URL,
                                "/".join([url.API, endpoint]))
    self._count = objects.COUNT
    self.session = None
    self.req_headers = None
    self.req_headers_put = None

  def init_session(self):
    """Return authorization cookie value (request header)."""
    resp = requests.get(urlparse.urljoin(environment.APP_URL, "/login"))
    cookie = Cookie.SimpleCookie()
    cookie.load(resp.headers["Set-Cookie"])
    self.session = cookie["session"].value

  def get_req_headers(self):
    """Return prepared request headers for HTTP GET, POST requests."""
    req_headers = self.BASIC_HEADERS
    if self.session is None:
      self.init_session()
    req_headers["Cookie"] = "session={0}".format(self.session)
    self.req_headers = req_headers
    return req_headers

  def get_req_headers_put(self, res_headers):
    """Return prepared request headers for HTTP PUT request according
    response headers.
    """
    if self.req_headers is None:
      self.get_req_headers()
    req_headers_put = self.req_headers
    req_headers_put["If-Match"] = res_headers["Etag"]
    req_headers_put["If-Unmodified-Since"] = res_headers["Last-Modified"]
    self.req_headers_put = req_headers_put
    self.req_headers_put = None
    return req_headers_put

  def create_object(self, type, **kwargs):
    """Create the object or make other functions used the HTTP request
    (POST method) to the web-server via REST API.
    Return the raw response from the web-server.
    """
    if type == self._count:
      self.url = urlparse.urljoin(environment.APP_URL, url.QUERY)
    req_body = self.generate_body(type=type, **kwargs)
    req_headers = self.get_req_headers()
    resp = requests.post(url=self.url, data=req_body, headers=req_headers)
    return resp

  def update_object(self, old_obj_href, **kwargs):
    """Update the object used the HTTP requests (GET, PUT methods) to the
    web-server via REST API.
    Return the raw response from the web-server.
    """
    old_obj_url = urlparse.urljoin(environment.APP_URL, old_obj_href)
    old_resp_headers = self.get_object(old_obj_url)["resp_headers"]
    old_resp_body = self.get_object(old_obj_url)["resp_body"]
    new_req_headers = self.get_req_headers_put(res_headers=old_resp_headers)
    new_req_body = self.update_body(body=old_resp_body, **kwargs)
    new_resp = requests.put(url=old_obj_url, data=new_req_body,
                            headers=new_req_headers)
    return new_resp

  def get_object(self, obj_url):
    """Get the object's info used the HTTP request (GET method) to the
    web-server via REST API.
    Return the dictionary like as {"body": ***, "headers"" ***}.
    """
    req_headers = self.get_req_headers()
    resp = requests.get(url=obj_url, headers=req_headers)
    return {"resp_body": resp.text, "resp_headers": resp.headers}

  def generate_body(self, type, **kwargs):
    """Generate the body for HTTP request based on JSON representation
    by type and kwargs.
    """
    if type == self._count:
      return json.dumps(
          [TemplateProvider.get_template_as_dict(
              template=type, **kwargs)[self._count]]
      )
    else:
      return json.dumps(
          [TemplateProvider.get_template_as_dict(template=type, **kwargs)]
      )

  @staticmethod
  def update_body(body, **kwargs):
    """Update the body for HTTP request based on JSON representation
    by body and kwargs.
    """
    return json.dumps(
        TemplateProvider.update_template_as_list_of_dict(
            template=body, **kwargs)
    )
