# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from .common import *
from .registry import service

"""All gGRC REST services."""


def contributed_services():
  """The list of all gGRC collection services as a list of
  (url, ModelClass) tuples.
  """
  import ggrc.models.all_models as models

  return [
      service('background_tasks', models.BackgroundTask),
      service('access_groups', models.AccessGroup),
      service('audits', models.Audit),
      service('audit_objects', models.AuditObject),
      service('categorizations', models.Categorization),
      service('category_bases', models.CategoryBase),
      service('control_categories', models.ControlCategory),
      service('control_assertions', models.ControlAssertion),
      service('contexts', models.Context),
      service('controls', models.Control),
      service('control_assessments', models.ControlAssessment),
      service('comments', models.Comment),
      service('custom_attribute_definitions',
              models.CustomAttributeDefinition),
      service('custom_attribute_values', models.CustomAttributeValue),
      service('data_assets', models.DataAsset),
      service('directives', models.Directive, ReadOnlyResource),
      service('contracts', models.Contract),
      service('policies', models.Policy),
      service('regulations', models.Regulation),
      service('standards', models.Standard),
      service('documents', models.Document),
      service('events', models.Event, ReadOnlyResource),
      service('facilities', models.Facility),
      service('help', models.Help),
      service('markets', models.Market),
      service('meetings', models.Meeting),
      service('object_documents', models.ObjectDocument),
      service('object_owners', models.ObjectOwner),
      service('object_people', models.ObjectPerson),
      service('objectives', models.Objective),
      service('options', models.Option),
      service('org_groups', models.OrgGroup),
      service('vendors', models.Vendor),
      service('people', models.Person),
      service('products', models.Product),
      service('projects', models.Project),
      service('programs', models.Program),
      service('relationships', models.Relationship),
      service('requests', models.Request),
      service('responses', models.Response),
      service('documentation_responses', models.DocumentationResponse),
      service('interview_responses', models.InterviewResponse),
      service('population_sample_responses', models.PopulationSampleResponse),
      service('revisions', models.Revision, ReadOnlyResource),
      service('sections', models.Section),
      service('clauses', models.Clause),
      service(
          'systems_or_processes', models.SystemOrProcess, ReadOnlyResource),
      service('systems', models.System),
      service('processes', models.Process),
      service('notification_config', models.NotificationConfig),
      service('issues', models.Issue),
  ]


def all_services():
  from ggrc.extensions import get_extension_modules

  services = contributed_services()

  for extension_module in get_extension_modules():
    contributions = getattr(extension_module, 'contributed_services', None)
    if contributions:
      if callable(contributions):
        contributions = contributions()
      services.extend(contributions)
  return services


def init_extra_services(app):
  from ggrc.login import login_required

  from .search import search
  app.add_url_rule(
      '/search', 'search', login_required(search))

  from .log_event import log_event
  app.add_url_rule(
      '/api/log_events', 'log_events', log_event, methods=['POST'])

  from .description import ServiceDescription
  app.add_url_rule(
      '/api', view_func=ServiceDescription.as_view('ServiceDescription'))


def init_all_services(app):
  """Register all gGRC REST services with the Flask application ``app``."""
  from ggrc.extensions import get_extension_modules
  from ggrc.login import login_required

  for entry in all_services():
    entry.service_class.add_to(
        app,
        '/api/{0}'.format(entry.name),
        entry.model_class,
        decorators=(login_required,),
    )

  init_extra_services(app)
  for extension_module in get_extension_modules():
    ext_extra_services = getattr(extension_module, 'init_extra_services', None)
    if ext_extra_services:
      ext_extra_services(app)
