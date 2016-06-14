# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from datetime import datetime

from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.properties import RelationshipProperty
from werkzeug.exceptions import BadRequest
import iso8601
import sqlalchemy

from ggrc import db
from ggrc.login import get_current_user_id
from ggrc.models.reflection import AttributeInfo
from ggrc.models.types import JsonType
from ggrc.utils import url_for
from ggrc.utils import view_url_for
from ggrc.utils import benchmark
import ggrc.builder
import ggrc.models
import ggrc.services

"""JSON resource state representation handler for gGRC models."""


def get_json_builder(obj):
  """Instantiate or retrieve a JSON representation builder for the given
  object.
  """
  if type(obj) is type:
    cls = obj
  else:
    cls = obj.__class__
  # Lookup the builder instance in the builder module
  builder = getattr(ggrc.builder, cls.__name__, None)
  if not builder:
    # Create the builder and cache it in the builder module
    builder = Builder(cls)
    setattr(ggrc.builder, cls.__name__, builder)
  return builder


def publish_base_properties(obj):
    ret = {}
    self_url = url_for(obj)
    if self_url:
      ret['selfLink'] = self_url
    view_url = view_url_for(obj)
    if view_url:
      ret['viewLink'] = view_url
    return ret


def publish(obj, inclusions=(), inclusion_filter=None):
  """Translate ``obj`` into a valid JSON value. Objects with properties are
  translated into a ``dict`` object representing a JSON object while simple
  values are returned unchanged or specially formatted if needed.
  """
  if inclusion_filter is None:
    def inclusion_filter(x):
      return True
  publisher = get_json_builder(obj)
  if publisher and getattr(publisher, '_publish_attrs', False):
    with benchmark("publish base properties"):
      ret = publish_base_properties(obj)
    with benchmark("publish contributions"):
      ret.update(publisher.publish_contribution(
          obj, inclusions, inclusion_filter))
    return ret
  # Otherwise, just return the value itself by default
  return obj


def publish_stub(obj, inclusions=(), inclusion_filter=None):
  publisher = get_json_builder(obj)
  if publisher:
    ret = {}
    self_url = url_for(obj)
    if self_url:
      ret['href'] = self_url
    ret['type'] = obj.__class__.__name__
    ret['context_id'] = obj.context_id
    if hasattr(publisher, '_stub_attrs') and publisher._stub_attrs:
      ret.update(publisher.publish_stubs(obj, inclusions, inclusion_filter))
    return ret
  # Otherwise, just return the value itself by default
  return obj


def update(obj, json_obj):
  """Translate the state represented by ``json_obj`` into update actions
  performed upon the model object ``obj``. After performing the update ``obj``
  and ``json_obj`` should be equivalent representations of the model state.
  """
  updater = get_json_builder(obj)
  if updater:
    updater.update(obj, json_obj)
  # FIXME what to do if no updater??
  # Nothing, perhaps log, assume omitted by design


def create(obj, json_obj):
  """Translate the state represented by ``json_obj`` into update actions
  performed upon the new model object ``obj``. After performing the update
  ``obj`` and ``json_obj`` should be equivalent representations of the model
  state.
  """
  creator = get_json_builder(obj)
  if creator:
    creator.create(obj, json_obj)


