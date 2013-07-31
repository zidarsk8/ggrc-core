
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import BusinessObject, Timeboxed
from .object_control import Controllable
from .object_document import Documentable
from .object_objective import Objectiveable
from .object_person import Personable
from .object_section import Sectionable

class OrgGroup(
    Documentable, Personable, Objectiveable, Controllable, Sectionable,
    Timeboxed, BusinessObject, db.Model):
  __tablename__ = 'org_groups'
