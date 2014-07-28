# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: silas@reciprocitylabs.com
# Maintained By: silas@reciprocitylabs.com

from flask import flash, render_template, request, redirect
from werkzeug.exceptions import Forbidden

from ggrc.app import app
from ggrc.converters.common import ImportException
from ggrc.converters.import_helper import handle_csv_import, handle_converter_csv_export
from ggrc.login import get_current_user, login_required
from ggrc.models.background_task import create_task, queued_task
from ggrc.views.converters import allowed_file, import_dump, import_redirect


def import_risk_task(parameters):
  from ggrc_risk_assessment_v2.converters.risks import RiskConverter

  csv_file = parameters.get("csv_file")
  dry_run = parameters.get("dry_run")
  options = {"dry_run": dry_run}
  try:
    converter = handle_csv_import(RiskConverter, csv_file.splitlines(True), **options)
    if dry_run:
      return render_template("risks/import_result.haml", converter=converter, results=converter.objects, heading_map=converter.object_map)
    else:
      count = len(converter.objects)
      flash(u'Successfully imported {} {}'.format(count, "Risk(s)"), 'notice')
      return import_redirect("/risk_admin")

  except ImportException as e:
    if e.show_preview:
      converter = e.converter
      return render_template("risks/import_result.haml", exception_message=e, converter=converter, results=converter.objects, heading_map=converter.object_map)
    return render_template("risks/import_errors.haml", exception_message=e)

def import_risks():
  if request.method != 'POST':
    return render_template("risks/import.haml", import_kind="Risks")

  if 'cancel' in request.form:
    return import_redirect('/risk_admin')
  dry_run = not ('confirm' in request.form)
  csv_file = request.files['file']
  if csv_file and allowed_file(csv_file.filename):
    from werkzeug import secure_filename
    filename = secure_filename(csv_file.filename)
  else:
    file_msg = "Could not import: invalid csv file."
    return render_template("risks/import_errors.haml", exception_message=file_msg)
  parameters = {"dry_run": dry_run, "csv_file": csv_file.read(), "csv_filename": filename, "object_kind": "risks"}
  #tq = create_task(
  #    get_current_user(), "import_risk", import_risk_task, parameters)
  #return tq.make_response(import_dump({"id": tq.id, "status": tq.status}))
  return import_risk_task(parameters)

def risk_import_template():
  from flask import current_app
  filename = "Risk_Import_Template.csv"
  headers = [('Content-Type', 'text/csv'), ('Content-Disposition', 'attachment; filename="{}"'.format(filename))]
  body = render_template("csv_files/" + filename)
  return current_app.make_response((body, 200, headers))


def init_extra_views(app):
  app.add_url_rule(
      "/risks/import", "import_risks",
      view_func=login_required(import_risks),
      methods=['GET', 'POST'])
  app.add_url_rule(
      "/risks/import_template", "risk_import_template",
      view_func=login_required(risk_import_template))
