# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

from sqlalchemy.orm import validates
from ggrc import db
from ggrc.models.mixins import Assignable
from ggrc.models.mixins import BusinessObject
from ggrc.models.mixins import CustomAttributable
from ggrc.models.mixins import TestPlanned
from ggrc.models.mixins import Timeboxed
from ggrc.models.mixins import deferred
from ggrc.models.object_document import Documentable
from ggrc.models.object_owner import Ownable
from ggrc.models.object_person import Personable
from ggrc.models.reflection import PublishOnly
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import HasObjectState
from ggrc.models.track_object_state import track_state_for_class


class Assessment(Assignable, HasObjectState, TestPlanned, CustomAttributable,
                 Documentable, Personable, Timeboxed, Ownable,
                 Relatable, BusinessObject, db.Model):
  __tablename__ = 'assessments'

  VALID_STATES = (u'Open', u'In Progress', u'Finished', u'Verified', u'Final')
  ASSIGNEE_TYPES = (u'Assessor', u'Verifier')

  status = deferred(db.Column(db.Enum(*VALID_STATES), nullable=False),
                    'Assessment')

  design = deferred(db.Column(db.String), 'Assessment')
  operationally = deferred(db.Column(db.String), 'Assessment')

  audit = {}  # we add this for the sake of client side error checking

  VALID_CONCLUSIONS = frozenset([
      "Effective",
      "Ineffective",
      "Needs improvement",
      "Not Applicable"
  ])

  # REST properties
  _publish_attrs = [
      'design',
      'operationally',
      PublishOnly('audit')
  ]

  _aliases = {
      "audit": {
          "display_name": "Audit",
          "mandatory": True,
      },
      "url": "Assessment URL",
      "design": "Conclusion: Design",
      "operationally": "Conclusion: Operation",
  }

  def validate_conclusion(self, value):
    return value if value in self.VALID_CONCLUSIONS else ""

  @validates("operationally")
  def validate_opperationally(self, key, value):
    return self.validate_conclusion(value)

  @validates("design")
  def validate_design(self, key, value):
    return self.validate_conclusion(value)

track_state_for_class(Assessment)
