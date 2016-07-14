# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Main view functions for import and export pages.

This module handles all view related function to import and export pages
including the import/export api endponts.
"""

from flask import current_app
from flask import request
from flask import json
from flask import render_template
from werkzeug.exceptions import BadRequest

from ggrc.app import app
from ggrc.converters.base import Converter
from ggrc.converters.import_helper import generate_csv_string
from ggrc.converters.import_helper import read_csv_file
from ggrc.converters.query_helper import BadQueryException
from ggrc.converters.query_helper import QueryHelper
from ggrc.login import login_required
from ggrc.utils import benchmark


def check_required_headers(required_headers):
  errors = []
  for header, valid_values in required_headers.items():
    if header not in request.headers:
      errors.append("Missing required header '{}'".format(header))
    elif request.headers[header] not in valid_values:
      errors.append("Invalid header value for '{}'".format(header))

  if errors:
    raise BadRequest("\n".join(errors))


def parse_export_request():
  """ Check if request contains all required fields """
  required_headers = {
      "X-Requested-By": ["gGRC"],
      "Content-Type": ["application/json"],
      "X-export-view": ["blocks", "grid"],
  }
  check_required_headers(required_headers)
  return request.json


def handle_export_request():
  try:
    data = parse_export_request()
    with benchmark("Create Query helper"):
      query_helper = QueryHelper(data)
    with benchmark("get ids"):
      converter = Converter(ids_by_type=query_helper.get_ids())
    with benchmark("generate array"):
      csv_data = converter.to_array()
    with benchmark("generate csv string"):
      csv_string = generate_csv_string(csv_data)

    with benchmark("return csv response"):
      object_names = "_".join(converter.get_object_names())
      filename = "{}.csv".format(object_names)

      headers = [
          ("Content-Type", "text/csv"),
          ("Content-Disposition", "attachment; filename='{}'".format(filename)),
      ]
      return current_app.make_response((csv_string, 200, headers))
  except BadQueryException as exception:
    raise BadRequest(exception.message)
  except Exception as exception:
    current_app.logger.exception(exception)
  raise BadRequest("Export failed due to server error.")


def check_import_file():
  if "file" not in request.files or not request.files["file"]:
    raise BadRequest("Missing csv file")
  csv_file = request.files["file"]
  if not csv_file.filename.lower().endswith(".csv"):
    raise BadRequest("Invalid file type.")
  return csv_file


def parse_import_request():
  """ Check if request contains all required fields """
  required_headers = {
      "X-Requested-By": ["gGRC"],
      "X-test-only": ["true", "false"],
  }
  check_required_headers(required_headers)
  csv_file = check_import_file()
  csv_data = read_csv_file(csv_file)
  dry_run = request.headers["X-test-only"] == "true"
  return dry_run, csv_data


def handle_import_request():
  try:
    dry_run, csv_data = parse_import_request()
    converter = Converter(dry_run=dry_run, csv_data=csv_data)
    converter.import_csv()
    response_data = converter.get_info()
    response_json = json.dumps(response_data)
    headers = [("Content-Type", "application/json")]
    return current_app.make_response((response_json, 200, headers))
  except Exception as exception:
    current_app.logger.exception(exception)
  raise BadRequest("Import failed due to server error.")


def init_converter_views():
  """Initialize views for import and export."""

  # pylint: disable=unused-variable
  # The view function trigger a false unused-variable.
  @app.route("/_service/export_csv", methods=["POST"])
  @login_required
  def handle_export_csv():
    with benchmark("handle export request"):
      return handle_export_request()

  @app.route("/_service/import_csv", methods=["POST"])
  @login_required
  def handle_import_csv():
    with benchmark("handle import request"):
      return handle_import_request()

  @app.route("/import")
  @login_required
  def import_view():
    return render_template("import_export/import.haml")

  @app.route("/export")
  @login_required
  def export_view():
    return render_template("import_export/export.haml")
