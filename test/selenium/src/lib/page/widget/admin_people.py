# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib import environment
from lib.constants import url


class AdminPeople(base.Widget):
  """Model for people widget on admin dashboard"""

  URL = environment.APP_URL \
      + url.ADMIN_DASHBOARD \
      + url.Widget.PEOPLE
