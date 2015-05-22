# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc import db
from .associationproxy import association_proxy
from .mixins import BusinessObject, CustomAttributable
from .object_document import Documentable
from .object_owner import Ownable
from .object_person import Personable
from .audit_object import Auditable
from .reflection import PublishOnly
from .track_object_state import HasObjectState, track_state_for_class
from .relationship import Relatable


class Objective(HasObjectState, CustomAttributable, Auditable, Relatable,
                Documentable, Personable, Ownable, BusinessObject, db.Model):
  __tablename__ = 'objectives'

  section_objectives = db.relationship(
      'SectionObjective', backref='objective', cascade='all, delete-orphan')
  sections = association_proxy(
      'section_objectives', 'section', 'SectionObjective')

  _publish_attrs = [
      PublishOnly('section_objectives'),
      'sections',
  ]

  _include_links = []

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Objective, cls).eager_query()
    return cls.eager_inclusions(query, Objective._include_links).options(
        orm.subqueryload('section_objectives').joinedload('section'))

track_state_for_class(Objective)
