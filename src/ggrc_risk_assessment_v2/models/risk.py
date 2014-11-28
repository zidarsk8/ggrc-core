# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: silas@reciprocitylabs.com
# Maintained By: silas@reciprocitylabs.com

from sqlalchemy.ext.declarative import declared_attr

from ggrc import db
from ggrc.models.associationproxy import association_proxy
from ggrc.models.object_owner import Ownable
from ggrc.models.object_control import Controllable
from ggrc.models.object_document import Documentable
from ggrc.models.object_objective import Objectiveable
from ggrc.models.mixins import Base, Described, Slugged, Titled, WithContact, deferred, Stateful, Timeboxed
from ggrc.models.reflection import PublishOnly
from ggrc.models.relationship import Relatable


class Risk(Stateful, Relatable, Controllable, Objectiveable, Documentable, Described,
    Ownable, WithContact, Titled, Timeboxed, Slugged, Base, db.Model):
  __tablename__ = 'risks'

  VALID_STATES = [
      'Draft',
      'Final',
      'Effective',
      'Ineffective',
      'Launched',
      'Not Launched',
      'In Scope',
      'Not in Scope',
      'Deprecated',
      ]

  # Overriding mixin to make mandatory
  @declared_attr
  def description(cls):
    return deferred(db.Column(db.Text, nullable=False), cls.__name__)

  risk_objects = db.relationship(
      'RiskObject', backref='risk', cascade='all, delete-orphan')
  objects = association_proxy(
      'risk_objects', 'object', 'RiskObject')

  _publish_attrs = [
      'risk_objects',
      PublishOnly('objects'),
      ]
