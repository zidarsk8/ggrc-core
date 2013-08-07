# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import datetime
import ggrc.builder.json
import hashlib
import time
from blinker import Namespace
from exceptions import TypeError
from flask import url_for, request, current_app, session
from flask.views import View
from ggrc import db
from ggrc.utils import as_json, UnicodeSafeJsonWrapper
from ggrc.fulltext import get_indexer
from ggrc.fulltext.recordbuilder import fts_record_for
from ggrc.login import get_current_user_id
from ggrc.models.context import Context
from ggrc.models.event import Event
from ggrc.models.revision import Revision
from ggrc.rbac import permissions
from sqlalchemy import or_
from werkzeug.exceptions import BadRequest, Forbidden
from wsgiref.handlers import format_date_time
from urllib import urlencode
from .attribute_query import AttributeQueryBuilder

"""gGRC Collection REST services implementation. Common to all gGRC collection
resources.
"""

def inclusion_filter(obj):
  return permissions.is_allowed_read(obj.__class__.__name__, obj.context_id)

class ModelView(View):
  pk = 'id'
  pk_type = 'int'

  _model = None

  # Simple accessor properties
  @property
  def request(self):
    return request

  @property
  def model(self):
    return self._model

  @property
  def modified_attr_name(self):
    return 'updated_at'

  @property
  def modified_attr(self):
    """Return the model attribute to be used for Last-Modified header and
    sorting collection elements.
    """
    return getattr(self.model, self.modified_attr_name)

  def modified_at(self, obj):
    return getattr(obj, self.modified_attr_name)

  # Default model/DB helpers
  def get_collection(self, filter_by_contexts=True):
    if hasattr(self.model, 'eager_query'):
      query = self.model.eager_query()
    else:
      query = db.session.query(self.model)
    joinlist = []
    if request.args:
      querybuilder = AttributeQueryBuilder(self.model)
      filter, joinlist = querybuilder.collection_filters(request.args)
      if filter is not None:
        for j in joinlist:
          query = query.join(j)
        query = query.filter(filter)
    if filter_by_contexts:
      contexts = permissions.read_contexts_for(self.model.__name__)
      if contexts is not None and len(contexts) > 0:
        query = query.filter(or_(
          self.model.context_id.in_(contexts),
          self.model.context_id == None))
      elif contexts is not None:
        query = query.filter(self.model.context_id == None)
      for j in joinlist:
        j_class = j.property.mapper.class_
        j_contexts = permissions.read_contexts_for(j_class.__name__)
        if j_contexts is not None:
          query = query.filter(or_(
            j_class.context_id.in_(j_contexts),
            j_class.context_id == None))
    return query.order_by(self.modified_attr.desc())#.limit(20)

  def get_object(self, id):
    # This could also use `self.pk`
    return self.get_collection(filter_by_contexts=False)\
        .filter(self.model.id == id).first()

  def not_found_message(self):
    return '{0} not found.'.format(self.model._inflector.title_singular)

  def not_found_response(self):
    return current_app.make_response((self.not_found_message(), 404, []))

  def etag(self, last_modified):
    """Generate the etag given a datetime for the last time the resource was
    modified. This isn't as good as an etag generated off of a hash of the
    representation, but, it doesn't require the representation in order to be
    calculated. An alternative would be to keep an etag on the stored
    representation, but this will do for now.

    .. note::

       Using the datetime implies the need for some care - the resolution of
       the time object needs to be sufficient such that you don't end up with
       the same etag due to two updates performed in rapid succession.
    """
    return '"{0}"'.format(hashlib.sha1(str(last_modified)).hexdigest())

  def collection_last_modified(self):
    """Calculate the last time a member of the collection was modified. This
    method relies on the fact that the collection table has an `updated_at` or
    other column with a relevant timestamp; services for models that don't have
    this field **MUST** override this method.
    """
    result = db.session.query(
        self.modified_attr).order_by(self.modified_attr.desc()).first()
    if result is not None:
      return self.modified_at(result)
    return datetime.datetime.now()

  # Routing helpers
  @classmethod
  def endpoint_name(cls):
    return cls.__name__

  @classmethod
  def url_for_preserving_querystring(cls, *args, **kwargs):
    url = cls.url_for(*args, **kwargs)
    # preserve original query string
    idx = request.url.find('?')
    querystring = '' if idx < 0 else '?' + request.url[idx+1:]
    return url + querystring

  @classmethod
  def base_url_for(cls, _memoized_base_url={}):
    if cls not in _memoized_base_url:
      _memoized_base_url[cls] = url_for(cls.endpoint_name())
    return _memoized_base_url[cls]

  @classmethod
  def url_for(cls, *args, **kwargs):
    url = cls.base_url_for()
    if len(args) > 0:
      arg = args[0]
      id = arg if not isinstance(arg, db.Model) else arg.id
      url = url + '/' + str(id)
    if 'id' in kwargs:
      url = url + '/' + str(kwargs['id'])
      del kwargs['id']
    if len(kwargs) > 0:
      url = url + '?' + urlencode(kwargs)
    return url

  @classmethod
  def decorate_view_func(cls, view_func, decorators):
    if not isinstance(decorators, (list, tuple)):
      decorators = (decorators,)
    for decorator in reversed(decorators):
      view_func = decorator(view_func)
    return view_func


