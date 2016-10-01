# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc import db
from .mixins import BusinessObject, CustomAttributable
from .object_owner import Ownable
from .object_person import Personable
from .audit_object import Auditable
from .track_object_state import HasObjectState, track_state_for_class
from .relationship import Relatable


class Objective(HasObjectState, CustomAttributable, Auditable, Relatable,
                Personable, Ownable, BusinessObject, db.Model):
  __tablename__ = 'objectives'
  _publish_attrs = []
  _include_links = []
  _aliases = {"url": "Objective URL"}

track_state_for_class(Objective)
