# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Object mapper modal."""
from lib import base
from lib.page.modal import search_modal_elements


class ObjectMapper(base.WithBrowser):
  """Object mapper modal."""
  # pylint: disable=too-few-public-methods

  def __init__(self):
    super(ObjectMapper, self).__init__()
    self._root = self._browser.element(tag_name="object-mapper")
    self._search_filter_area = search_modal_elements.SearchFilterArea(
        self._root)
    self._search_results_area = search_modal_elements.SearchResultsArea(
        self._root)

  def map_obj(self, obj):
    """Maps object."""
    self._search_filter_area.search_obj(obj)
    self._search_results_area.get_result_by(title=obj.title).select()
    self._search_results_area.click_map_selected()
