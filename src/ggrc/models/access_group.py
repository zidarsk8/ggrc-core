# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

from ggrc import db
from ggrc.models.mixins import BusinessObject, Timeboxed, CustomAttributable
from ggrc.models.object_document import Documentable
from ggrc.models.object_owner import Ownable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import HasObjectState, track_state_for_class


class AccessGroup(HasObjectState,
                  CustomAttributable, Personable, Documentable, Relatable,
                  Timeboxed, Ownable, BusinessObject, db.Model):
    __tablename__ = 'access_groups'

    _aliases = {"url": "Access Group URL"}

track_state_for_class(AccessGroup)
