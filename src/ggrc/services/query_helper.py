# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""This module contains special query helper class for query API."""

from datetime import datetime

from ggrc.builder import json
from ggrc.converters.query_helper import QueryHelper


class QueryAPIQueryHelper(QueryHelper):
  """Helper class for handling request queries for query API.

  query object = [
    {
      # the same parameters as in QueryHelper
      fields: [ a list of fields to include in JSON if query_type is "values" ]
    }
  ]

  After the query is done (by `get` method), the results are appended
  to each query object:

  query object with results = [
    {
      # the same fields as in QueryHelper
      values: [ filtered objects in JSON ]
              (present if values parameter is True)
      ids: [ ids of filtered objects ] (present if ids parameter is True)
      count: the number of objects filtered, after "limit" is applied
      total: the number of objects filtered, before "limit" is applied
             (present if total parameter is True)
  """
  def get(self, ids=False, total=False, values=False):
    """Filter the objects and get their information.

    Updates self.query items with their results.

    Args:
      ids: if True, provide ids of the filtered objects under ["ids"];
      total: if True, provide the total number of the filtered objects
             before "limit" is applied under ["total"];
      values: if True, provide the filtered objects themselves under ["values"]

    Returns:
      list of dicts: same query as the input with requested results that match
                     the filter.
    """
    if not (ids or total or values):
      # no additional info requested, no action required
      return self.query
    for object_query in self.query:
      objects = self._get_objects(object_query)
      if total:
        object_query["total"] = len(objects)
      objects = self._apply_order_by_and_limit(
          objects,
          order_by=object_query.get("order_by"),
          limit=object_query.get("limit"),
      )
      if values:
        object_query["values"] = objects
      if ids:
        object_query["ids"] = [o.id for o in objects]
    return self.query

  @staticmethod
  def _transform_to_json(objects, fields=None):
    """Make a JSON representation of objects from the list."""
    objects_json = [json.publish(obj) for obj in objects]
    objects_json = json.publish_representation(objects_json)
    if fields:
      objects_json = [{f: o.get(f) for f in fields}
                      for o in objects_json]
    return objects_json

  @staticmethod
  def _get_last_modified(model, objects):
    """Get the time of last update of an object in the list."""
    if not objects:
      return None
    elif hasattr(model, "updated_at"):
      return max(obj.updated_at for obj in objects)
    else:
      return datetime.now()
