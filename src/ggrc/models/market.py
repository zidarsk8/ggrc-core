# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc import db
from .mixins import BusinessObject, Timeboxed, CustomAttributable
from .object_person import Personable
from .object_owner import Ownable
from .relationship import Relatable
from .track_object_state import HasObjectState, track_state_for_class


class Market(HasObjectState, CustomAttributable, Personable,
             Relatable, Timeboxed, Ownable,
             BusinessObject, db.Model):
  __tablename__ = 'markets'
  _aliases = {"url": "Market URL"}

track_state_for_class(Market)
