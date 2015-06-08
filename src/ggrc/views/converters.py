# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from flask import current_app
from flask import request
from werkzeug.exceptions import BadRequest

from ggrc.app import app
from ggrc.login import login_required
from ggrc.converters import IMPORTABLE
from ggrc.converters.base import Converter
from ggrc.converters.import_helper import generate_csv_string


def check_required_headers(required_headers):
  errors = []
  for header, valid_values in required_headers.items():
    if header not in request.headers:
      errors.append("Missing required header '{}'".format(header))
    elif request.headers[header] not in valid_values:
      errors.append("Invalid header value for '{}'".format(header))


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
      "Content-Type": "application/json"
  }

  header_errors = check_required_headers(required_headers)
  if header_errors:
    raise BadRequest("\n".join(header_errors))
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
      ('Content-Disposition', 'attachment; filename="{}"'.format(filename))
  ]

  return current_app.make_response((csv_string, 200, headers))



def init_converter_views():
  @app.route("/_service/export_csv", methods=['POST'])
  @login_required
  def export_csv():
    return handle_export_request()
