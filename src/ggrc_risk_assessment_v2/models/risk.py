# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: silas@reciprocitylabs.com
# Maintained By: silas@reciprocitylabs.com

from sqlalchemy.ext.declarative import declared_attr

from ggrc import db
from ggrc.models.object_owner import Ownable
from ggrc.models.mixins import Base, Described, Slugged, Titled, WithContact, deferred


class Risk(Described, Ownable, WithContact, Titled, Slugged, Base, db.Model):
  __tablename__ = 'risks'

  # Overriding mixin to make mandatory
  @declared_attr
  def description(cls):
    return deferred(db.Column(db.Text, nullable=False), cls.__name__)
