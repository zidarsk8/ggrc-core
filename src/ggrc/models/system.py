# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from sqlalchemy.ext.declarative import declared_attr
from .associationproxy import association_proxy
from .mixins import deferred, BusinessObject, Timeboxed
from .categorization import Categorizable
from .object_control import Controllable
from .object_document import Documentable
from .object_objective import Objectiveable
from .object_person import Personable
from .object_section import Sectionable

CATEGORY_SYSTEM_TYPE_ID = 101

class SystemCategorized(Categorizable):
  @declared_attr
  def categorizations(cls):
    return cls._categorizations(
        'categorizations', 'categories', CATEGORY_SYSTEM_TYPE_ID)

class System(
    Documentable, Personable, Objectiveable, Controllable, Sectionable,
    Timeboxed, SystemCategorized, BusinessObject, db.Model):
  __tablename__ = 'systems'

  infrastructure = deferred(db.Column(db.Boolean), 'System')
  # TODO: unused?
  owner_id = deferred(db.Column(db.Integer, db.ForeignKey('people.id')), 'System')
  is_biz_process = deferred(db.Column(db.Boolean, default=False), 'System')
  # TODO: handle option
  type_id = deferred(db.Column(db.Integer), 'System')
  version = deferred(db.Column(db.String), 'System')
  notes = deferred(db.Column(db.Text), 'System')
  # TODO: handle option
  network_zone_id = deferred(db.Column(db.Integer), 'System')

  system_controls = db.relationship('SystemControl', backref='system', cascade='all, delete-orphan')
  controls = association_proxy('system_controls', 'control', 'SystemControl')
  responses = db.relationship('Response', backref='system', cascade='all, delete-orphan')
  #TODO What about system_section?
  owner = db.relationship('Person', uselist=False)
  sub_system_systems = db.relationship(
      'SystemSystem', foreign_keys='SystemSystem.parent_id', backref='parent', cascade='all, delete-orphan')
  sub_systems = association_proxy(
      'sub_system_systems', 'child', 'SystemSystem')
  super_system_systems = db.relationship(
      'SystemSystem', foreign_keys='SystemSystem.child_id', backref='child', cascade='all, delete-orphan')
  super_systems = association_proxy(
      'super_system_systems', 'parent', 'SystemSystem')
  type = db.relationship(
      'Option',
      primaryjoin='and_(foreign(System.type_id) == Option.id, '\
                       'Option.role == "system_type")',
      uselist=False,
      )
  network_zone = db.relationship(
      'Option',
      primaryjoin='and_(foreign(System.network_zone_id) == Option.id, '\
                       'Option.role == "network_zone")',
      uselist=False,
      )

  # REST properties
  _publish_attrs = [
      'infrastructure',
      'is_biz_process',
      'type',
      'version',
      'notes',
      'network_zone',
      'system_controls',
      'controls',
      'responses',
      'owner',
      'sub_system_systems',
      'sub_systems',
      'super_system_systems',
      'super_systems',
      ]
  _update_attrs = [
      'infrastructure',
      'is_biz_process',
      'type',
      'version',
      'notes',
      'network_zone',
      'controls',
      'responses',
      'owner',
      'sub_systems',
      'super_systems',
      ]

  def kind_model(self):
    return Process if self.is_biz_process else System

  _kind_plural = 'systems'
  @property
  def kind_plural(self):
    return self.kind_model()._kind_plural

  @property
  def kind_singular(self):
    return self.kind_model().__name__

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(System, cls).eager_query()
    return query.options(
        orm.joinedload('type'),
        orm.joinedload('network_zone'),
        orm.subqueryload('responses'),
        orm.subqueryload_all('system_controls.control'),
        orm.subqueryload_all('sub_system_systems.child'),
        orm.subqueryload_all('super_system_systems.parent'))

class Process(System):
  _kind_plural = 'processes'
