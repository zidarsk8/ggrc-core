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
      permissions=permissions
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

  # Find all models then remove base classes
  models = set(all_models.all_models) -\
      set([all_models.Directive, all_models.SystemOrProcess])
  for model in models:
    mapper_class = model._sa_class_manager.mapper.base_mapper.class_
    query = model.query.options(
        db.undefer_group(mapper_class.__name__+'_complete'),
        )
    for instance in query.all():
      indexer.create_record(fts_record_for(instance), False)
  db.session.commit()

  return app.make_response((
    'success', 200, [('Content-Type', 'text/html')]))

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


@app.route("/regulations/<directive_id>/import_controls", methods=['GET', 'POST'])
@app.route("/policies/<directive_id>/import_controls", methods=['GET', 'POST'])
@app.route("/contracts/<directive_id>/import_controls", methods=['GET', 'POST'])
def import_controls(directive_id):
  from werkzeug import secure_filename
  from ggrc.converters.controls import ControlsConverter
  from ggrc.converters.import_helper import handle_csv_import
  from ggrc.models import Directive
  import ggrc.views

  directive = Directive.query.get(directive_id)
  directive_url =\
    getattr(ggrc.views, directive.__class__.__name__).url_for(directive)

  if request.method == 'POST':
    if 'cancel' in request.form:
      return import_redirect(directive_url)
    dry_run = not ('confirm' in request.form)
    csv_file = request.files['file']
    try:
      if csv_file and allowed_file(csv_file.filename):
        filename = secure_filename(csv_file.filename)
        options = {}
        options['directive_id'] = directive_id
        options['dry_run'] = dry_run
        converter = handle_csv_import(ControlsConverter, csv_file, **options)
        if dry_run:
          options['converter'] = converter
          options['results'] = converter.objects
          options['heading_map'] = converter.object_map
          return render_template("directives/import_controls_result.haml", **options)
        else:
          count = len(converter.objects)
          flash(u'Successfully imported {} control{}'.format(count, 's' if count > 1 else ''), 'notice')
          return import_redirect(directive_url)
    except ImportException as e:
      return render_template("directives/import_errors.haml",
            directive_id = directive_id, exception_message = str(e))

  return render_template("directives/import.haml", directive_id = directive_id, import_kind = 'Controls')

@app.route("/regulations/<directive_id>/import_sections", methods=['GET', 'POST'])
@app.route("/policies/<directive_id>/import_sections", methods=['GET', 'POST'])
@app.route("/contracts/<directive_id>/import_sections", methods=['GET', 'POST'])
def import_sections(directive_id):
  from werkzeug import secure_filename
  from ggrc.converters.sections import SectionsConverter
  from ggrc.converters.import_helper import handle_csv_import
  from ggrc.models import Directive
  import ggrc.views

  directive = Directive.query.get(directive_id)
  directive_url =\
    getattr(ggrc.views, directive.__class__.__name__).url_for(directive)

  if request.method == 'POST':

    if 'cancel' in request.form:
      return import_redirect(directive_url)
    dry_run = not ('confirm' in request.form)
    csv_file = request.files['file']
    try:
      if csv_file and allowed_file(csv_file.filename):
        filename = secure_filename(csv_file.filename)
        converter = handle_csv_import(SectionsConverter, csv_file,
          directive_id = directive_id, dry_run = dry_run)

        if dry_run:
          return render_template("directives/import_result.haml",directive_id = directive_id,
          converter = converter, results=converter.objects, heading_map = converter.object_map)
        else:
          count = len(converter.objects)
          flash(u'Successfully imported {} section{}'.format(count, 's' if count > 1 else ''), 'notice')
          return import_redirect(directive_url)
    except ImportException as e:
      return render_template("directives/import_errors.haml",
            directive_id = directive_id, exception_message = str(e))

  return render_template("directives/import.haml", directive_id = directive_id, import_kind = 'Sections')


@app.route("/systems/import", methods=['GET', 'POST'])
def import_systems():
  from werkzeug import secure_filename
  from ggrc.converters.systems import SystemsConverter
  from ggrc.converters.import_helper import handle_csv_import

  if request.method == 'POST':
    if 'cancel' in request.form:
      return import_redirect('/admin')
    dry_run = not ('confirm' in request.form)
    csv_file = request.files['file']
    try:
      if csv_file and allowed_file(csv_file.filename):
        filename = secure_filename(csv_file.filename)
        converter = handle_csv_import(SystemsConverter, csv_file, dry_run = dry_run)
        if dry_run:
          return render_template("systems/import_result.haml",
            converter = converter, results=converter.objects, heading_map=converter.object_map)
        else:
          count = len(converter.objects)
          flash(u'Successfully imported {} system{}'.format(count, 's' if count > 1 else ''), 'notice')
          return import_redirect("/admin")
    except ImportException as e:
      return render_template("directives/import_errors.haml", exception_message = str(e))

  return render_template("systems/import.haml", import_kind = 'Systems')

