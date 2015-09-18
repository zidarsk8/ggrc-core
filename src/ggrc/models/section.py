# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: vraj@reciprocitylabs.com

from sqlalchemy.orm import validates

from ggrc import db
from ggrc.models.exceptions import ValidationError
from ggrc.models.mixins import (
    deferred, Hierarchical, Noted, Described, Hyperlinked, WithContact,
    Titled, Slugged, CustomAttributable, Stateful, Timeboxed
)
from ggrc.models.directive import Directive
from ggrc.models.object_document import Documentable
from ggrc.models.object_owner import Ownable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import track_state_for_class
from ggrc.models.track_object_state import HasObjectState


class Section(HasObjectState, Hierarchical, Noted, Described, Hyperlinked,
              WithContact, Titled, Slugged, Stateful, db.Model,
              CustomAttributable, Documentable, Personable,
              Ownable, Relatable):
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
  __tablename__ = 'sections'
  _table_plural = 'sections'
  _title_uniqueness = False
  _aliases = {
      "url": "Section URL",
      "description": "Text of Section",
      "directive": None
  }


  na = deferred(db.Column(db.Boolean, default=False, nullable=False),
                'Section')
  notes = deferred(db.Column(db.Text), 'Section')

  _publish_attrs = [
      'na',
      'notes',
  ]
  _sanitize_html = ['notes']
  _include_links = []

track_state_for_class(Section)
