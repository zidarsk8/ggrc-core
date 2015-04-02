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


class Issue(HasObjectState, TestPlanned, CustomAttributable, Documentable,
            Personable, Timeboxed, Ownable, Relatable,
            BusinessObject, db.Model):

  __tablename__ = 'issues'

  control = {}
  audit = {}
  program = {}
  control_assessment = {}

  # REST properties
  _publish_attrs = [
      PublishOnly('audit'),
      PublishOnly('control'),
      PublishOnly('program'),
      PublishOnly('control_assessment')
  ]

  _relationship_attrs = [
      'audit',
      'control',
      'program',
      'control_assessment',
  ]

track_state_for_class(Issue)
