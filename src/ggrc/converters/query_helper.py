# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from werkzeug.exceptions import BadRequest

from ggrc.models.relationship import RelationshipHelper
from ggrc.converters import IMPORTABLE


class QueryHelper(object):
  """ Helper class for handling request queries

  Primary use for this class is to get list of object ids for each object
  defined in the query. All object ids must pass the query filters if they
  are defined.

  query object = [
    {
      object_name: class name,
      fields: [list of column names],
      filters: {
      relevant_filters:
        [ list of filters joined by OR expression
          [ list of filters joined by AND expression
            {
              "object_name": class of relevant object,
              "slugs": list of relevant object slugs,
                      optional and if exists will be converted into ids
              "ids": list of relevant object ids
            }
          ]
        ]
      }
      object_filters: {
        TODO: allow filtering by title, description and other object fields
      }
    }
  ]
  """

  def __init__(self, query):
    self.query = self.clean_query(query)
    self.object_map = {o.__name__: o for o in IMPORTABLE.values()}

  def clean_query(self, query):
    return query

  def get_ids(self):
    for object_query in self.query:
      object_query["ids"] = self.get_object_ids(object_query)
    return self.query

  def get_object_ids(self, object_query):
    """ get a set of object ids describideb in the filters """
    object_name = object_query["object_name"]
    filters = object_query.get("filters", {})
    relevant_filters = filters.get("relevant_filters")
    relevant_by_ids = None
    if relevant_filters:
      relevant_by_ids = self.get_by_relevant_filters(
          object_name, relevant_filters)
    object_filters = filters.get("object_filters")
    if object_filters:
      return self.get_filtered_objects(
          object_name, object_filters, relevant_by_ids)
    if relevant_by_ids:
      return relevant_by_ids
    return set()

  def get_filtered_objects(self, object_name, filters, relevant_ids):
    """ get objects by key filters """
    return []

  def get_by_relevant_filters(self, object_name, filters):
    """ get object ids by relevancy filters """
    results = set()
    for or_filters in filters:
      and_results = [self.get_related_object_ids(
          object_name,
          and_filter["object_name"],
          and_filter["slugs"],
      )for and_filter in or_filters]
      and_results = map(set, and_results)
      and_results = reduce(set.intersection, and_results)
      results |= and_results
    return results

  def get_related_object_ids(self, object_name, related_name, related_slugs):
    related_ids = self.slugs_to_ids(related_name, related_slugs)
    object_ids = RelationshipHelper.get_objects_ids_related_to(
        object_name, related_name, related_ids)
    return object_ids

  def slugs_to_ids(self, object_name, slugs):
    object_class = self.object_map.get(object_name)
    if not object_class:
      return []
    ids = [c.id for c in object_class.query.filter(
        object_class.slug.in_(slugs)).all()]
    return ids

  def test_export_query_json(self, query):
    for export_object in query:
      if set(["object_class", "filters"]) != set(export_object.keys):
        raise BadRequest("object_class and filters are needed")
      if export_object["object_class"] not in self.object_map:
        raise BadRequest("object_class '{}' is not exportable".format(
            export_object["object_class"]))
