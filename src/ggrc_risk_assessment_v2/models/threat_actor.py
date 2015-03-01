# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

from ggrc import db
from ggrc.models.mixins import CustomAttributable, BusinessObject, Timeboxed
from ggrc.models.object_control import Controllable
from ggrc.models.object_document import Documentable
from ggrc.models.object_objective import Objectiveable
from ggrc.models.object_person import Personable
from ggrc.models.object_owner import Ownable
from ggrc.models.object_section import Sectionable
from ggrc.models.relationship import Relatable


class ThreatActor(
    CustomAttributable, Documentable, Personable, Objectiveable, Controllable,
    Sectionable, Relatable, Timeboxed, Ownable, BusinessObject, db.Model):
  __tablename__ = 'threat_actors'
