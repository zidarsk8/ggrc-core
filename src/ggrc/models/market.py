# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from .mixins import BusinessObject, Timeboxed, CustomAttributable
from .object_control import Controllable
from .object_document import Documentable
from .object_objective import Objectiveable
from .object_person import Personable
from .object_owner import Ownable
from .object_section import Sectionable
from .relationship import Relatable
from .track_object_state import HasObjectState, track_state_for_class

class Market(HasObjectState,
    CustomAttributable, Documentable, Personable, Objectiveable, Controllable,
    Sectionable, Relatable, Timeboxed, Ownable, BusinessObject, db.Model):
  __tablename__ = 'markets'

track_state_for_class(Market)