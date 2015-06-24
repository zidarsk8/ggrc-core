# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: laran@reciprocitylabs.com
# Maintained By: laran@reciprocitylabs.com

from ggrc import db
from .mixins import BusinessObject, Timeboxed, CustomAttributable
from .object_document import Documentable
from .object_owner import Ownable
from .object_person import Personable
from .relationship import Relatable
from .track_object_state import HasObjectState, track_state_for_class


class Vendor(HasObjectState, CustomAttributable, Documentable, Personable,
             Relatable, Timeboxed, Ownable, BusinessObject, db.Model):
  __tablename__ = 'vendors'

  _aliases = {
      "url": "Vendor URL",
      "reference_url": "Reference URL",
  }

track_state_for_class(Vendor)