def import_redirect(location):
  # The textarea here is a custom response for 'remoteipart' to
  # proxy a JSON response through an iframe.
  return app.make_response((
    '<textarea data-type="application/json" response-code="200">{0}</textarea>'.format(
      json.dumps({ 'location': location })), 200, [('Content-Type', 'text/html')]))


@app.route("/processes/import", methods=['GET', 'POST'])
def import_processes():
  from werkzeug import secure_filename
  from ggrc.converters.systems import SystemsConverter
  from ggrc.converters.import_helper import handle_csv_import

  if request.method == 'POST':
    if 'cancel' in request.form:
      return import_redirect('/admin')
    dry_run = not ('confirm' in request.form)
    csv_file = request.files['file']
    try:
      if csv_file and allowed_file(csv_file.filename):
        filename = secure_filename(csv_file.filename)
        converter = handle_csv_import(SystemsConverter, csv_file, dry_run = dry_run, is_biz_process='1')
        if dry_run:
          return render_template("systems/import_result.haml",
            converter = converter, results=converter.objects, heading_map=converter.object_map)
        else:
          count = len(converter.objects)
          flash(u'Successfully imported {} process{}'.format(count, 'es' if count > 1 else ''), 'notice')
          return import_redirect("/admin")
    except ImportException as e:
      return render_template("directives/import_errors.haml", exception_message = str(e))

  return render_template("systems/import.haml", import_kind = 'Processes')

@app.route("/processes/export", methods=['GET'])
def export_processes():
  from ggrc.converters.systems import SystemsConverter
  from ggrc.converters.import_helper import handle_converter_csv_export
  from ggrc.models.all_models import Process

  options = {}
  options['export'] = True
  options['is_biz_process'] = '1'
  procs = Process.query.all()
  filename = "PROCESSES.csv"
  return handle_converter_csv_export(filename, procs, SystemsConverter, **options)

@app.route("/systems/export", methods=['GET'])
def export_systems():
  from ggrc.converters.systems import SystemsConverter
  from ggrc.converters.import_helper import handle_converter_csv_export
  from ggrc.models.all_models import System

  options = {}
  options['export'] = True
  systems = System.query.filter_by(is_biz_process=False).all()
  filename = "SYSTEMS.csv"
  return handle_converter_csv_export(filename, systems, SystemsConverter, **options)

@app.route("/regulations/<directive_id>/export_sections", methods=['GET'])
@app.route("/policies/<directive_id>/export_sections", methods=['GET'])
@app.route("/contracts/<directive_id>/export_sections", methods=['GET'])
def export_sections(directive_id):
  from ggrc.converters.sections import SectionsConverter
  from ggrc.converters.import_helper import handle_converter_csv_export
  from ggrc.models.all_models import Directive

  options = {}
  directive = Directive.query.filter_by(id=int(directive_id)).first()
  options['directive'] = directive
  options['export'] = True
  filename = "{}.csv".format(directive.slug)
  return handle_converter_csv_export(filename, directive.sections, SectionsConverter, **options)

@app.route("/regulations/<directive_id>/export_sections", methods=['GET'])
@app.route("/policies/<directive_id>/export_sections", methods=['GET'])
@app.route("/contracts/<directive_id>/export_sections", methods=['GET'])
def export_controls(directive_id):
  from ggrc.converters.controls import ControlsConverter
  from ggrc.converters.import_helper import handle_converter_csv_export
  from ggrc.models.all_models import Directive

  options = {}
  directive = Directive.query.filter_by(id=int(directive_id)).first()
  options['directive'] = directive
  options['export'] = True
  filename = "{}-controls.csv".format(directive.slug)
  return handle_converter_csv_export(filename, directive.controls, ControlsConverter, **options)

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
      'contracts',
      'policies',
      'regulations',
      'cycles',
      'controls',
      'objectives',
      'systems',
      'processes',
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
      'contracts',
      'policies',
      'regulations',
      'cycles',
      'controls',
      'objectives',
      'systems',
      'processes',
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

