# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import re


def prepare_slug(slug):
  return re.sub(r'\r|\n', " ", slug.strip())


class ImportException(Exception):

  def __init__(self, message, show_preview=False, converter=None):
    self.message = message
    self.show_preview = show_preview
    self.converter = converter

  def __str__(self):
    if self.message:
      return self.message
    return "Import error: verify the file is correctly formatted."
