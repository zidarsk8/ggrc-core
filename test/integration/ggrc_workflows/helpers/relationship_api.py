# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Relationship related helper functions for REST API calls."""

from integration.ggrc_workflows.helpers import common_api


def get_relationship_post_dict(source, destination):
  """Get Relationship JSON representation for POST API call.

    Args:
        source: Relationship source instance.
        destination: Relationship destination instance
    Returns:
        Relationship object dict representation for using in POST request.
    """
  return {
      "relationship": {
          "source": common_api.get_object_subdict(source),
          "destination": common_api.get_object_subdict(destination),
          "context": common_api.get_object_subdict(source.context),
      }
  }
