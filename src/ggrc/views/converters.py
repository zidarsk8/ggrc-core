# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from flask import current_app
from flask import request
from flask import json
from flask import render_template
from collections import defaultdict
from werkzeug.exceptions import BadRequest

from ggrc.app import app
from ggrc.login import login_required
from ggrc.converters import IMPORTABLE
from ggrc.converters.base import Converter
from ggrc.converters.import_helper import generate_csv_string
from ggrc.converters.import_helper import read_csv_file
from ggrc.converters.import_helper import split_array


def check_required_headers(required_headers):
  errors = []
  for header, valid_values in required_headers.items():
    if header not in request.headers:
      errors.append("Missing required header '{}'".format(header))
    elif request.headers[header] not in valid_values:
      errors.append("Invalid header value for '{}'".format(header))

  if errors:
    raise BadRequest("\n".join(errors))


def check_export_request_data():
  """ Check request.json structure matches dict(str, list(int)) """
  if type(request.json) is not dict:
    raise BadRequest("export requst data invalid")

  if not all(isinstance(ids, list) for ids in request.json.values()):
    raise BadRequest("export requst data invalid")

  for ids in request.json.values():
    if not all(isinstance(id_, int) for id_ in ids):
      raise BadRequest("export requst data invalid")


def parse_export_request():
  """ Check if request contains all required fields """
  required_headers = {
      "X-Requested-By": ["gGRC"],
      "Content-Type": ["application/json"],
  }
  check_required_headers(required_headers)
  check_export_request_data()

  export_data = {k: v for k, v in request.json.items() if k in IMPORTABLE}
  return export_data


def handle_export_request():

  data = parse_export_request()

  csv_data = []
  for object_name, ids in data.items():
    object_type = IMPORTABLE[object_name]
    converter = Converter.from_ids(object_type, ids)
    csv_data.extend(converter.to_array())
  csv_string = generate_csv_string(csv_data)

  object_names = "_".join(data.keys())
  filename = "{}_template.csv".format(object_names)

  headers = [
      ('Content-Type', 'text/csv'),
      ('Content-Disposition', 'attachment; filename="{}"'.format(filename)),
  ]
  return current_app.make_response((csv_string, 200, headers))


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
  def update_response_data(data, new_data):
    for k, v in new_data.items():
      data[k].extend(v)

  dry_run, csv_data = parse_import_request()
  offsets, data_blocks = split_array(csv_data)

  response_data = []
  new_slugs = defaultdict(set)
  converters = []
  shared_state = {}
  for offset, data in zip(offsets, data_blocks):
    converter = Converter.from_csv(data, offset, dry_run, shared_state)
    converters.append(converter)
    converter.import_objects()
    object_class, slugs = converter.get_new_slugs()
    new_slugs[object_class].update(slugs)

  for converter in converters:
    converter.import_mappings(new_slugs)
    response_data.append(converter.get_info())

  response_json = json.dumps(response_data)
  headers = [('Content-Type', 'application/json')]
  return current_app.make_response((response_json, 200, headers))


def init_converter_views():
  @app.route("/_service/export_csv", methods=['POST'])
  @login_required
  def handle_export_csv():
    return handle_export_request()

  @app.route("/_service/import_csv", methods=['POST'])
  @login_required
  def handle_import_csv():
    return handle_import_request()

  @app.route("/import")
  @login_required
  def import_view():
    return render_template("import_export/import.haml")

  @app.route("/export")
  @login_required
  def export_view():
    return render_template("import_export/export.haml")
