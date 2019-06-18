# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""This module provides endpoints to add/remove SavedSearch models"""

from flask import request

from ggrc import db
from ggrc import login
from ggrc.app import app
from ggrc.query.views import json_success_response, validate_post_data_keys
from ggrc.utils.error_handlers import make_error_response
from ggrc.models.saved_search import SavedSearch
from ggrc.models.exceptions import ValidationError


@app.route("/api/saved_searches/<int:saved_search_id>", methods=["GET"])
def get_saved_searches_by_id(saved_search_id):
  """

  Args:
    saved_search_id:

  Returns:

  """
  saved_search = SavedSearch.query.filter(
      SavedSearch.id == saved_search_id
  ).first()

  if saved_search:
    response_data = {
        SavedSearch.__name__: saved_search
    }

    return json_success_response(response_data)
  return make_error_response(
      "No saved search with id {} found".format(
          saved_search_id,
      ),
      404,
      force_json=True,
  )


@app.route("/api/saved_searches/<string:search_type>", methods=["GET"])
def get_saved_searches_by_type(search_type):
  """Get SavedSearch by object type

  Get SavedSearch model by object type.
  Request object should includes search_type parameter and can includes
   offset and limit parameters.

  Args:
    search_type: Type of search

  Returns:
    Flask Response object with object_name, count, total and values as payload
  """
  user = login.get_current_user(use_external_user=False)
  all_objects = user.saved_searches.filter(
      SavedSearch.search_type == search_type
  )
  if search_type == SavedSearch.ADVANCED_SEARCH or \
      (search_type == SavedSearch.GLOBAL_SEARCH and
          "object_type" in request.args):
    all_objects = all_objects.filter(
        SavedSearch.object_type == request.args.get("object_type")
    )
  db_query_result = all_objects.order_by(
      SavedSearch.created_at.desc()
  ).offset(
      request.args.get("offset")
  ).limit(
      request.args.get("limit")
  ).all()

  response_data = {
      "object_name": SavedSearch.__name__,
      "count": len(db_query_result),
      "total": all_objects.count(),
      "values": db_query_result,
  }

  return json_success_response(response_data)


@app.route("/api/saved_searches/<int:saved_search_id>", methods=["DELETE"])
def delete_saved_search(saved_search_id):
  """Delete saved search

    Args
      saved_search_id: id of saved_search object that should be deleted

    Returns
      Response object with id of a deleted object or error message if object
      did not found
  """
  user = login.get_current_user(use_external_user=False)

  saved_search = user.saved_searches.filter(
      SavedSearch.id == saved_search_id
  ).first()

  if not saved_search:
    return make_error_response(
        "No saved search with id {} found for current user".format(
            saved_search_id,
        ),
        404,
        force_json=True,
    )

  db.session.delete(saved_search)
  db.session.commit()

  return json_success_response({"deleted": saved_search_id})


@app.route("/api/saved_searches", methods=["POST"])
@validate_post_data_keys(["name", "object_type", "search_type"])
def create_saved_search():
  """Create new saved search"""
  user = login.get_current_user(use_external_user=False)

  data = request.get_json()

  try:
    search = SavedSearch(
        data.get("name"),
        data.get("object_type"),
        user,
        data.get("search_type"),
        data.get("filters"),
    )
  except ValidationError as error:
    return make_error_response(error.message, 400, force_json=True)

  user.saved_searches.append(search)
  db.session.commit()

  return json_success_response(search)
