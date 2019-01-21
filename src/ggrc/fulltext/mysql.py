# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Full text index engine for Mysql DB backend"""

import logging

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import select, union_all
from sqlalchemy import event

from ggrc import db
from ggrc.fulltext.sql import SqlIndexer
from ggrc.fulltext.mixin import Indexed
from ggrc.models import all_models, get_model
from ggrc.query import my_objects
from ggrc.rbac import permissions


logger = logging.getLogger(__name__)


ATTRIBUTE_ALIASES_TO_SEARCH_IN = (
    'title',
    'name',
    'email',
    'notes',
    'description',
    'slug'
)


# pylint: disable=too-few-public-methods
class MysqlRecordProperty(db.Model):
  """ Db model for collect fulltext index records"""
  __tablename__ = 'fulltext_record_properties'

  key = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String(64), primary_key=True)
  tags = db.Column(db.String)
  property = db.Column(db.String(250), primary_key=True)
  subproperty = db.Column(db.String(64), primary_key=True)
  content = db.Column(db.Text, nullable=False, default=u"")

  @declared_attr
  def __table_args__(cls):  # pylint: disable=no-self-argument
    return (
        db.Index('ix_{}_tags'.format(cls.__tablename__), 'tags'),
        db.Index('ix_{}_key'.format(cls.__tablename__), 'key'),
        db.Index('ix_{}_type'.format(cls.__tablename__), 'type'),
    )


