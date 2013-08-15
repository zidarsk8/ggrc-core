# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc import db
from .associationproxy import association_proxy
from .mixins import deferred, BusinessObject
from .object_document import Documentable
from .object_person import Personable
from .reflection import PublishOnly

class Objective(Documentable, Personable, BusinessObject, db.Model):
  __tablename__ = 'objectives'

  notes = deferred(db.Column(db.Text), 'Objective')

  section_objectives = db.relationship(
      'SectionObjective', backref='objective', cascade='all, delete-orphan')
  sections = association_proxy(
      'section_objectives', 'section', 'SectionObjective')
  objective_controls = db.relationship(
      'ObjectiveControl', backref='objective', cascade='all, delete-orphan')
  controls = association_proxy(
      'objective_controls', 'control', 'ObjectiveControl')
  object_objectives = db.relationship(
      'ObjectObjective', backref='objective', cascade='all, delete-orphan')

  _publish_attrs = [
      'notes',
      PublishOnly('section_objectives'),
      'sections',
      PublishOnly('objective_controls'),
      'controls',
      'object_objectives',
      ]
  _sanitize_html = [
      'notes',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Objective, cls).eager_query()
    return query.options(
        orm.subqueryload_all('section_objectives.section'),
        orm.subqueryload_all('objective_controls.control'),
        orm.subqueryload_all('object_objectives'))
