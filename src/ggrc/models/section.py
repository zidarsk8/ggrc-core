
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc import db
from .associationproxy import association_proxy
from .mixins import BusinessObject, Hierarchical

class Section(Hierarchical, BusinessObject, db.Model):
  __tablename__ = 'sections'

  directive_id = db.Column(db.Integer, db.ForeignKey('directives.id'))
  na = db.Column(db.Boolean, default=False, nullable=False)
  notes = db.Column(db.Text)
  control_sections = db.relationship('ControlSection', backref='section')
  controls = association_proxy('control_sections', 'control', 'ControlSection')
  section_objectives = db.relationship('SectionObjective', backref='section')
  objectives = association_proxy('section_objectives', 'objective', 'SectionObjective')

  _publish_attrs = [
      'directive',
      'na',
      'notes',
      'control_sections',
      'controls',
      'section_objectives',
      'objectives',
      ]
  _update_attrs = [
      'directive',
      'na',
      'notes',
      'controls',
      'objectives',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Section, cls).eager_query()
    return query.options(
        orm.joinedload('directive'),
        orm.subqueryload_all('control_sections.control'),
        orm.subqueryload_all('section_objectives.objective'))
