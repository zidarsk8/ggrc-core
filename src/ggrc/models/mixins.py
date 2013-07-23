# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc import settings, db
from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from uuid import uuid1
from .inflector import ModelInflectorDescriptor

"""Mixins to add common attributes and relationships. Note, all model classes
must also inherit from ``db.Model``. For example:

  ..

     class Market(BusinessObject, db.Model):
       __tablename__ = 'markets'

"""

class Identifiable(object):
  """A model with an ``id`` property that is the primary key."""
  id = db.Column(db.Integer, primary_key=True)

  # REST properties
  _publish_attrs = ['id']
  _update_attrs = []

  _inflector = ModelInflectorDescriptor()

  @classmethod
  def eager_query(cls):
    return db.session.query(cls)

def created_at_args():
  """Sqlite doesn't have a server, per se, so the server_* args are useless."""
  return {'default': db.text('current_timestamp'),}

def updated_at_args():
  """Sqlite doesn't have a server, per se, so the server_* args are useless."""
  return {
    'default': db.text('current_timestamp'),
    'onupdate': db.text('current_timestamp'),
    }

class ChangeTracked(object):
  """A model with fields to tracked the last user to modify the model, the
  creation time of the model, and the last time the model was updated.
  """
  # FIXME: change modified_by_id to nullable=False when there is an Account
  # model
  modified_by_id = db.Column(db.Integer)
  created_at = db.Column(
      db.DateTime,
      **created_at_args())
  updated_at = db.Column(
      db.DateTime,
      **updated_at_args())
  @declared_attr
  def modified_by(cls):
    return db.relationship(
        'Person',
        primaryjoin='{0}.modified_by_id == Person.id'.format(cls.__name__),
        foreign_keys='{0}.modified_by_id'.format(cls.__name__))
  #TODO Add a transaction id, this will be handy for generating etags
  #and for tracking the changes made to several resources together.
  #transaction_id = db.Column(db.Integer)

  # REST properties
  _publish_attrs = [
      'modified_by',
      'created_at',
      'updated_at',
      ]
  _update_attrs = []

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(ChangeTracked, cls).eager_query()
    return query.options(
        orm.subqueryload('modified_by'))

class Described(object):
  description = db.Column(db.Text)

  # REST properties
  _publish_attrs = ['description']
  _fulltext_attrs = ['description']

class Hyperlinked(object):
  url = db.Column(db.String)

  # REST properties
  _publish_attrs = ['url']

class Hierarchical(object):
  @declared_attr
  def parent_id(cls):
    return db.Column(
        db.Integer, db.ForeignKey('{0}.id'.format(cls.__tablename__)))

  @declared_attr
  def children(cls):
    return db.relationship(
        cls.__name__,
        backref=db.backref('parent', remote_side='{0}.id'.format(cls.__name__)),
        )

  # REST properties
  _publish_attrs = [
      'children',
      'parent',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Hierarchical, cls).eager_query()
    return query.options(
        orm.subqueryload('children'),
        orm.joinedload('parent'))


class Timeboxed(object):
  start_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)

  # REST properties
  _publish_attrs = ['start_date', 'end_date']

class ContextRBAC(object):
  @declared_attr
  def context_id(self):
    return db.Column(db.Integer, db.ForeignKey('contexts.id'))

  @declared_attr
  def context(self):
    return db.relationship('Context', uselist=False)

  _publish_attrs = ['context']

class Base(ChangeTracked, Identifiable, ContextRBAC):
  """Several of the models use the same mixins. This class covers that common
  case.
  """

  def to_json(self):
    d = {}
    for column in self.__table__.columns:
      d[column.name] = getattr(self, column.name)
    return d

class Slugged(Base):
  """Several classes make use of the common mixins and additional are
  "slugged" and have additional fields related to their publishing in the
  system.
  """
  slug = db.Column(db.String, nullable=False)
  title = db.Column(db.String, nullable=False)

  # REST properties
  _publish_attrs = ['slug', 'title']
  _update_attrs = ['title']
  _create_attrs = _publish_attrs
  _fulltext_attrs = ['slug', 'title']

  @classmethod
  def generate_slug_for(cls, obj):
    id = obj.id if hasattr(obj, 'id') else uuid1()
    obj.slug = "{0} {1}".format(obj.__class__.__name__, id)

  @classmethod
  def ensure_slug_before_flush(cls, session, flush_context, instances):
    """Set the slug to a default string so we don't run afoul of the NOT NULL
    constraint.
    """
    for o in session.new:
      if isinstance(o, Slugged) and (o.slug is None or o.slug == ''):
        o.slug = uuid1()
        o._replace_slug = True

  @classmethod
  def ensure_slug_after_flush_postexec(cls, session, flush_context):
    """Replace the placeholder slug with a real slug that will be set on the
    next flush/commit.
    """
    for o in session.identity_map.values():
      if isinstance(o, Slugged) and hasattr(o, '_replace_slug'):
        cls.generate_slug_for(o)
        delattr(o, '_replace_slug')

event.listen(Session, 'before_flush', Slugged.ensure_slug_before_flush)
event.listen(
  Session, 'after_flush_postexec', Slugged.ensure_slug_after_flush_postexec)

class BusinessObject(Slugged, Described, Hyperlinked):
  pass
