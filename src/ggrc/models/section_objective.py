# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc import db
from .mixins import Base

class SectionObjective(Base, db.Model):
  __tablename__ = 'section_objectives'

  section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
  objective_id = db.Column(db.Integer, db.ForeignKey('objectives.id'))

  _publish_attrs = [
      'section',
      'objective',
      ]
