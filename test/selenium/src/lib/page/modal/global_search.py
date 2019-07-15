# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Global search modal."""
from lib import base
from lib.page.modal import search_modal_elements


class GlobalSearch(base.WithBrowser):
  """Global search modal."""
  # pylint: disable=too-few-public-methods

  def __init__(self):
    super(GlobalSearch, self).__init__()
    self._root = self._browser.element(tag_name="object-search")

  @property
  def search_results_area(self):
    return search_modal_elements.SearchResultsArea(self._root)

  @property
  def search_filter_area(self):
    return search_modal_elements.SearchFilterArea(self._root)

  def search_obj(self, obj):
    """Search object via Global Search.
    Returns found object item."""
    self.search_filter_area.search_obj(obj)
    return self.search_results_area.get_result_by(title=obj.title)
