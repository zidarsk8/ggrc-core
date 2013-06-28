# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import Base

class ControlSection(Base, db.Model):
  __tablename__ = 'control_sections'

  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'), nullable=False)
  section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)

  __table_args__ = (
    db.UniqueConstraint('control_id', 'section_id'),
  )

  _publish_attrs = [
      'control',
      'section',
      ]
