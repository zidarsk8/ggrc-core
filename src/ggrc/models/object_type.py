# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: miha@reciprocitylabs.com

"""
 GGRC notification SQLAlchemy layer data model extensions
"""

from sqlalchemy.orm import backref
from sqlalchemy import event

from ggrc import db
from .mixins import Base, Stateful



class ObjectType(Base, db.Model):
  __tablename__ = 'object_types'

  name = db.Column(db.String, nullable=False)
  description = db.Column(db.Text, nullable=True)


