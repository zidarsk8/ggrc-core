# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base


class Widget(base.Widget):
  def __init__(self, driver):
    super(Widget, self).__init__(driver)
    self.object_id = self.url.split("/")[-1][:-1]
