# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Represents a page with the url of some object."""
import re

from lib import base, environment
from lib.page.widget import page_tab


class ObjectPage(base.WithBrowser):
  """Represents some tab of some object page."""

  @property
  def top_tabs(self):
    """Returns Tabs page elements for top page tabs."""
    return page_tab.Tabs(self._browser, page_tab.Tabs.TOP)

  def _get_url_match(self):
    """Returns instance of re.MatchObject for current page url."""
    current_url = self._browser.url
    pattern = r"{}\w+/(\d+)".format(environment.app_url)
    return re.search(pattern, current_url)

  def get_url(self):
    """Gets url of the object if page relates to the object."""
    match = self._get_url_match()
    if match:
      return match.string
    return None

  def get_obj_id(self):
    """Gets id of the object (if possible)."""
    match = self._get_url_match()
    if match:
      return match.group(1)
    return None
