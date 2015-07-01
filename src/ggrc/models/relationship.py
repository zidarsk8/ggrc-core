# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import ggrc.models
from ggrc import db
from .mixins import deferred, Base, Described, Mapping
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import or_, and_

class Relationship(Mapping, db.Model):
  __tablename__ = 'relationships'
  source_id = db.Column(db.Integer, nullable=False)
  source_type = db.Column(db.String, nullable=False)
  destination_id = db.Column(db.Integer, nullable=False)
  destination_type = db.Column(db.String, nullable=False)
  relationship_type_id = db.Column(db.String)
  # FIXME: Should this be a strict constraint?  If so, a migration is needed.
  #relationship_type_id = db.Column(
  #    db.Integer, db.ForeignKey('relationship_types.id'))
  relationship_type = db.relationship(
      'RelationshipType',
      primaryjoin='foreign(RelationshipType.relationship_type) =='
      ' Relationship.relationship_type_id',
      uselist=False
  )
  automapping_id = db.Column(
      db.Integer,
      db.ForeignKey('relationships.id', ondelete='SET NULL'),
      nullable=True,
  )
  automapping = db.relationship(
      lambda: Relationship,
      remote_side=lambda: Relationship.id
  )

  @property
  def source_attr(self):
    return '{0}_source'.format(self.source_type)

  @property
  def source(self):
    return getattr(self, self.source_attr)

  @source.setter
  def source(self, value):
    self.source_id = value.id if value is not None else None
    self.source_type = value.__class__.__name__ if value is not None else None
    return setattr(self, self.source_attr, value)

  @property
  def destination_attr(self):
    return '{0}_destination'.format(self.destination_type)

  @property
  def destination(self):
    return getattr(self, self.destination_attr)

  @destination.setter
  def destination(self, value):
    self.destination_id = value.id if value is not None else None
    self.destination_type = value.__class__.__name__ if value is not None \
        else None
    return setattr(self, self.destination_attr, value)

  @classmethod
  def find_related(cls, object1, object2):
    def predicate(src, dst):
      return and_(
          Relationship.source_type == src.type,
          Relationship.source_id == src.id,
          Relationship.destination_type == dst.type,
          Relationship.destination_id == dst.id
      )
    return Relationship.query.filter(
        or_(predicate(object1, object2), predicate(object2, object1))
    ).first()

  @staticmethod
  def _extra_table_args(cls):
    return (
        db.UniqueConstraint(
            'source_id', 'source_type', 'destination_id', 'destination_type'),
        db.Index(
            'ix_relationships_source',
            'source_type', 'source_id'),
        db.Index(
            'ix_relationships_destination',
            'destination_type', 'destination_id'),
    )

  _publish_attrs = [
      'source',
      'destination',
      'relationship_type_id',
  ]

  def _display_name(self):
    return self.source.display_name + '<->' + self.destination.display_name


class RelationshipType(Described, Base, db.Model):
  __tablename__ = 'relationship_types'
  relationship_type = deferred(db.Column(db.String), 'RelationshipType')
  forward_phrase = deferred(db.Column(db.String), 'RelationshipType')
  backward_phrase = deferred(db.Column(db.String), 'RelationshipType')
  symmetric = deferred(
      db.Column(db.Boolean, nullable=False), 'RelationshipType')

  _publish_attrs = [
      'forward_phrase',
      'backward_phrase',
      'symmetric',
  ]


class Relatable(object):

  @declared_attr
  def related_sources(cls):
    joinstr = 'and_(remote(Relationship.destination_id) == {type}.id, '\
        'remote(Relationship.destination_type) == "{type}")'
    joinstr = joinstr.format(type=cls.__name__)
    return db.relationship(
        'Relationship',
        primaryjoin=joinstr,
        foreign_keys='Relationship.destination_id',
        backref='{0}_destination'.format(cls.__name__),
        cascade='all, delete-orphan')

  @declared_attr
  def related_destinations(cls):
    joinstr = 'and_(remote(Relationship.source_id) == {type}.id, '\
        'remote(Relationship.source_type) == "{type}")'
    joinstr = joinstr.format(type=cls.__name__)
    return db.relationship(
        'Relationship',
        primaryjoin=joinstr,
        foreign_keys='Relationship.source_id',
        backref='{0}_source'.format(cls.__name__),
        cascade='all, delete-orphan')

  _publish_attrs = [
      'related_sources',
      'related_destinations'
  ]

  _include_links = []

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Relatable, cls).eager_query()
    return cls.eager_inclusions(query, Relatable._include_links).options(
        orm.subqueryload('related_sources'),
        orm.subqueryload('related_destinations'))


class RelationshipHelper(object):

  @classmethod
  def get_ids_related_to(cls, object_type, related_type, related_ids=[]):
    """ get ids of objects

    Get a list of all ids for object with object_type, that are related to any
    of the objects with type related_type and id in related_ids
    """
    if isinstance(related_ids, (int, long)):
      related_ids = [related_ids]

    by_source = Relationship.query.filter(and_(
        Relationship.destination_type == object_type,
        Relationship.source_type == related_type,
        Relationship.source_id.in_(related_ids),
    )).all()
    by_destination = Relationship.query.filter(and_(
        Relationship.source_type == object_type,
        Relationship.destination_type == related_type,
        Relationship.destination_id.in_(related_ids),
    )).all()
    destination_ids = [r.destination_id for r in by_source]
    source_ids = [r.source_id for r in by_destination]
    return source_ids + destination_ids
