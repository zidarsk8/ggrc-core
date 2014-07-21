# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: silas@reciprocitylabs.com
# Maintained By: silas@reciprocitylabs.com


from ggrc import db
from ggrc.models.mixins import Base, Titled, Slugged


class Risk(Slugged, Base, db.Model):
  __tablename__ = 'risks'
