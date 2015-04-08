# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

from ggrc import db
from .mixins import (
    deferred, BusinessObject, Timeboxed, CustomAttributable, TestPlanned
)
from .object_document import Documentable
from .object_owner import Ownable
from .object_person import Personable
from .relationship import Relatable
from .track_object_state import HasObjectState, track_state_for_class
from ggrc.models.reflection import PublishOnly


class ControlAssessment(HasObjectState, TestPlanned, CustomAttributable, Documentable,
                        Personable, Timeboxed, Ownable, Relatable,
                        BusinessObject, db.Model):
  __tablename__ = 'control_assessments'

  design = deferred(db.Column(db.String), 'ControlAssessment')
  operationally = deferred(db.Column(db.String), 'ControlAssessment')

  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
  control = db.relationship('Control', foreign_keys=[control_id])

  # REST properties
  _publish_attrs = [
      'design',
      'operationally',
      'control'
  ]

track_state_for_class(ControlAssessment)
