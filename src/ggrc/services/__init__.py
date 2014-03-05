# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from collections import namedtuple
from .common import *
from .registry import service
from ggrc.cache import CacheManager, Config, Factory, get_cache_manager

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
def update_cache_before_flush(session, flush_context, objects):
  current_app.logger.info("Entering update_cache_before_flush")
  cache_manager = get_cache_manager()
  """
  Before the flush happens, we can still access to-be-deleted objects, so
  record JSON for log here
  """
  for o in session.new:
    if hasattr(o, 'log_json'):
      cache_manager.new[o] = 'marked for add'
  for o in session.deleted:
    if hasattr(o, 'log_json'):
      cache_manager.deleted[o] = 'marked for delete'
  dirty = set(o for o in session.dirty if session.is_modified(o))
  for o in dirty - set(cache_manager.new) - set(cache_manager.deleted):
    if hasattr(o, 'log_json'):
      cache_manager.dirty[o] = 'marked for update'

  """
  REVISIT: Update local or mem cache state that the object is marked for delete or update ONLY   
  The session.new entries are ignored
  """

def update_cache_after_flush(session, flush_context):
  current_app.logger.info("Entering update_cache_after_flush")
  cache_manager = get_cache_manager()
  """
  After the flush, we know which objects were actually deleted, not just
  modified (deletes due to cascades are not known pre-flush), so fix up
  cache.
  """
  for o in cache_manager.dirty.keys():
    # SQLAlchemy magic to determine whether object was actually deleted due
    #   to `cascade="all,delete-orphan"`
     # If an object was actually deleted, move it into `deleted`
    if flush_context.is_deleted(o._sa_instance_state):
      cache_manager.deleted[o] = cache_manager.dirty[o]
      del cache_manager.dirty[o]

  """
  Update local or mem cache 
  """
  if len(cache_manager.new) > 0: 
    items_to_add = cache_manager.new.items()
    for o, json_obj in items_to_add:
      json_obj = o.log_json()
      cls = o.__class__.__name__
      if cache_manager.supported_classes.has_key(cls):
        model_plural = cache_manager.supported_classes[cls]
        # REVISIT Handle the cache expiry of mapping creation, mark source and destination for deletion
        # 
        current_app.logger.info("CACHE: Adding new object instance of model: " + cls + \
          " resource type: " + cache_manager.supported_classes[cls])
        key = 'collection:' + model_plural + ':' + str(json_obj['id'])
        cache_manager.marked_for_add[key]=json_obj

    # REVISIT: before_flush and after_flush reentrancy issues?
    #
    for o, json_obj in items_to_add:
      del cache_manager.new[o]
      
  if len(cache_manager.dirty) > 0: 
    items_to_update = cache_manager.dirty.items()
    for o, json_obj in items_to_update:
      json_obj = o.log_json()
      cls = o.__class__.__name__
      if cache_manager.supported_classes.has_key(cls):
        model_plural = cache_manager.supported_classes[cls]
        current_app.logger.info("CACHE: Updating object instance of model: " + cls + \
            " resource type: " + cache_manager.supported_classes[cls])
        key = 'collection:' + model_plural + ':' + str(json_obj['id'])
        cache_manager.marked_for_update[key]=json_obj

    # REVISIT: before_flush and after_flush reentrancy issues?
    #
    for o, json_obj in items_to_update:
      del cache_manager.dirty[o]

  if len(cache_manager.deleted) > 0: 
    items_to_delete=cache_manager.deleted.items()
    for o, json_obj in items_to_delete:
      cls = o.__class__.__name__
      if cache_manager.supported_classes.has_key(cls):
        model_plural = cache_manager.supported_classes[cls]
        current_app.logger.info("CACHE: Deleting object instance of model: " + cls + \
          " resource type: " + cache_manager.supported_classes[cls]) 
        key = 'collection:' + model_plural + ':' + str(json_obj['id'])
        stubs = 'stubs:' + model_plural + ':' + str(json_obj['id'])
        # json_obj is passed for cache_manager but it may not be used for delete operation in cache
        #
        cache_manager.marked_for_delete[key]=json_obj
        cache_manager.marked_for_delete[stubs]=json_obj

    # REVISIT: before_flush and after_flush reentrancy issues?
    #
    for o, json_obj in items_to_delete:
      del cache_manager.deleted[o]

def clear_cache(session):
  current_app.logger.info("Entering clear_cache")
  cache_manager = get_cache_manager()
  cache_manager.clear_cache()

def sync_cache(session):
  current_app.logger.info("Entering sync_cache")
  cache_manager = get_cache_manager()
  current_app.logger.info("CACHE: sync cache");
  current_app.logger.info("CACHE: objects marked for add in cache");
  for key, data in cache_manager.marked_for_add.items():
    current_app.logger.info("CACHE: key: " + key + " : data: " + str(data))
  current_app.logger.info("CACHE: objects marked for update in cache");
  for key, data in cache_manager.marked_for_update.items():
    current_app.logger.info("CACHE: key: " + key + " data: " + str(data))
  current_app.logger.info("CACHE: objects marked for delete in cache");
  for key, data in cache_manager.marked_for_delete.items():
    current_app.logger.info("CACHE: key: " + key + " data: " + str(data))
  
  cache_manager.clear_cache()

def init_ggrc_cache(app):
  # REVIST: read properties from settings for app similar to SQLAlchemy and other modules
  #defaultproperties={'CACHEMECHANISM':'local,memcache'}
  defaultproperties={'CACHEMECHANISM':'memcache'}
  #defaultproperties={'CACHEMECHANISM':'local'}
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
  event.listen(Session, 'before_flush',update_cache_before_flush)
  event.listen(Session, 'after_flush', update_cache_after_flush)
  event.listen(Session, 'after_commit', sync_cache)
  event.listen(Session, 'after_rollback', clear_cache)
  cache_manager.initialize()


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

