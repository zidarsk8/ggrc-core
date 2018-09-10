# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Utility classes and functions for tests."""
# pylint: disable=too-few-public-methods

import re
import uuid

import waiting

from lib import constants


def append_random_string(text):
  return text + str(uuid.uuid4())


def prepend_random_string(text):
  return str(uuid.uuid4()) + text


class HtmlParser(object):
  """The HtmlParser class simulates what happens with (non-rich)text in HTML.
 """
  @staticmethod
  def parse_text(text):
    """Simulates text parsed by html.
    Args: text (basestring)
    """
    return re.sub(r'\s+', " ", text)


def wait_for(*args, **kwargs):
  """Waits for function to return truthy value."""
  if "timeout_seconds" not in kwargs:
    kwargs["timeout_seconds"] = constants.ux.MAX_USER_WAIT_SECONDS
  return waiting.wait(*args, **kwargs)
