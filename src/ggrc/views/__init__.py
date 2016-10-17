# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""ggrc.views
Handle non-RESTful views, e.g. routes which return HTML rather than JSON
"""

import collections
import json

from flask import flash
from flask import g
from flask import render_template
from flask import url_for
from werkzeug.exceptions import Forbidden

from ggrc import models
from ggrc import settings
from ggrc.app import app
from ggrc.app import db
from ggrc.builder.json import publish
from ggrc.builder.json import publish_representation
from ggrc.converters import get_importables, get_exportables
from ggrc.extensions import get_extension_modules
from ggrc.fulltext import get_indexer
from ggrc.fulltext.recordbuilder import fts_record_for
from ggrc.fulltext.recordbuilder import model_is_indexed
from ggrc.login import get_current_user
from ggrc.login import login_required
from ggrc.models import all_models
from ggrc.models.background_task import create_task
from ggrc.models.background_task import make_task_response
from ggrc.models.background_task import queued_task
from ggrc.models.reflection import AttributeInfo
from ggrc.rbac import permissions
from ggrc.services.common import as_json
from ggrc.services.common import inclusion_filter
from ggrc.services import query as services_query
from ggrc.views import converters
from ggrc.views import cron
from ggrc.views import filters
from ggrc.views import mockups
from ggrc.views import notifications
from ggrc.views.common import RedirectedPolymorphView
from ggrc.views.registry import object_view
from ggrc.utils import benchmark


# Needs to be secured as we are removing @login_required

@app.route("/_background_tasks/reindex", methods=["POST"])
@queued_task
def reindex(_):
  """
  Web hook to update the full text search index
  """

  do_reindex()

  return app.make_response((
      'success', 200, [('Content-Type', 'text/html')]))


def do_reindex():
  """
  update the full text search index
  """

  indexer = get_indexer()
  indexer.delete_all_records(False)

  # Remove model base classes and non searchable objects
  excluded_models = {
      all_models.Directive,
      all_models.Option,
      all_models.SystemOrProcess
  }
  indexed_models = {model for model in all_models.all_models
                    if model_is_indexed(model)}

  indexed_models -= excluded_models

  for model in indexed_models:
    mapper_class = model._sa_class_manager.mapper.base_mapper.class_
    query = model.query.options(
        db.undefer_group(mapper_class.__name__ + '_complete'),
    )
    for query_chunk in generate_query_chunks(query):
      for instance in query_chunk:
        indexer.create_record(fts_record_for(instance), False)
      db.session.commit()


def get_permissions_json():
  """Get all permissions for current user"""
  with benchmark("Get permission JSON"):
    permissions.permissions_for(permissions.get_user())
    return json.dumps(getattr(g, '_request_permissions', None))


def get_config_json():
  """Get public app config"""
  with benchmark("Get config JSON"):
    public_config = dict(app.config.public_config)
    for extension_module in get_extension_modules():
      if hasattr(extension_module, 'get_public_config'):
        public_config.update(
            extension_module.get_public_config(get_current_user()))
    return json.dumps(public_config)


def get_full_user_json():
  """Get the full current user"""
  with benchmark("Get full user JSON"):
    from ggrc.models.person import Person
    current_user = get_current_user()
    person = Person.eager_query().filter_by(id=current_user.id).one()
    result = publish_representation(publish(person, (), inclusion_filter))
    return as_json(result)


def get_current_user_json():
  """Get current user"""
  with benchmark("Get current user JSON"):
    person = get_current_user()
    return as_json({
        "id": person.id,
        "company": person.company,
        "email": person.email,
        "language": person.language,
        "name": person.name,
        "system_wide_role": person.system_wide_role,
    })


def get_attributes_json():
  """Get a list of all custom attribute definitions"""
  with benchmark("Get attributes JSON"):
    attrs = models.CustomAttributeDefinition.eager_query().filter(
        models.CustomAttributeDefinition.definition_id.is_(None)
    )
    published = []
    for attr in attrs:
      published.append(publish(attr))
    published = publish_representation(published)
    return as_json(published)


def get_import_types(export_only=False):
  types = get_exportables if export_only else get_importables
  data = []
  for model in set(types().values()):
    data.append({
        "model_singular": model.__name__,
        "title_plural": model._inflector.title_plural
    })
  data.sort()
  response_json = json.dumps(data)
  return response_json


def get_export_definitions():
  with benchmark("Get export definitions"):
    return get_import_types(export_only=True)


def get_import_definitions():
  with benchmark("Get import definitions"):
    return get_import_types(export_only=False)


def get_all_attributes_json(load_custom_attributes=False):
  """Get a list of all attribute definitions

  This exports all attributes related to a given model, including custom
  attributes and mapping attributes, that are used in csv import and export.
  """
  with benchmark('Loading all attributes JSON'):
    published = {}
    ca_cache = collections.defaultdict(list)
    if load_custom_attributes:
      definitions = models.CustomAttributeDefinition.eager_query().group_by(
          models.CustomAttributeDefinition.title,
          models.CustomAttributeDefinition.definition_type)
      for attr in definitions:
        ca_cache[attr.definition_type].append(attr)
    for model in all_models.all_models:
      published[model.__name__] = \
          AttributeInfo.get_attr_definitions_array(model, ca_cache=ca_cache)
    return as_json(published)


@app.context_processor
def base_context():
  """Gets the base context"""
  return dict(
      get_model=models.get_model,
      permissions_json=get_permissions_json,
      permissions=permissions,
      config_json=get_config_json,
      current_user_json=get_current_user_json,
      full_user_json=get_full_user_json,
      attributes_json=get_attributes_json,
      all_attributes_json=get_all_attributes_json,
      import_definitions=get_import_definitions,
      export_definitions=get_export_definitions,
  )


# Actual HTML-producing routes
#


@app.route("/")
def index():
  """The initial entry point of the app
  """
  if not settings.PRODUCTION:
    flash(u"""<b>WARNING</b> - This is not the production instance
              of the GGRC application.<br><br>
              Company confidential, sensitive or personally identifiable
              information <b>*MUST NOT*</b> be entered or stored here.
              For any questions, please contact your administrator.""",
          "alert alert-warning")
  about_url = getattr(settings, "ABOUT_URL", None)
  about_text = getattr(settings, "ABOUT_TEXT", "About gGRC")
  return render_template(
      "welcome/index.haml",
      about_url=about_url,
      about_text=about_text,
  )


@app.route("/dashboard")
@login_required
def dashboard():
  """The dashboard page
  """
  return render_template("dashboard/index.haml")


@app.route("/objectBrowser")
@login_required
def objectBrowser():
  """The object Browser page
  """
  return render_template("dashboard/index.haml")


def generate_query_chunks(query):
  """Generate query chunks used by pagination"""
  chunk_size = 100
  count = query.count()
  for offset in range(0, count, chunk_size):
    yield query.order_by('id').limit(chunk_size).offset(offset).all()


@app.route("/admin/reindex", methods=["POST"])
@login_required
def admin_reindex():
  """Calls a webhook that reindexes indexable objects
  """
  if not permissions.is_allowed_read("/admin", None, 1):
    raise Forbidden()
  task_queue = create_task("reindex", url_for(reindex.__name__), reindex)
  return task_queue.make_response(
      app.make_response(("scheduled %s" % task_queue.name, 200,
                         [('Content-Type', 'text/html')])))


@app.route("/admin")
@login_required
def admin():
  """The admin dashboard page
  """
  if not permissions.is_allowed_read("/admin", None, 1):
    raise Forbidden()
  return render_template("admin/index.haml")


@app.route("/assessments_view")
@login_required
def assessments_view():
  """The clutter-free list of all Person's Assessments"""
  return render_template("assessments_view/index.haml")


