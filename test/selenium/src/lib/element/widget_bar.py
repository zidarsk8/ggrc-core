# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base


class Tab(base.Tab):
    def __init__(self, driver, element_locator):
        """
        Args:
            driver (base.CustomDriver
        """
        super(Tab, self).__init__(driver, element_locator)
        self.items_count = self._parse_item_count_from_label()

    def _parse_item_count_from_label(self):
        """
        Parses number of members which are as string together in the label
        Returns:
            number of members (int)
        """
        return int(self._element.text.split("(")[-1][:-1])
