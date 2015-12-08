# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

from ggrc import db
from .mixins import (
    BusinessObject, Timeboxed, CustomAttributable, TestPlanned
)
from .object_document import Documentable
from .object_owner import Ownable
from .object_person import Personable
from .relationship import Relatable
from .track_object_state import HasObjectState, track_state_for_class


class Issue(HasObjectState, TestPlanned, CustomAttributable, Documentable,
            Personable, Timeboxed, Ownable, Relatable,
            BusinessObject, db.Model):

  __tablename__ = 'issues'

  # REST properties
  _publish_attrs = [
  ]

  _aliases = {"url": "Issue URL"}

track_state_for_class(Issue)
