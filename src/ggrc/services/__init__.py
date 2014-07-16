# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from collections import namedtuple
from .common import *
from .registry import service

"""All gGRC REST services."""


def contributed_services():
  """The list of all gGRC collection services as a list of
  (url, ModelClass) tuples.
  """
  import ggrc.models.all_models as models

  return [
    service('audits', models.Audit),
    service('background_tasks', models.BackgroundTask),
    service('categorizations', models.Categorization),
    service('category_bases', models.CategoryBase),
    service('clauses', models.Clause),
    service('contexts', models.Context),
    service('contracts', models.Contract),
    service('control_assertions', models.ControlAssertion),
    service('control_categories', models.ControlCategory),
    service('control_controls', models.ControlControl),
    service('control_sections', models.ControlSection),
    service('controls', models.Control),
    service('data_assets', models.DataAsset),
    service('directives', models.Directive, ReadOnlyResource),
    service('directive_controls', models.DirectiveControl),
    service('directive_sections', models.DirectiveSection),
    service('documentation_responses', models.DocumentationResponse),
    service('documents', models.Document),
    service('events', models.Event, ReadOnlyResource),
    service('facilities', models.Facility),
    service('help', models.Help),
    service('interview_responses', models.InterviewResponse),
    service('markets', models.Market),
    service('meetings', models.Meeting),
    service('notification_config', models.NotificationConfig),
    service('object_controls', models.ObjectControl),
    service('object_documents', models.ObjectDocument),
    service('object_objectives', models.ObjectObjective),
    service('object_owners', models.ObjectOwner),
    service('object_people', models.ObjectPerson),
    service('object_sections', models.ObjectSection),
    service('objectives', models.Objective),
    service('objective_controls', models.ObjectiveControl),
    service('options', models.Option),
    service('org_groups', models.OrgGroup),
    service('people', models.Person),
    service('policies', models.Policy),
    service('population_sample_responses', models.PopulationSampleResponse),
    service('processes', models.Process),
    service('products', models.Product),
    service('programs', models.Program),
    service('program_controls', models.ProgramControl),
    service('program_directives', models.ProgramDirective),
    service('projects', models.Project),
    service('regulations', models.Regulation),
    service('relationships', models.Relationship),
    service('requests', models.Request),
    service('responses', models.Response),
    service('revisions', models.Revision, ReadOnlyResource),
    service('section_bases', models.SectionBase, ReadOnlyResource),
    service('section_objectives', models.SectionObjective),
    service('sections', models.Section),
    service('standards', models.Standard),
    service('systems', models.System),
    service('systems_or_processes', models.SystemOrProcess, ReadOnlyResource),
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