class MysqlIndexer(SqlIndexer):
  """MysqlIndexer class"""
  record_type = MysqlRecordProperty

  @staticmethod
  def _get_attr_names_to_search_in(model):
    """Get list of indexed attribute names"""

    attrs = model.get_fulltext_attrs()

    aliases = dict((attr.alias, attr) for attr in attrs)

    ret = []
    # Get list of attribute names by alias name
    for name in ATTRIBUTE_ALIASES_TO_SEARCH_IN:
      if name in aliases:
        ret.append(model.get_fulltext_attr_name(aliases[name]))

    return ret

  @classmethod
  def _get_filter_query(cls, terms, model=None):
    """Get the whitelist of fields to filter in full text table."""

    if not model or not issubclass(model, Indexed):
      # Only indexed models are supported
      return sa.false()

    attr_names = cls._get_attr_names_to_search_in(model)
    whitelist = MysqlRecordProperty.property.in_(attr_names)

    if not terms:
      return whitelist
    return sa.and_(whitelist, MysqlRecordProperty.content.contains(terms))

  @staticmethod
  def get_permissions_query(model_names, permission_type='read'):
    """Prepare the query based on the allowed resources

    This filters for each of the required models based on permissions on every
    object type.
    """
    if not model_names:
      # If there are no model names set, the result of the permissions query
      # will always be false, so we can just return false instead of having an
      # empty in statement combined with an empty list joined by or statement.
      return sa.false()

    type_queries = []
    for model_name in model_names:
      contexts, resources = permissions.get_context_resource(
          model_name=model_name,
          permission_type=permission_type,
      )

      if contexts is None:
        # None context means user has full access of permission_type for the
        # given model
        type_queries.append(MysqlRecordProperty.type == model_name)
      elif resources:
        type_queries.append(sa.and_(
            MysqlRecordProperty.type == model_name,
            MysqlRecordProperty.key.in_(resources),
        ))

    if not type_queries:
      return sa.false()

    return sa.or_(*type_queries)

  @staticmethod
  def search_get_owner_query(query, types=None, contact_id=None):
    """Prepare the search query based on the contact_id to return my
    objects. This method is used only for dashboard and returns objects
    the user is the owner.
    """
    if not contact_id:
      return query

    union_query = my_objects.get_myobjects_query(
        types=types,
        contact_id=contact_id)

    return query.join(
        union_query,
        sa.and_(
            union_query.c.id == MysqlRecordProperty.key,
            union_query.c.type == MysqlRecordProperty.type),
    )

  def _add_extra_params_query(self, query, type_name, extra_param):
    """Prepare the query for handling extra params."""
    if not extra_param:
      return query

    models = [m for m in all_models.all_models if m.__name__ == type_name]

    if not models:
      return query
    model_klass = models[0]

    return query.filter(self.record_type.key.in_(
        db.session.query(
            model_klass.id.label('id')
        ).filter_by(**extra_param)
    ))

  @staticmethod
  def _get_grouped_types(types=None, extra_params=None):
    """Return dict(type -> model) for all types if it's not in extra_params"""
    model_names = dict()
    for model_klass in all_models.all_models:
      model_name = model_klass.__name__
      if types and model_name not in types:
        continue
      if extra_params and model_name in extra_params:
        continue
      model_names[model_name] = model_klass
    return model_names

  @staticmethod
  def _get_model(model_name, extra_params=None):
    """Return model by its name if it is not in `extra_params`, else None"""

    if extra_params and model_name in extra_params:
      return None


    return get_model(model_name)

  # pylint: disable=too-many-arguments
  def search(self, terms, types=None, permission_type='read',
             contact_id=None, extra_params=None):
    """Prepare the search query and return the results set based on the
    full text table."""

    if not types:
      # return empty result in case if type is not specified
      return []

    queries = []

    for type_ in types:
      queries.append(self._get_search_for_single_model(
          terms=terms,
          types=[type_],
          permission_type=permission_type,
          contact_id=contact_id,
          extra_params=extra_params
      ))

    if len(queries) > 1:
      query = union_all(*queries)
    else:
      query = queries[0]

    return db.session.execute(query)

  # pylint: disable=too-many-arguments,too-many-locals
  def _get_search_for_single_model(self, terms, types,
                                   permission_type='read',
                                   contact_id=None, extra_params=None):
    """Prepare the search query and return the results set based on the
    full text table.

    `types` must contain 1 item at most
    """

    extra_params = extra_params or {}
    model_names = self._get_grouped_types(types, extra_params)
    any_model = model_names.values()[0] if model_names else None

    columns = (
        self.record_type.key.label('key'),
        self.record_type.type.label('type'),
        self.record_type.property.label('property'),
        self.record_type.content.label('content'),
        sa.case(
            [(self.record_type.property == 'title', sa.literal(0))],
            else_=sa.literal(1)).label('sort_key'))

    query = db.session.query(*columns)
    query = query.filter(self.get_permissions_query(
        model_names.keys(), permission_type))
    query = query.filter(self._get_filter_query(terms, any_model))
    query = self.search_get_owner_query(query, types, contact_id)

    model_names = self._get_grouped_types(types)
    any_model = model_names.values()[0] if model_names else None

    unions = [query]
    # Add extra_params and extra_colums:
    for key, value in extra_params.iteritems():
      if key not in model_names:
        continue
      extra_q = db.session.query(*columns)
      extra_q = extra_q.filter(
          self.get_permissions_query([key], permission_type))
      extra_q = extra_q.filter(self._get_filter_query(terms, any_model))
      extra_q = self.search_get_owner_query(extra_q, [key], contact_id)
      extra_q = self._add_extra_params_query(extra_q, key, value)
      unions.append(extra_q)
    all_queries = sa.union(*unions)
    all_queries = aliased(all_queries.order_by(
        all_queries.c.sort_key, all_queries.c.content))

    return select([all_queries.c.key, all_queries.c.type]).distinct()

  # pylint: disable=too-many-arguments
  def counts(self, terms, types=None, contact_id=None, extra_params=None,
             extra_columns=None):
    """Prepare the search query and return the results set based on the
    full text table."""

    queries = []

    if not types:
      # return empty result in case if type is not specified
      return []

    for type_ in types:
      queries.append(self._get_counts_for_single_model(
          terms=terms,
          types=[type_],
          contact_id=contact_id,
          extra_params=extra_params,
          extra_columns=extra_columns
      ))

    if len(queries) > 1:
      query = union_all(*queries)
    else:
      query = queries[0]

    return db.session.execute(query)

  # pylint: disable=too-many-arguments
  def _get_counts_for_single_model(self, terms, types=None,
                                   contact_id=None, extra_params=None,
                                   extra_columns=None):
    """Prepare the search query, but return only count for the requested object.

    `types` must contain 1 item at most
    """
    extra_params = extra_params or {}
    extra_columns = extra_columns or {}
    model_names = self._get_grouped_types(types, extra_params)
    any_model = model_names.values()[0] if model_names else None

    query = db.session.query(
        self.record_type.type, sa.func.count(sa.distinct(
            self.record_type.key)), sa.literal(""))
    query = query.filter(self.get_permissions_query(model_names.keys()))
    query = query.filter(self._get_filter_query(terms, any_model))
    query = self.search_get_owner_query(query, types, contact_id)
    query = query.group_by(self.record_type.type)
    all_extra_columns = dict(extra_columns.items() +
                             [(p, p) for p in extra_params
                              if p not in extra_columns])
    if not all_extra_columns:
      return query

    # Add extra_params and extra_colums:
    for key, value in all_extra_columns.iteritems():
      extra_q = db.session.query(
          self.record_type.type,
          sa.func.count(sa.distinct(self.record_type.key)),
          sa.literal(key)
      )
      extra_q = extra_q.filter(self.get_permissions_query([value]))
      extra_q = extra_q.filter(self._get_filter_query(terms, any_model))
      extra_q = self.search_get_owner_query(extra_q, [value], contact_id)
      extra_q = self._add_extra_params_query(extra_q,
                                             value,
                                             extra_params.get(key, None))
      extra_q = extra_q.group_by(self.record_type.type)
      query = query.union(extra_q)
    return query


Indexer = MysqlIndexer


# pylint:disable=unused-argument
@event.listens_for(all_models.Relationship, "after_insert")
@event.listens_for(all_models.Relationship, "after_delete")
def refresh_documents(mapper, connection, target):
  """Refreshes related Documents"""
  if target.source_type == 'Document':
    for_refresh = target.destination
  elif target.destination_type == 'Document':
    for_refresh = target.source
  else:
    return
  if hasattr(for_refresh, 'documents'):
    db.session.expire(for_refresh, ['documents'])


# pylint:disable=unused-argument
@event.listens_for(all_models.Relationship, "after_insert")
@event.listens_for(all_models.Relationship, "after_delete")
def refresh_evidences(mapper, connection, target):
  """Refreshes related Evidences"""
  if target.source_type == 'Evidence':
    for_refresh = target.destination
  elif target.destination_type == 'Evidence':
    for_refresh = target.source
  else:
    return
  if hasattr(for_refresh, 'evidences'):
    db.session.expire(for_refresh, ['evidences'])
