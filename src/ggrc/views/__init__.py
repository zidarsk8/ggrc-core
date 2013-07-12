# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc.app import db, app
from .tooltip import TooltipView
from .relationships import RelatedObjectResults
from . import filters
from ggrc.converters.sections import SectionsConverter
from pprint import pprint
from flask import request, redirect, url_for
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

@app.route("/admin/events")
@login_required
def admin_events():
  """The page showing events and revisions
  """
  return render_template("admin/events.haml")

@app.route("/admin")
@login_required
def admin():
  """The admin dashboard page
  """
  return render_template("admin/index.haml")

@app.route("/design")
@login_required
def styleguide():
  """The style guide page
  """
  return render_template("styleguide.haml")

@app.route("/testimport")
def testImport():
  """ create route to test import/export HAMLs for directives
  """
  return render_template("directives/import.haml")


@app.route("/testrender")
def testRender():
  """ create route to test rendering of HAMLs for directives
  """
  converter = SectionsConverter.start_import("/vagrant/extras/Import_Test-Regulations_Legal.csv")
  if converter.import_exception is None:
    results = converter.final_results
    return render_template("directives/import_result_errors.haml",converter = converter, dummy_data=results, all_warnings=converter.warnings, all_errors=converter.errors)
  else:
    return render_template("directives/import_errors.haml", converter=converter, exception_message = str(converter.import_exception))


def allowed_file(filename):
  return filename.rsplit('.',1)[1] == 'csv'


@app.route("/directives/<directive_id>/import_sections", methods=['GET', 'POST'])
def import_sections(directive_id):

  if request.method == 'POST':
    dry_run = 'confirm' in request.form
    csv_file = request.files['file']
    if csv_file and allowed_file(csv_file.filename):
      filename = secure_filename(csv_file.filename)
      converter = SectionsConverter.start_import(csv_file, directive_id = directive_id, dry_run = dry_run)
      if converter.import_exception is None:
        results = converter.final_results
        dummy_data = results
        return render_template("directives/import.haml",directive_id = directive_id, converter = converter, dummy_data=dummy_data, all_warnings=converter.warnings, all_errors=converter.errors)
      else:
        return render_template("directives/import.haml", exception_message = str(converter.import_exception))

  return render_template("directives/import.haml")

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

