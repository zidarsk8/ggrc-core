# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from collections import namedtuple
from .common import *
from .registry import service

"""All gGRC REST services."""


def all_collections():
  """The list of all gGRC collection services as a list of
  (url, ModelClass) tuples.
  """
  import ggrc.models.all_models as models
  import sys
  from ggrc import settings

  ret = [
    service('tasks', models.Task),
    service('audits', models.Audit),
    service('categorizations', models.Categorization),
    service('category_bases', models.CategoryBase),
      service('control_categories', models.ControlCategory),
      service('control_assertions', models.ControlAssertion),
    service('contexts', models.Context),
    service('controls', models.Control),
    service('control_controls', models.ControlControl),
    service('control_sections', models.ControlSection),
    service('data_assets', models.DataAsset),
    service('directives', models.Directive, ReadOnlyResource),
      service('contracts', models.Contract),
      service('policies', models.Policy),
      service('regulations', models.Regulation),
      service('standards', models.Standard),
    service('directive_controls', models.DirectiveControl),
    service('documents', models.Document),
    service('events', models.Event, ReadOnlyResource),
    service('facilities', models.Facility),
    service('help', models.Help),
    service('markets', models.Market),
    service('meetings', models.Meeting),
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
    service('products', models.Product),
    service('projects', models.Project),
    service('programs', models.Program),
    service('program_controls', models.ProgramControl),
    service('program_directives', models.ProgramDirective),
    service('relationships', models.Relationship),
    service('requests', models.Request),
    service('responses', models.Response),
      service('documentation_responses', models.DocumentationResponse),
      service('interview_responses', models.InterviewResponse),
      service('population_sample_responses', models.PopulationSampleResponse),
    service('revisions', models.Revision, ReadOnlyResource),
    service('sections', models.Section),
    service('section_objectives', models.SectionObjective),
    service('systems_or_processes', models.SystemOrProcess, ReadOnlyResource),
      service('systems', models.System),
      service('processes', models.Process),
    ]

  for extension in settings.EXTENSIONS:
    __import__(extension)
    extension_module = sys.modules[extension]
    if hasattr(extension_module, 'all_collections'):
      entries = extension_module.all_collections
      if callable(entries):
        entries = entries()
      ret.extend(entries)
  return ret

# initialization of GGRC Caching Layer objects
#
def init_ggrc_cache(app):
  from ggrc.cache import CacheManager, Config, Factory, get_cache_manager

  # REVIST: read properties from settings for app like SQLAlchemy and other modules
  defaultproperties={'CACHEMECHANISM':'local'}

  # Create instance of cache manager class for applying policies and operations on cache
  cache_manager = get_cache_manager()

  # Setup config including policies
  config = Config();
  config.setProperties(defaultproperties)
  config.initialize()

  # Setup factory class to allow cache manager to create the cache mechanism objects.
  # REVIST: Rename as BaseFactory instead of Factory
  factory = Factory();

  # Initialize the caching layer
  cache_manager.set_config(config)
  cache_manager.set_factory(factory)
  cache_manager.initialize()
  print "Cache Manager initalized"


def init_all_services(app):
  """Register all gGRC REST services with the Flask application ``app``."""
  from ggrc.login import login_required

  for entry in all_collections():
    entry.service_class.add_to(
      app,
      '/api/{0}'.format(entry.name),
      entry.model_class,
      decorators=(login_required,),
      )

  from .search import search
  app.add_url_rule(
    '/search', 'search', login_required(search))

  from .log_event import log_event
  app.add_url_rule(
    '/api/log_events', 'log_events', log_event, methods=['POST'])

  from .description import ServiceDescription
  app.add_url_rule(
    '/api', view_func=ServiceDescription.as_view('ServiceDescription'))


  # Initialize Caching layer
  init_ggrc_cache(app)

