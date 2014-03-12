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

def update_cache_before_flush(session, flush_context, objects):
  current_app.logger.info("CACHE: Entering updating cache before flush")
  cache_manager = get_cache_manager()

  """
  Before the flush happens, populate intermediate data structures (dict)
  and actual marking for add, delete and updates are done in session event listenerafter_flush 
  """
  for o in session.new:
    if hasattr(o, 'log_json'):
      cache_manager.new[o] = o.log_json()
  for o in session.deleted:
    if hasattr(o, 'log_json'):
      cache_manager.deleted[o] = o.log_json()
  dirty = set(o for o in session.dirty if session.is_modified(o))
  for o in dirty - set(cache_manager.new) - set(cache_manager.deleted):
    if hasattr(o, 'log_json'):
      cache_manager.dirty[o] = o.log_json()

def update_cache_after_flush(session, flush_context):
  current_app.logger.info("CACHE: Entering updating cache after flush")
  cache_manager = get_cache_manager()

  """ update cache during session event after_flush
  After the flush, we know which objects were actually deleted, not just
  modified (deletes due to cascades are not known pre-flush), so fix up
  cache.
  Args:
    session: SQLAlchemy Session object
    flush_context: context of flush including states
  Returns:
    None 
  """
  for o in cache_manager.dirty.keys():
    # SQLAlchemy magic to determine whether object was actually deleted due
    #   to `cascade="all,delete-orphan"`
     # If an object was actually deleted, move it into `deleted`
    if flush_context.is_deleted(o._sa_instance_state):
      cache_manager.deleted[o] = cache_manager.dirty[o]
      del cache_manager.dirty[o]

  """
  Mark add, update and delete entries and commits to cache (memcache) will be done in session commit event listener
  """
  if len(cache_manager.new) > 0: 
    items_to_add = cache_manager.new.items()
    for o, json_obj in items_to_add:
      json_obj = o.log_json()
      cls = o.__class__.__name__
      if cache_manager.supported_classes.has_key(cls):
        model_plural = cache_manager.supported_classes[cls]
        # Marking object to be added to cache
        key = 'collection:' + model_plural + ':' + str(json_obj['id'])
        cache_manager.marked_for_add[key]=json_obj

        # Marking stubs to be expired from cache instead of appending to end of the list
        stubs_key = 'stubs:' + model_plural + ':0' 
        cache_manager.marked_for_delete.append(stubs_key)

        # Marking mapping links to be deleted from cache
        if cache_manager.supported_mappings.has_key(cls):
          (model, cls, srctype, srcname, dsttype, dstname, polymorph, cachetype) = \
                   cache_manager.supported_mappings[cls]
          srcid  = json_obj[srcname] 
          dstid = json_obj[dstname] 
          model_plural = None
          if polymorph is True:
            dsttype = json_obj[dsttype]
            model_plural = cache_manager.supported_classes[dsttype]
          else:
            model_plural = dsttype
          if srctype is not None:
            from_key = 'collection:' + srctype + ':' + str(srcid)
            cache_manager.marked_for_delete.append(from_key)
          if model_plural is not None:
            to_key   = 'collection:' + model_plural + ':' + str(dstid)
            cache_manager.marked_for_delete.append(to_key)
          else:
            # This error should not happen, it indicates that class is not in the supported_classes map
            # Log error
            current_app.logger.error("CACHE: destination class : " + dsttype + " is not supported for caching") 

    for o, json_obj in items_to_add:
      del cache_manager.new[o]
      
  if len(cache_manager.dirty) > 0: 
    items_to_update = cache_manager.dirty.items()
    for o, json_obj in items_to_update:
      json_obj = o.log_json()
      cls = o.__class__.__name__
      if cache_manager.supported_classes.has_key(cls):
        model_plural = cache_manager.supported_classes[cls]
        current_app.logger.info("CACHE: Marking cache updates for object instance of model: " + cls + \
            " resource type: " + cache_manager.supported_classes[cls])
        # Marking object to updated in cache
        #
        key = 'collection:' + model_plural + ':' + str(json_obj['id'])
        cache_manager.marked_for_update[key]=json_obj

    for o, json_obj in items_to_update:
      del cache_manager.dirty[o]

  if len(cache_manager.deleted) > 0: 
    items_to_delete=cache_manager.deleted.items()
    for o, json_obj in items_to_delete:
      cls = o.__class__.__name__
      if cache_manager.supported_classes.has_key(cls):
        model_plural = cache_manager.supported_classes[cls]
        # Marking object to deleted from cache
        #
        object_key = 'collection:' + model_plural + ':' + str(json_obj['id'])
        cache_manager.marked_for_delete.append(object_key)

        # Marking stubs to be expired from cache instead of deleting it from the list
        #
        stubs_key = 'stubs:' + model_plural + ':0'
        cache_manager.marked_for_delete.append(stubs_key)

        # Marking mapping links to be deleted from cache
        #
        if cache_manager.supported_mappings.has_key(cls):
          (model, cls, srctype, srcname, dsttype, dstname, polymorph, cachetype) = \
                   cache_manager.supported_mappings[cls]
          srcid  = json_obj[srcname] 
          dstid = json_obj[dstname] 
          model_plural = None
          if polymorph is True:
            dsttype = json_obj[dsttype]
            model_plural = cache_manager.supported_classes[dsttype]
          else:
            model_plural = dsttype
          if srctype is not None:
            from_key = 'collection:' + srctype + ':' + str(srcid)
            cache_manager.marked_for_delete.append(from_key)
          if model_plural is not None:
            to_key   = 'collection:' + model_plural + ':' + str(dstid)
            cache_manager.marked_for_delete.append(to_key)
          else:
            # This error should not happen, it indicates that class is not in the supproted_classes map
            # Log error
            current_app.logger.error("CACHE: destination class : " + dsttype + " is not supported for caching") 

    for o, json_obj in items_to_delete:
      del cache_manager.deleted[o]

