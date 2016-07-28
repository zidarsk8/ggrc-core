# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""This module contains logic to handle '/query' endpoint."""

from datetime import datetime
import time
from wsgiref.handlers import format_date_time

from flask import request
from flask import current_app

from ggrc.builder import json
from ggrc.converters.query_helper import QueryHelper
from ggrc.login import login_required
from ggrc.models.inflector import get_model
from ggrc.services.common import etag
from ggrc.utils import as_json


def build_collection_representation(model, objects, total):
  """Enclose objects list into type-describing block."""
  # pylint: disable=protected-access
  collection = [{
      model.__name__: {
          "total": total,
          "count": len(objects),
          "values": objects,
      },
      "selfLink": None,  # not implemented yet
  }]
  return collection


def get_last_modified(model, objects):
  """Get last object update time for Last-Modified header."""
  if hasattr(model, 'updated_at') and objects:
    last_modified = max(obj.updated_at for obj in objects)
  else:
    last_modified = datetime.now()
  return last_modified


def json_success_response(response_object, last_modified, status=200):
  """Build a 200-response with metadata headers."""
  headers = [
      ('Last-Modified', http_timestamp(last_modified)),
      ('Etag', etag(response_object)),
      ('Content-Type', 'application/json'),
  ]
  return current_app.make_response(
      (as_json(response_object), status, headers),
  )


def http_timestamp(timestamp):
  return format_date_time(time.mktime(timestamp.utctimetuple()))


def get_objects_by_query():
  """Return objects corresponding to a POST'ed query."""
  # Note: only a single query in a single request is supported now. If we get
  # several queries in a single request, we process only the first one
  request_json = request.json[0]

  # valid types should be: 'values', 'ids', 'count'
  query_type = request_json.get('type', 'values')
  object_type = request_json.get('object_name')
  query_helper = QueryHelper([request_json])

  if query_type == 'values':
    result = query_helper.get(values=True, total=True)[0]
    object_type = result['object_name']
    total = result['total']
    objects = result['values']

    model = get_model(object_type)
    objects_json = [json.publish(obj) for obj in objects]
    objects_json = json.publish_representation(objects_json)

    if result.get('fields'):
      objects_json = [{f: o.get(f) for f in result['fields']}
                      for o in objects_json]
    collection = build_collection_representation(model, objects_json, total)
  else:
    raise NotImplementedError("Only 'values' queries are supported now")

  return json_success_response(
      collection,
      get_last_modified(model, objects),
  )


def init_query_view(app):
  # pylint: disable=unused-variable
  @app.route('/query', methods=['POST'])
  @login_required
  def query_objects():
    """Advanced object collection queries view."""
    return get_objects_by_query()
