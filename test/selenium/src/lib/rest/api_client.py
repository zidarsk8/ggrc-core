# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""GGRC REST API client."""
import urlparse

from lib import environment, users
from lib.service.rest import session_pool


def send_get(url):
  """Sends GET request to `url`."""
  url = urlparse.urljoin(environment.app_url, url)
  return _user_session().get(url).json()


def send_post(url, json_body):
  """Sends POST request to `url` with `json_body`."""
  url = urlparse.urljoin(environment.app_url, url)
  return _user_session().post(url, json=json_body).json()


def _user_session():
  """Returns a Requests session for the current user."""
  return session_pool.get_session(users.current_user())
