# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

import json

from ggrc.app import db, app
from ggrc.rbac import permissions
from werkzeug.exceptions import Forbidden
from .tooltip import TooltipView
from .relationships import RelatedObjectResults
from . import filters
from flask import request, redirect, url_for, flash, session
from ggrc.converters.common import ImportException
from ggrc.converters.sections import SectionsConverter
from ggrc.converters.controls import ControlsConverter
"""ggrc.views
Handle non-RESTful views, e.g. routes which return HTML rather than JSON
"""

def get_permissions_json():
  return json.dumps(session['permissions'])

@app.context_processor
def base_context():
  from ggrc.models import get_model
  return dict(
      get_model=get_model,
      permissions_json=get_permissions_json,
      )

from flask import render_template

# Actual HTML-producing routes
#

@app.route("/")
def index():
  """The initial entry point of the app
  """
  return render_template("welcome/index.haml")

from ggrc.login import login_required

@app.route("/dashboard")
@login_required
def dashboard():
  """The dashboard page
  """
  return render_template("dashboard/index.haml")

@app.route("/admin/reindex", methods=["POST"])
@login_required
def admin_reindex():
  """Simple re-index of all indexable objects
  """
  if not permissions.is_allowed_read("/admin", 1):
    raise Forbidden()

  from ggrc.fulltext import get_indexer
  from ggrc.fulltext.recordbuilder import fts_record_for

  indexer = get_indexer()
  indexer.delete_all_records(False)

  from ggrc.models import all_models
  from ggrc.app import db

  models = set(all_models.all_models) - set([all_models.LogEvent])
  for model in models:
    for instance in model.query.all():
      indexer.create_record(fts_record_for(instance), False)
  db.session.commit()

  return redirect(url_for('admin'))

@app.route("/admin")
@login_required
def admin():
  """The admin dashboard page
  """
  if not permissions.is_allowed_read("/admin", 1):
    raise Forbidden()
  return render_template("admin/index.haml")

@app.route("/design")
@login_required
def styleguide():
  """The style guide page
  """
  return render_template("styleguide/styleguide.haml")

def allowed_file(filename):
  return filename.rsplit('.',1)[1] == 'csv'


@app.route("/directives/<directive_id>/import_controls", methods=['GET', 'POST'])
def import_controls(directive_id):
  from werkzeug import secure_filename
  from ggrc.converters.controls import ControlsConverter
  from ggrc.converters.import_helper import handle_csv_import

  if request.method == 'POST':
    if 'cancel' in request.form:
      return import_redirect(directive_id)
    dry_run = not ('confirm' in request.form)
    csv_file = request.files['file']
    try:
      if csv_file and allowed_file(csv_file.filename):
        filename = secure_filename(csv_file.filename)
        converter = handle_csv_import(ControlsConverter, csv_file,
          directive_id = directive_id, dry_run = dry_run,)

        if dry_run:
          return render_template("directives/import_controls_result.haml",directive_id = directive_id,
          converter = converter, results=converter.objects, heading_map = converter.object_map)
        else:
          return import_redirect(directive_id)
    except ImportException as e:
      return render_template("directives/import_errors.haml",
            directive_id = directive_id, exception_message = str(e))

  return render_template("directives/import.haml", directive_id = directive_id)

@app.route("/directives/<directive_id>/import_sections", methods=['GET', 'POST'])
def import_sections(directive_id):
  from werkzeug import secure_filename
  from ggrc.converters.sections import SectionsConverter
  from ggrc.converters.import_helper import handle_csv_import

  if request.method == 'POST':

    if 'cancel' in request.form:
      return import_redirect(directive_id)
    dry_run = not ('confirm' in request.form)
    csv_file = request.files['file']
    try:
      if csv_file and allowed_file(csv_file.filename):
        filename = secure_filename(csv_file.filename)
        converter = handle_csv_import(SectionsConverter, csv_file,
          directive_id = directive_id, dry_run = dry_run,)

        if dry_run:
          return render_template("directives/import_result.haml",directive_id = directive_id,
          converter = converter, results=converter.objects, heading_map = converter.object_map)
        else:
          return import_redirect(directive_id)
    except ImportException as e:
      return render_template("directives/import_errors.haml",
            directive_id = directive_id, exception_message = str(e))

  return render_template("directives/import.haml", directive_id = directive_id)


def import_redirect(directive_id):
  # The textarea here is a custom response for 'remoteipart' to
  # proxy a JSON response through an iframe.
  return app.make_response((
    '<textarea data-type="application/json" response-code="200">{0}</textarea>'.format(
      json.dumps({ 'location': '/directives/{0}'.format(directive_id) })),
    200,
    [('Content-Type', 'text/html')]))



@app.route("/directives/<directive_id>/export_sections", methods=['GET', 'POST'])
def export_sections(directive_id):
  from ggrc.converters.sections import SectionsConverter
  from ggrc.converters.import_helper import handle_converter_csv_export

  if request.method == 'GET':
    return handle_converter_csv_export(directive_id, SectionsConverter)
  return redirect('directives/{}'.format(directive_id))

@app.route("/directives/<directive_id>/export_controls", methods=['GET', 'POST'])
def export_controls(directive_id):
  from ggrc.converters.controls import ControlsConverter
  from ggrc.converters.import_helper import handle_converter_csv_export

  if request.method == 'GET':
    return handle_converter_csv_export(directive_id, ControlsConverter)
  return redirect('directives/{}'.format(directive_id))

def _all_views(view_list):
  import ggrc.services
  collections = dict(
      [(e.name, e.model_class) for e in ggrc.services.all_collections()])

  def with_model(object_plural):
    return (object_plural, collections.get(object_plural))

  return map(with_model, view_list)

def all_object_views():
  return _all_views([
      'programs',
      'directives',
      'cycles',
      'controls',
      'objectives',
      'systems',
      'products',
      'org_groups',
      'facilities',
      'markets',
      'projects',
      'data_assets',
      'risky_attributes',
      'risks',
      'people',
      'pbc_lists',
      'roles',
      ])

def all_tooltip_views():
  return _all_views([
      'programs',
      'directives',
      'cycles',
      'controls',
      'objectives',
      'systems',
      'products',
      'org_groups',
      'facilities',
      'markets',
      'projects',
      'data_assets',
      'risky_attributes',
      'risks',
      'people',
      'events',
      ])

def init_all_object_views(app):
  import sys
  from ggrc import settings
  from .common import BaseObjectView

  for k,v in all_object_views():
    BaseObjectView.add_to(
      app, '/{0}'.format(k), v, decorators=(login_required,))

  for k,v in all_tooltip_views():
    TooltipView.add_to(
      app, '/{0}'.format(k), v, decorators=(login_required,))

  if hasattr(settings, 'EXTENSIONS'):
    for extension in settings.EXTENSIONS:
      __import__(extension)
      extension_module = sys.modules[extension]
      if hasattr(extension_module, 'initialize_all_object_views'):
        extension_module.initialize_all_object_views(app)

