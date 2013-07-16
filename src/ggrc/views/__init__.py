# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc.app import db, app
from ggrc.rbac import permissions
from werkzeug.exceptions import Forbidden
from .tooltip import TooltipView
from .relationships import RelatedObjectResults
from . import filters
from ggrc.converters.sections import SectionsConverter
from ggrc.converters.import_helper import *
from pprint import pprint
from flask import request, redirect, url_for, flash
from werkzeug import secure_filename
"""ggrc.views
Handle non-RESTful views, e.g. routes which return HTML rather than JSON
"""

@app.context_processor
def base_context():
  from ggrc.models import get_model
  return dict(
      get_model=get_model,
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
  return render_template("styleguide.haml")

def allowed_file(filename):
  return filename.rsplit('.',1)[1] == 'csv'


@app.route("/directives/<directive_id>/import_sections", methods=['GET', 'POST'])
def import_sections(directive_id):

  if request.method == 'POST':
    dry_run = not ('confirm' in request.form)
    csv_file = request.files['file']

    if csv_file and allowed_file(csv_file.filename):
      print "GOING IN WITH DRY_RUN: " + str(dry_run)
      filename = secure_filename(csv_file.filename)
      converter = handle_csv_import(SectionsConverter, csv_file, directive_id = directive_id, dry_run = dry_run)
      if converter.import_exception is None:
        results = converter.final_results
        dummy_data = results
        if not dry_run:
          #FIXME: Flash from the server side does not seem to be working
          flash("Import is done.")
          return redirect('/directives/{}'.format(directive_id))

        return render_template("directives/import.haml",directive_id = directive_id, converter = converter, dummy_data=dummy_data, all_warnings=converter.warnings, all_errors=converter.errors)
      else:
        return render_template("directives/import.haml", directive_id = directive_id, exception_message = str(converter.import_exception))

  return render_template("directives/import.haml", directive_id = directive_id)


@app.route("/directives/<directive_id>/export_sections", methods=['GET', 'POST'])
def export_sections(directive_id):

  if request.method == 'GET':
    handle_converter_csv_export(directive_id, SectionsConverter)

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

