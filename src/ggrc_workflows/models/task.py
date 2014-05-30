# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc import db
from ggrc.models.mixins import Base, Titled, Slugged, Described, Timeboxed


class Task(Timeboxed, Described, Titled, Slugged, Base, db.Model):
  __tablename__ = 'tasks'