class UpdateAttrHandler(object):
  """Performs the translation of a JSON state representation into update
  actions performed on a model object instance.
  """
  @classmethod
  def do_update_attr(cls, obj, json_obj, attr):
    """Perform the update to ``obj`` required to make the attribute attr
    equivalent in ``obj`` and ``json_obj``.
    """
    class_attr = getattr(obj.__class__, attr)
    if (hasattr(attr, '__call__')):
      # The attribute has been decorated with a callable, grab the name and
      # invoke the callable to get the value
      attr_name = attr.attr_name
      value = attr(cls, obj, json_obj)
    elif not hasattr(cls, class_attr.__class__.__name__):
      # The attribute is a function on the obj like custom_attributes in
      # CustomAttributable mixin
      attr_name = attr
      value = class_attr(obj, json_obj)
    else:
      # Lookup the method to use to perform the update. Use reflection to
      # key off of the type of the attribute and invoke the method of the
      # same name.
      attr_name = attr
      method = getattr(cls, class_attr.__class__.__name__)
      value = method(obj, json_obj, attr_name, class_attr)
    if isinstance(value, (set, list)) \
       and (
           not hasattr(class_attr, 'property') or not
           hasattr(class_attr.property, 'columns') or not isinstance(
            class_attr.property.columns[0].type,
            JsonType)
    ):
      # SQLAlchemy instrumentation botches up if we replace entire collections
      # It works if we update them with changes
      new_set = set(value)
      old_set = set(getattr(obj, attr_name))
      coll_class_attr = getattr(obj.__class__, attr_name)
      coll_attr = getattr(obj, attr_name)
      # Join table objects require special handling so that we can be sure to
      # set the modified_by_id correctly
      if isinstance(coll_class_attr, AssociationProxy):
        current_user_id = get_current_user_id()
        proxied_attr = coll_class_attr.local_attr
        proxied_property = coll_class_attr.remote_attr
        proxied_set_map = dict([(getattr(i, proxied_property.key), i)
                                for i in getattr(obj, proxied_attr.key)])
        coll_attr = getattr(obj, proxied_attr.key)
        for item in new_set - old_set:
          new_item = coll_class_attr.creator(item)
          new_item.modified_by_id = current_user_id
          coll_attr.append(new_item)
        for item in old_set - new_set:
          coll_attr.remove(proxied_set_map[item])
      else:
        for item in new_set - old_set:
          coll_attr.append(item)
        for item in old_set - new_set:
          coll_attr.remove(item)
    else:
      setattr(obj, attr_name, value)

  @classmethod
  def InstrumentedAttribute(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for an ``InstrumentedAttribute``"""
    method = getattr(cls, class_attr.property.__class__.__name__)
    return method(obj, json_obj, attr_name, class_attr)

  @classmethod
  def ColumnProperty(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for a ``ColumnProperty``"""
    method = getattr(
        cls,
        class_attr.property.expression.type.__class__.__name__,
        cls.default_column_handler)
    return method(obj, json_obj, attr_name, class_attr)

  @classmethod
  def default_column_handler(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for a simple value column"""
    return json_obj.get(attr_name)

  @classmethod
  def DateTime(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for a ``Datetime`` column."""
    value = json_obj.get(attr_name)
    try:
      if value:
        d = iso8601.parse_date(value)
        d = d.replace(tzinfo=None)
      else:
        d = None
      return d
    except iso8601.ParseError as e:
      raise BadRequest(
          'Malformed DateTime {0} for parameter {1}. '
          'Error message was: {2}'.format(value, attr_name, e.message)
      )

  @classmethod
  def Date(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for a ``Date`` column."""
    value = json_obj.get(attr_name)
    try:
      return datetime.strptime(value, "%Y-%m-%d") if value else None
    except ValueError as e:
      try:
        return datetime.strptime(value, "%m/%d/%Y") if value else None
      except ValueError as e:
        raise BadRequest(
            'Malformed Date {0} for parameter {1}. '
            'Error message was: {2}'.format(value, attr_name, e.message)
        )

  @classmethod
  def query_for(cls, rel_class, json_obj, attr_name, uselist):
    """Resolve the model object instance referred to by the JSON value."""
    if uselist:
      # The value is a collection of links, resolve the collection of objects
      value = json_obj.get(attr_name)
      rel_ids = [o[u'id'] for o in value] if value else []

      if rel_ids:
        return db.session.query(rel_class).filter(
            rel_class.id.in_(rel_ids)).all()
      else:
        return []
    else:
      rel_obj = json_obj.get(attr_name)
      if rel_obj:
        try:
          # FIXME: Should this be .one() instead of .first() ?
          return db.session.query(rel_class).filter(
              rel_class.id == rel_obj[u'id']).first()
        except(TypeError):
          raise TypeError(''.join(['Failed to convert attribute ', attr_name]))
      return None

  @classmethod
  def RelationshipProperty(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for a ``RelationshipProperty``."""
    rel_class = class_attr.property.mapper.class_
    return cls.query_for(
        rel_class, json_obj, attr_name, class_attr.property.uselist)

  @classmethod
  def AssociationProxy(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for an ``AssociationProxy``."""
    if getattr(class_attr, "publish_raw", False):
      return json_obj.get(attr_name, {})
    rel_class = class_attr.remote_attr.property.mapper.class_
    return cls.query_for(rel_class, json_obj, attr_name, True)

  @classmethod
  def property(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for an object method decorated as a
    ``property``.
    """
    # FIXME need a way to decide this. Require link? Use URNs?
    #  reflective approaches won't work as this is used for polymorphic
    #  properties
    # rel_class = None
    # return cls.query_for(rel_class, json_obj, attr_name, True)
    attr_value = json_obj.get(attr_name, None)
    if attr_value:
      import ggrc.models
      rel_class_name = json_obj[attr_name]['type']
      rel_class = ggrc.models.get_model(rel_class_name)
      return cls.query_for(rel_class, json_obj, attr_name, False)
    return None

  @classmethod
  def simple_property(cls, obj, json_obj, attr_name, class_attr):
    return json_obj.get(attr_name)


"""
Builder strategy:
  * For each non-present attribute, return an "AttributeBuilder" instance
    which describes the objects needed to complete the representation.
  * Maintain a set of requested (type, condition, stub_only?) tuples
  * stub_only? tuples can be requested en-masse via UNION queries
  * non-stub_only? tuples can override stub_only? tuples with identical
    conditions
  * When all available object representations have been built:

Query types:
  (type, id) -> explicit link
  (type, { keyX: valX, ... }) -> an actual query
    note, keyX row/object values must be included in response to distinguish
    results from aggregated queries on the same type
  (type, [id, { keyX: valX, ... }, id2, { keyY: valY }, ...]) ->
    an already-aggregated list of conditions

Query combination:
  (type, id) -> aggregate into "id IN (...)"
  (type, {}) -> aggregate into "...OR keyX = valX OR keyY = valY"

Query construction:
  pass

Result storing:
  { type: { id: <result>, (keyX, ...): { (valX, ...): [<result>, ...] } } }

Result dispatch:
  singles = { (type, id): [<Builder>, ...] }
"""


def build_type_query(type, result_spec):
  model = ggrc.models.get_model(type)
  mapper = model._sa_class_manager.mapper
  columns = []
  columns_indexes = {}
  if len(list(mapper.self_and_descendants)) == 1:
    type_column = sqlalchemy.literal(mapper.class_.__name__)
  else:
    # Handle polymorphic types with CASE
    type_column = sqlalchemy.case(
        value=mapper.polymorphic_on,
        whens={
            val: mapper.class_.__name__
            for val, mapper in mapper.polymorphic_map.items()
        })
  columns.append(type_column)
  columns_indexes['type'] = 0
  columns.append(model.id)
  columns_indexes['id'] = 1
  columns.append(mapper.c.context_id)
  columns_indexes['context_id'] = 2
  columns.append(mapper.c.updated_at)
  columns_indexes['updated_at'] = 3

  conditions = {}
  for keys, vals in result_spec.items():
    for key in keys:
      if key not in columns_indexes:
        columns_indexes[key] = len(columns)
        columns.append(mapper.c[key])
    conditions.setdefault(keys, []).extend(vals.keys())

  where_clauses = []
  for keys, vals in conditions.items():
    if len(keys) == 1:
      # If the key is singular, use `IN (...)`
      where_clauses.append(
          columns[columns_indexes[keys[0]]].in_([v[0] for v in vals]))
    else:
      # If multiple keys, build `OR` of multiple `AND` clauses
      clauses = []
      cols = [columns[columns_indexes[k]] for k in keys]
      for val in vals:
        # Now build OR clause with (key, val) pairs
        clause = []
        for i, v in enumerate(val):
          clause.append(cols[i] == val[i])
        clauses.append(sqlalchemy.and_(*clause))
      where_clauses.append(sqlalchemy.or_(*clauses))
  where_clause = sqlalchemy.or_(*where_clauses)

  query = db.session.query(*columns).filter(where_clause)

  return columns_indexes, query


def build_stub_union_query(queries):
  results = {}
  for (type, conditions) in queries:
    if isinstance(conditions, (int, long, str, unicode)):
      # Assume `id` query
      keys, vals = ('id',), (conditions,)
      results.setdefault(type, {}).setdefault(keys, {}).setdefault(vals, [])
    elif isinstance(conditions, dict):
      keys, vals = zip(*sorted(conditions.items()))
      results.setdefault(type, {}).setdefault(keys, {}).setdefault(vals, [])
    else:
      # FIXME: Handle aggregated conditions recursively
      pass

  column_count = 0
  type_column_indexes = {}
  type_queries = {}
  for (type, result_spec) in results.items():
    columns_indexes, query = build_type_query(type, result_spec)
    type_column_indexes[type] = columns_indexes
    type_queries[type] = query
    if len(columns_indexes) > column_count:
      column_count = len(columns_indexes)

  for (type, query) in type_queries.items():
    for _ in range(column_count - len(type_column_indexes[type])):
      query = query.add_column(sqlalchemy.literal(None))
    type_queries[type] = query

  queries_for_union = type_queries.values()
  if len(queries_for_union) == 0:
    query = None
  elif len(queries_for_union) == 1:
    query = queries_for_union[0]
  else:
    query = db.session.query(
        sqlalchemy.sql.expression.union(
            *[q for q in type_queries.values()]).alias('union_query'))
  return results, type_column_indexes, query


def _render_stub_from_match(match, type_columns):
  type = match[type_columns['type']]
  id = match[type_columns['id']]
  return {
      'type': type,
      'id': id,
      'context_id': match[type_columns['context_id']],
      'href': url_for(type, id=id),
  }


class LazyStubRepresentation(object):
  def __init__(self, type, conditions):
    self.type = type
    if isinstance(conditions, (int, long)):
      conditions = {'id': conditions}
    self.conditions = conditions
    self.condition_key, self.condition_val = zip(*sorted(conditions.items()))

  def get_matches(self, results):
    return results\
        .get(self.type, {})\
        .get(self.condition_key, {})\
        .get(self.condition_val, [])

  def render(self, results, type_columns):
    matches = self.get_matches(results)
    assert len(matches) <= 1, (results, self.type, self.condition_key,
                               self.condition_val)
    if len(matches) == 1:
      return _render_stub_from_match(matches[0], type_columns[self.type])
    else:
      return None


def walk_representation(obj):  # noqa
  if isinstance(obj, dict):
    for k, v in obj.items():
      if isinstance(v, dict):
        for x in walk_representation(v):
          yield x
      elif isinstance(v, (list, tuple)):
        for x in walk_representation(v):
          yield x
      else:
        yield v, k, obj
  elif isinstance(obj, (list, tuple)):
    for i, v in enumerate(obj):
      if isinstance(v, dict):
        for x in walk_representation(v):
          yield x
      elif isinstance(v, (list, tuple)):
        for x in walk_representation(v):
          yield x
      else:
        yield v, i, obj


def gather_queries(resource):
  queries = []
  for val, key, obj in walk_representation(resource):
    if isinstance(val, LazyStubRepresentation):
      queries.append((val.type, val.conditions))
  return queries


def reify_representation(resource, results, type_columns):
  for val, key, obj in walk_representation(resource):
    if isinstance(val, LazyStubRepresentation):
      obj[key] = val.render(results, type_columns)
  return resource


def publish_representation(resource):
  queries = gather_queries(resource)

  if len(queries) == 0:
    return resource
  else:
    results, type_columns, query = build_stub_union_query(queries)
    rows = query.all()
    for row in rows:
      type = row[0]
      for columns, matches in results[type].items():
        vals = tuple(row[type_columns[type][c]] for c in columns)
        if vals in matches:
          matches[vals].append(row)

    return reify_representation(resource, results, type_columns)


class Builder(AttributeInfo):
  """JSON Dictionary builder for ggrc.models.* objects and their mixins."""

  def generate_link_object_for_foreign_key(self, id, type, context_id=None):
    """Generate a link object for this object reference."""
    return {'id': id, 'type': type, 'href': url_for(type, id=id),
            'context_id': context_id}

  def generate_link_object_for(
          self, obj, inclusions, include, inclusion_filter):
    """Generate a link object for this object. If there are property paths
    to be included specified in the ``inclusions`` parameter, those properties
    will be added to the object representation. If the ``include`` parameter
    is ``True`` the entire object will be represented in the result.
    """
    if include and ((not inclusion_filter) or inclusion_filter(obj)):
      return publish(obj, inclusions, inclusion_filter)
    result = {
        'id': obj.id, 'type': type(obj).__name__, 'href': url_for(obj),
        'context_id': obj.context_id}
    for path in inclusions:
      if type(path) is not str and type(path) is not unicode:
        attr_name, remaining_path = path[0], path[1:]
      else:
        attr_name, remaining_path = path, ()
      result[attr_name] = self.publish_attr(
          obj, attr_name, remaining_path, include, inclusion_filter)
    return result

  def publish_link_collection(
          self, join_objects, inclusions, include, inclusion_filter):
    """The ``attr_name`` attribute is a collection of object references;
    translate the collection of object references into a collection of link
    objects for the JSON dictionary representation.
    """
    # FIXME: Remove the "if o is not None" when we can guarantee referential
    #   integrity
    return [
        self.generate_link_object_for(o, inclusions, include, inclusion_filter)
        for o in join_objects if o is not None]

  def publish_link(
          self, obj, attr_name, inclusions, include, inclusion_filter):
    """The ``attr_name`` attribute is an object reference; translate the object
    reference into a link object for the JSON dictionary representation.
    """
    attr_value = getattr(obj, attr_name)
    if attr_value:
      return self.generate_link_object_for(
          attr_value, inclusions, include, inclusion_filter)
    else:
      return None

  def publish_association_proxy(
          self, obj, attr_name, class_attr, inclusions, include,
          inclusion_filter):
    # `associationproxy` uses another table as a join table, and context
    # filtering must be done on the join table, or information leakage will
    # result.
    with benchmark("publish association proxy: {}".format(attr_name)):
      with benchmark("get object list for: {}".format(attr_name)):
        import ipdb; ipdb.set_trace()
        join_objects = []
        with benchmark("get objects for: {} - {}".format(attr_name, class_attr.local_attr.key)):
          all_objects = getattr(obj, class_attr.local_attr.key)
        for join_object in all_objects:
          if (not inclusion_filter) or inclusion_filter(join_object):
            join_objects.append(join_object)

      if include:
        target_objects = [
            getattr(join_object, class_attr.remote_attr.key)
            for join_object in join_objects]
        return self.publish_link_collection(
            target_objects, inclusions, include, inclusion_filter)
      else:
        if isinstance(class_attr.remote_attr, property):
          target_name = class_attr.value_attr + '_id'
          target_type = class_attr.value_attr + '_type'
          return [
              LazyStubRepresentation(
                  getattr(o, target_type), getattr(o, target_name))
              for o in join_objects]
        else:
          target_mapper = class_attr.remote_attr.property.mapper
          # Handle inheritance -- we must check the object itself for the type
          if len(list(target_mapper.self_and_descendants)) > 1:
            target_attr = class_attr.remote_attr.property.key
            return [
                self.generate_link_object_for(
                    getattr(o, target_attr),
                    inclusions,
                    include,
                    inclusion_filter)
                for o in join_objects]
          else:
            target_name = list(
                class_attr.remote_attr.property.local_columns)[0].key
            target_type = class_attr.remote_attr.property.mapper.class_.__name__
            with benchmark("generate result list for: {}".format(attr_name)):
              result_list = [
                  LazyStubRepresentation(
                      target_type, getattr(o, target_name))
                  for o in join_objects]
            return result_list

  def publish_relationship(
          self, obj, attr_name, class_attr, inclusions, include,
          inclusion_filter):
    uselist = class_attr.property.uselist
    if uselist:
      join_objects = getattr(obj, attr_name)
      return self.publish_link_collection(
          join_objects, inclusions, include, inclusion_filter)
    elif include or class_attr.property.backref:
      return self.publish_link(
          obj, attr_name, inclusions, include, inclusion_filter)
    else:
      if class_attr.property.mapper.class_.__mapper__.polymorphic_on \
              is not None:
        target = getattr(obj, attr_name)
        target_type = target.__class__.__name__
      else:
        target_type = class_attr.property.mapper.class_.__name__
      target_name = list(class_attr.property.local_columns)[0].key
      attr_value = getattr(obj, target_name)
      if attr_value is not None:
        return LazyStubRepresentation(target_type, attr_value)
      else:
        return None

  def publish_attr(
          self, obj, attr_name, inclusions, include, inclusion_filter):
    class_attr = getattr(obj.__class__, attr_name)
    if isinstance(class_attr, AssociationProxy):
      if getattr(class_attr, 'publish_raw', False):
        published_attr = getattr(obj, attr_name)
        if hasattr(published_attr, "copy"):
          return published_attr.copy()
        else:
          return published_attr
      else:
        return self.publish_association_proxy(
            obj, attr_name, class_attr, inclusions, include, inclusion_filter)
    elif isinstance(class_attr, InstrumentedAttribute) and \
            isinstance(class_attr.property, RelationshipProperty):
      return self.publish_relationship(
          obj, attr_name, class_attr, inclusions, include, inclusion_filter)
    elif class_attr.__class__.__name__ == 'property':
      if not inclusions or include:
        if (getattr(obj, '{0}_id'.format(attr_name))):
          return LazyStubRepresentation(
              getattr(obj, '{0}_type'.format(attr_name)),
              getattr(obj, '{0}_id'.format(attr_name)))
      else:
        return self.publish_link(
            obj, attr_name, inclusions, include, inclusion_filter)
    else:
      return getattr(obj, attr_name)

  def _publish_attrs_for(
          self, obj, attrs, json_obj, inclusions=[], inclusion_filter=None):
    with benchmark("publish attrs for, atttr count: {}".format(len(attrs))):
      for attr in attrs:
        with benchmark("publish attr for attr: {}".format(attr)):
          if hasattr(attr, '__call__'):
            attr_name = attr.attr_name
          else:
            attr_name = attr
          local_inclusion = ()
          with benchmark("find attr inclusion: {}".format(attr_name)):
            for inclusion in inclusions:
              if inclusion[0] == attr_name:
                local_inclusion = inclusion
                break
          json_obj[attr_name] = self.publish_attr(
              obj, attr_name, local_inclusion[1:], len(local_inclusion) > 0,
              inclusion_filter)

  def publish_attrs(self, obj, json_obj, extra_inclusions, inclusion_filter):
    """Translate the state represented by ``obj`` into the JSON dictionary
    ``json_obj``.

    The ``inclusions`` parameter can specify a tree of property paths to be
    inlined into the representation. Leaf attributes will be inlined completely
    if they are links to other objects. The inclusions data structure is a
    list where the first segment of a path is a string and the next segment
    is a list of segment paths. Here are some examples:

    ..

      ('directives')
      [('directives'),('cycles')]
      [('directives', ('audit_frequency','organization')),('cycles')]
    """
    inclusions_set = set((attr,) for attr in self._include_links)
    inclusions = inclusions_set.union(set(extra_inclusions))
    return self._publish_attrs_for(
        obj, self._publish_attrs, json_obj, inclusions, inclusion_filter)

  @classmethod
  def do_update_attrs(cls, obj, json_obj, attrs):
    """Translate every attribute in ``attrs`` from the JSON dictionary value
    to a value or model object instance for references set for the attribute
    in ``obj``.
    """
    for attr_name in attrs:
      UpdateAttrHandler.do_update_attr(obj, json_obj, attr_name)

  def update_attrs(self, obj, json_obj):
    """Translate the state representation given by ``json_obj`` into the
    model object ``obj``.
    """
    self.do_update_attrs(obj, json_obj, self._update_attrs)

  def create_attrs(self, obj, json_obj):
    """Translate the state representation given by ``json_obj`` into the new
    model object ``obj``.
    """
    self.do_update_attrs(obj, json_obj, self._create_attrs)

  def publish_contribution(self, obj, inclusions, inclusion_filter):
    """Translate the state represented by ``obj`` into a JSON dictionary"""
    json_obj = {}
    self.publish_attrs(obj, json_obj, inclusions, inclusion_filter)
    return json_obj

  def publish_stubs(self, obj, inclusions, inclusion_filter):
    """Translate the state represented by ``obj`` into a JSON dictionary
    containing an abbreviated representation.
    """
    json_obj = {}
    self._publish_attrs_for(
        obj, self._stub_attrs, json_obj, inclusions, inclusion_filter)
    return json_obj

  def update(self, obj, json_obj):
    """Update the state represented by ``obj`` to be equivalent to the state
    represented by the JSON dictionary ``json_obj``.
    """
    self.update_attrs(obj, json_obj)

  def create(self, obj, json_obj):
    """Update the state of the new model object ``obj`` to be equivalent to the
    state represented by the JSON dictionary ``json_obj``.
    """
    self.create_attrs(obj, json_obj)
