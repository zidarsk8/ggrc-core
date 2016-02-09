# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import environment
from lib.constants import url
from lib.page.widget.base import Widget


class AdminEvents(Widget):
  URL = environment.APP_URL \
      + url.ADMIN_DASHBOARD \
      + url.Widget.EVENTS
