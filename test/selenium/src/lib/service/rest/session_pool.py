# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Pool to hold requests sessions."""

import requests

from lib import url as url_module


BASIC_HEADERS = {"X-Requested-By": "GGRC",
                 "Content-Type": "application/json",
                 "Accept-Encoding": "gzip, deflate, br"}

_sessions = {}  # pylint: disable=invalid-name


def get_session(user):
  """Returns a requests Session for the `user`."""
  try:
    value = _sessions[user.email]
  except KeyError:
    value = _create_session(user)
    _sessions[user.email] = value
  return value


def _create_session(user):
  """Creates a new requests Session for the `user`."""
  session = requests.Session()
  session.headers = BASIC_HEADERS
  _set_login_cookie(session, user)
  return session


def _set_login_cookie(session, user):
  """Sets dev_appserver_login and session cookies."""
  session.get(url_module.Urls().gae_login(user))
  session.get(url_module.Urls().login)


def reset_sessions():
  """Clears all sessions, to be invoked before each test."""
  # pylint: disable=invalid-name, global-statement
  global _sessions
  _sessions = {}