@app.route("/background_task/<id_task>", methods=['GET'])
def get_task_response(id_task):
  """Gets the status of a background task"""
  return make_task_response(id_task)


def contributed_object_views():
  """Contributed object views"""

  return [
      object_view(models.BackgroundTask),
      object_view(models.Program),
      object_view(models.Audit),
      object_view(models.Directive, RedirectedPolymorphView),
      object_view(models.Contract),
      object_view(models.Policy),
      object_view(models.Regulation),
      object_view(models.Standard),
      object_view(models.Clause),
      object_view(models.Section),
      object_view(models.Control),
      object_view(models.Assessment),
      object_view(models.AssessmentTemplate),
      object_view(models.Objective),
      object_view(models.System),
      object_view(models.Process),
      object_view(models.Product),
      object_view(models.Request),
      object_view(models.OrgGroup),
      object_view(models.Facility),
      object_view(models.Market),
      object_view(models.Project),
      object_view(models.DataAsset),
      object_view(models.AccessGroup),
      object_view(models.Person),
      object_view(models.Vendor),
      object_view(models.Issue),
  ]


def all_object_views():
  """Gets all object views defined in the application"""
  views = contributed_object_views()

  for extension_module in get_extension_modules():
    contributions = getattr(extension_module, "contributed_object_views", None)
    if contributions:
      if callable(contributions):
        contributions = contributions()
      views.extend(contributions)

  return views


def init_extra_views(app_):
  """Init any extra views needed by the app

  This should be used for any views that might use extension modules.
  """
  mockups.init_mockup_views()
  filters.init_filter_views()
  converters.init_converter_views()
  cron.init_cron_views(app_)
  notifications.init_notification_views(app_)
  services_query.init_query_view(app_)


def init_all_views(app_):
  """Inits all views defined in the core module and submodules"""
  for entry in all_object_views():
    entry.service_class.add_to(
        app_,
        '/{0}'.format(entry.url),
        entry.model_class,
        decorators=(login_required,)
    )

  init_extra_views(app_)
  for extension_module in get_extension_modules():
    ext_extra_views = getattr(extension_module, "init_extra_views", None)
    if ext_extra_views:
      ext_extra_views(app_)


@app.route("/permissions")
@login_required
def user_permissions():
  '''Permissions object for the currently
     logged in user
  '''
  return get_permissions_json()



@app.route("/perf_test", methods=["GET"])
@login_required
def perf_test():
  """Run and display performance tests."""
  import perf_test
  from flask import request
  n = int(request.args.get("n", 10))
  response = perf_test.run_all(n)
  return response, 200, {'Content-Type': 'text/plain; charset=utf-8'}