def clear_cache(session):
  """
  Clean up any cache items related to a session
  Args:
    session: SQLAlchemy session object
  Returns:
    None 
  """
  current_app.logger.info("Entering clear_cache")
  cache_manager = get_cache_manager()

  cache_manager.clear_cache()

def build_status_cache(data, key, timestamp, status):
  """
  build the status cache dictionary
  Args:
    data: dictionary to update
    key: key to dictionary
    timestamp: update timestamp entry 
    status: Update status entry, e.g.InProgress
  Returns:
    None 
  """
  data[key] = {'timestamp': timestamp, 'status': status}

def update_cache_before_commit(session):
  """
  The session event listener before_commit results in updating flag in memcache for marking for add/delete/update
  On any failures, it logs errors and does not throw exception
  """
  cache_manager = get_cache_manager()
  status_entries ={}
  for key in cache_manager.marked_for_add.keys():
       build_status_cache(status_entries, 'CreateOp:' + key, datetime.datetime.now(), 'InProgress')
  for key in cache_manager.marked_for_update.keys():
       build_status_cache(status_entries, 'UpdateOp:' + key, datetime.datetime.now(), 'InProgress')
  for key in cache_manager.marked_for_delete:
       build_status_cache(status_entries, 'DeleteOp:' + key, datetime.datetime.now(), 'InProgress')
  if len(status_entries) > 0:
    ret = cache_manager.bulk_add(status_entries)
    if len(ret) > 0:
     current_app.logger.error('CACHE: Unable to add status for newly created entries in memcache ')

def update_cache_after_commit(session):
  """
  The session event listener after_commit results in actually updating the cache entries
  Also marks the flag for the objects modified as completed, this is to indicate to gets() to go ahead and read from cache
  Logs error if there are errors in updating entries in cache 

  Args:
    app: Flask Application context

  Returns:
    None 
  """
  cache_manager = get_cache_manager()

  if len(cache_manager.marked_for_add) > 0:
    add_result = cache_manager.bulk_add(cache_manager.marked_for_add)
    # result is empty on success, non-empty on failure
    #
    if len(add_result) > 0: 
      current_app.logger.error("CACHE: Failed to add entries to cache: " + str(add_result))
    else:
      current_app.logger.info("CACHE: Successfully added entries to cache") 

  if len(cache_manager.marked_for_update) > 0:
    update_result = cache_manager.bulk_update(cache_manager.marked_for_update)
    # result is empty on success, non-empty on failure returns list of keys including network failures
    if len(update_result) > 0: 
      current_app.logger.error("CACHE: Failed to update entries in cache: " + str(update_result))
    else:
      current_app.logger.info("CACHE: Successfully updated entries in cache") 

  # TODO(ggrcdev): check for duplicates in marked_for_delete
  #
  if len(cache_manager.marked_for_delete) > 0:
    delete_result = cache_manager.bulk_delete(cache_manager.marked_for_delete)
    # TODOC(ggrcdev): handling failure including network errors, currently we log errors
    if delete_result is True:
      current_app.logger.info("CACHE: Successfully deleted entries from cache") 
    else:
      current_app.logger.error("CACHE: Failed to delete entries from cache: " + str(delete_result))
  
  status_entries =[]
  for key in cache_manager.marked_for_add.keys():
     status_entries.append('CreateOp:' + key)
  for key in cache_manager.marked_for_update.keys():
     status_entries.append('UpdateOp:' + key)
  for key in cache_manager.marked_for_delete:
     status_entries.append('DeleteOp:' + key)
  if len(status_entries) > 0:
    if cache_manager.bulk_delete(status_entries) is not True:
      current_app.logger.error('CACHE: Unable to delete status for entries in memcache')

  cache_manager.clear_cache()


def init_ggrc_cache(app):
  """Write collection (objects or stubs) to cache
  Args:
    app: Flask Application context

  Returns:
    None 
  """
  # Create instance of cache manager class for applying policies and operations on cache
  #
  cache_manager = get_cache_manager()

  # Setup config, policy, DTO manager
  #
  defaultproperties={'CACHEMECHANISM':'memcache'}
  config = Config();
  config.setProperties(defaultproperties)
  config.initialize()

  # Setup factory class to allow cache manager to create the cache mechanism objects.
  # TODO(ggrcdev): Rename Factory as BaseFactory 
  #
  factory = Factory();
  cache_manager.set_config(config)
  cache_manager.set_factory(factory)

  # Setup session event listeners
  #
  event.listen(Session, 'before_flush',update_cache_before_flush)
  event.listen(Session, 'after_flush', update_cache_after_flush)
  event.listen(Session, 'before_commit', update_cache_before_commit)
  event.listen(Session, 'after_commit', update_cache_after_commit)
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

