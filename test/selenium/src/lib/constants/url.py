# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""The module provides constants GGRC's URLs construction."""

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from lib.constants.objects import *  # noqa; the names are later exported
import urlparse

from lib.constants import objects


# URL's parts for objects
API = "api"
DASHBOARD = "dashboard"
ADMIN_DASHBOARD = "admin"
AUDIT = AUDITS + "/{0}"
RELATIONSHIPS = "relationships"
OBJECT_OWNERS = "object_owners"
CONTACTS = "contacts"
QUERY = "query"

# url path for user
DEFAULT_EMAIL_DOMAIN = "example.com"
DEFAULT_EMAIL = "user@" + DEFAULT_EMAIL_DOMAIN
DEFAULT_URL_USER_API = "/".join([API, PEOPLE, str(1)])


class Widget(object):
  """URL's parts for widgets."""
  # pylint: disable=too-few-public-methods
  # common
  INFO = "#info_widget"
  # admin dashboard page
  CUSTOM_ATTRIBUTES = "#custom_attribute_widget"
  EVENTS = "#events_list_widget"
  ROLES = "#roles_list_widget"
  PEOPLE = "#people_list_widget"
  ASSESSMENTS = "#assessment_widget"
  ASSESSMENT_TEMPLATES = "#assessment_template_widget"
  CONTROLS = "#control_widget"


def get_second_part_url(full_url):
  """Get the second part of the full URL.
  Example: "http://localhost/api/controls" -> "/api/controls"
  """
  return urlparse.urlparse(full_url).path
