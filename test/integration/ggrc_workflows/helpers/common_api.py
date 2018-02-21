# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Package contains common API helper functions for REST API calls."""
from ggrc import utils


def get_object_subdict(obj):
  return {
      "id": obj.id,
      "href": utils.url_for(obj),
      "type": obj.type,
  }