# View base class for Views handling
#   - /resources (GET, POST)
#   - /resources/<pk:pk_type> (GET, PUT, POST, DELETE)
class Resource(ModelView):
  """View base class for Views handling.  Will typically be registered with an
  application following a collection style for routes. Collection `GET` and
  `POST` will have a route like `/resources` while collection member
  resource routes will have routes likej `/resources/<pk:pk_type>`.

  To register a Resource subclass FooCollection with a Flask application:

  ..

     FooCollection.add_to(app, '/foos')

  By default will only support the `application/json` content-type.
  """

  signals = Namespace()
  model_posted = signals.signal('Model POSTed',
    """
    Indicates that a model object was received via POST and will be committed
    to the database. The sender in the signal will be the model class of the
    POSTed resource. The following arguments will be sent along with the
    signal:

      :obj: The model instance created from the POSTed JSON.
      :src: The original POSTed JSON dictionary.
      :service: The instance of Resource handling the POST request.  
    """,
    )

  def dispatch_request(self, *args, **kwargs):
    method = request.method

    if method == 'GET':
      if self.pk in kwargs and kwargs[self.pk] is not None:
        return self.get(*args, **kwargs)
      else:
        return self.collection_get()
    elif method == 'POST':
      if self.pk in kwargs and kwargs[self.pk] is not None:
        return self.post(*args, **kwargs)
      else:
        return self.collection_post()
    elif method == 'PUT':
      return self.put(*args, **kwargs)
    elif method == 'DELETE':
      return self.delete(*args, **kwargs)
    else:
      raise NotImplementedError()

  def post(*args, **kwargs):
    raise NotImplementedError()

  # Default JSON request handlers
  def get(self, id):
    obj = self.get_object(id)
    if obj is None:
      return self.not_found_response()
    if 'Accept' in self.request.headers and \
       'application/json' not in self.request.headers['Accept']:
      return current_app.make_response((
        'application/json', 406, [('Content-Type', 'text/plain')]))
    if not permissions.is_allowed_read(self.model.__name__, obj.context_id):
      raise Forbidden()
    object_for_json = self.object_for_json(obj)
    if 'If-None-Match' in self.request.headers and \
        self.request.headers['If-None-Match'] == self.etag(object_for_json):
      return current_app.make_response((
        '', 304, [('Etag', self.etag(object_for_json))]))
    return self.json_success_response(
      self.object_for_json(obj), self.modified_at(obj))

  def validate_headers_for_put_or_delete(self, obj):
    missing_headers = []
    if 'If-Match' not in self.request.headers:
      missing_headers.append('If-Match')
    if 'If-Unmodified-Since' not in self.request.headers:
      missing_headers.append('If-Unmodified-Since')
    if missing_headers:
      # rfc 6585 defines a new status code for missing required headers
      return current_app.make_response((
        'If-Match is required.', 428, [('Content-Type', 'text/plain')]))
    if request.headers['If-Match'] != self.etag(self.object_for_json(obj)) or \
       request.headers['If-Unmodified-Since'] != \
          self.http_timestamp(self.modified_at(obj)):
      return current_app.make_response((
          'The resource has been changed. The conflict must be resolved and '
          'the request resubmitted with an up to date Etag for If-Match '
          'header.',
          409,
          [('Content-Type', 'text/plain')]
          ))
    return None

  def json_update(self, obj, src):
    ggrc.builder.json.update(obj, src)

  def put(self, id):
    obj = self.get_object(id)
    if obj is None:
      return self.not_found_response()
    if self.request.headers['Content-Type'] != 'application/json':
      return current_app.make_response((
        'Content-Type must be application/json', 415,[]))
    header_error = self.validate_headers_for_put_or_delete(obj)
    if header_error:
      return header_error
    src = UnicodeSafeJsonWrapper(self.request.json)
    root_attribute = self.model._inflector.table_singular
    try:
      src = src[root_attribute]
    except KeyError, e:
      return current_app.make_response((
        'Required attribute "{0}" not found'.format(root_attribute), 400, []))
    if not permissions.is_allowed_update(self.model.__name__, obj.context_id):
      raise Forbidden()
    new_context = self.get_context_id_from_json(src)
    if new_context != obj.context_id \
        and not permissions.is_allowed_update(self.model.__name__, new_context):
      raise Forbidden()
    self.json_update(obj, src)
    #FIXME Fake the modified_by_id until we have that information in session.
    obj.modified_by_id = get_current_user_id()
    db.session.add(obj)
    self.log_event(db.session, obj)
    db.session.commit()
    obj = self.get_object(id)
    get_indexer().update_record(fts_record_for(obj))
    return self.json_success_response(
        self.object_for_json(obj), self.modified_at(obj))

  def delete(self, id):
    obj = self.get_object(id)

    if obj is None:
      return self.not_found_response()
    header_error = self.validate_headers_for_put_or_delete(obj)
    if header_error:
      return header_error
    if not permissions.is_allowed_delete(self.model.__name__, obj.context_id):
      raise Forbidden()
    db.session.delete(obj)
    self.log_event(db.session, obj)
    db.session.commit()
    get_indexer().delete_record(self.url_for(id=id))
    return self.json_success_response(
      self.object_for_json(obj), self.modified_at(obj))

  def collection_get(self):
    if 'Accept' in self.request.headers and \
       'application/json' not in self.request.headers['Accept']:
      return current_app.make_response((
        'application/json', 406, [('Content-Type', 'text/plain')]))

    objs = self.get_collection()
    collection = self.collection_for_json(objs)
    if 'If-None-Match' in self.request.headers and \
        self.request.headers['If-None-Match'] == self.etag(collection):
      return current_app.make_response((
        '', 304, [('Etag', self.etag(collection))]))
    return self.json_success_response(
      collection, self.collection_last_modified())

  def json_create(self, obj, src):
    ggrc.builder.json.create(obj, src)

  def get_context_id_from_json(self, src):
    context = src.get('context', None)
    if context:
      context_id = context.get('id', None)
      try:
        return int(context_id)
      except (ValueError, TypeError):
        return None
    return None

  def personal_context(self):
    current_user_id = get_current_user_id()
    context = db.session.query(Context).filter(
        Context.related_object_id == current_user_id,
        Context.related_object_type == 'Person',
        ).first()
    if not context:
      context = Context(
          name='Personal Context for {0}'.format(current_user_id),
          description='',
          context_id=1,
          related_object_id=current_user_id,
          related_object_type='Person',
          )
      db.session.add(context)
      db.session.commit()
    return context

  def handle_create(self, obj, src):
    """Do NOTHING by default"""
    pass

  def collection_post(self):
    if self.request.headers['Content-Type'] != 'application/json':
      return current_app.make_response((
        'Content-Type must be application/json', 415,[]))
    obj = self.model()
    src = UnicodeSafeJsonWrapper(self.request.json)
    root_attribute = self.model._inflector.table_singular
    try:
      src = src[root_attribute]
    except KeyError, e:
      return current_app.make_response((
        'Required attribute "{0}" not found'.format(root_attribute), 400, []))
    if 'private' in src:
      pass
    elif 'context' not in src:
      raise BadRequest('context MUST be specified.')
    else:
      if not permissions.is_allowed_create(
          self.model.__name__, self.get_context_id_from_json(src)):
        raise Forbidden()
    self.json_create(obj, src)
    self.model_posted.send(obj.__class__, obj=obj, src=src, service=self)
    obj.modified_by_id = get_current_user_id()
    db.session.add(obj)
    self.log_event(db.session, obj)
    db.session.commit()
    get_indexer().create_record(fts_record_for(obj))
    return self.json_success_response(
      self.object_for_json(obj), self.modified_at(obj), id=obj.id, status=201)

  def log_event(self, session, obj):
    revisions = []
    new_objects = list(session.new) # Delay creation of revisions as ids are not available
    http_method = request.method
    for o in session.dirty:
      if session.is_modified(o):
        revision = Revision( o, get_current_user_id(), 'modified', o.to_json())
        revisions.append(revision)
    for o in session.deleted:
      revision = Revision( o, get_current_user_id(), 'deleted', o.to_json())
      revisions.append(revision)
    session.flush() # this ensures that ids are available for new objects
    for o in new_objects:
      revision = Revision( o, get_current_user_id(), 'created', o.to_json())
      revisions.append(revision)
    event = Event(
      modified_by_id = get_current_user_id(),
      http_method = http_method,
      resource_id = obj.id,
      resource_type = str(obj.__class__.__name__))
    event.revisions = revisions
    session.add(event)

  @classmethod
  def add_to(cls, app, url, model_class=None, decorators=()):
    if model_class:
      service_class = type(model_class.__name__, (cls,), {
        '_model': model_class,
        })
      import ggrc.services
      setattr(ggrc.services, model_class.__name__, service_class)
    else:
      service_class = cls
    view_func = service_class.as_view(service_class.endpoint_name())
    view_func = cls.decorate_view_func(view_func, decorators)
    app.add_url_rule(
        url,
        defaults={cls.pk: None},
        view_func=view_func,
        methods=['GET','POST'])
    app.add_url_rule(
        '{url}/<{type}:{pk}>'.format(url=url, type=cls.pk_type, pk=cls.pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE'])

  # Response helpers
  @classmethod
  def as_json(cls, obj, **kwargs):
    return as_json(obj, **kwargs)

  def object_for_json(self, obj, model_name=None, properties_to_include=None):
    model_name = model_name or self.model._inflector.table_singular
    json_obj = ggrc.builder.json.publish(obj, properties_to_include or [])
    return { model_name: json_obj }

  def get_properties_to_include(self):
    #FIXME This needs to be improved to deal with branching paths... if that's
    #desirable or needed.
    inclusions = request.args.get('__include')
    if inclusions is not None:
      if len(inclusions) == 0:
        raise BadRequest(
            'The __include query parameter requires at least one field to be '
            'included.')
      paths = inclusions.split(',')
      inclusions = []
      for p in paths:
        path = p.split('.')
        if len(path) == 1:
          inclusions.append(path)
        else:
          inclusions.append((path[0], path[1:]))
    else:
      inclusions = ()
    return inclusions

  def collection_for_json(
      self, objects, model_plural=None, collection_name=None):
    model_plural = model_plural or self.model._inflector.table_plural
    collection_name = collection_name or '{0}_collection'.format(model_plural)

    objects_json = []
    for object in objects:
      object_for_json = ggrc.builder.json.publish(
          object, self.get_properties_to_include())
      objects_json.append(object_for_json)

    collection_json = {
      collection_name: {
        'selfLink': self.url_for_preserving_querystring(),
        model_plural: objects_json,
        }
      }

    return collection_json

  def http_timestamp(self, timestamp):
    return format_date_time(time.mktime(timestamp.utctimetuple()))

  def json_success_response(
      self, response_object, last_modified, status=200, id=None):
    headers = [
        ('Last-Modified', self.http_timestamp(last_modified)),
        ('Etag', self.etag(response_object)),
        ('Content-Type', 'application/json'),
        ]
    if id:
      headers.append(('Location', self.url_for(id=id)))
    return current_app.make_response(
      (self.as_json(response_object), status, headers))

  def getval(self, src, attr, *args):
    if args:
      return src.get(unicode(attr), *args)
    return src.get(unicode(attr))

class ReadOnlyResource(Resource):
  def dispatch_request(self, *args, **kwargs):
    method = request.method

    if method == 'GET':
      return super(ReadOnlyResource, self).dispatch_request(*args, **kwargs)
    else:
      raise NotImplementedError()
