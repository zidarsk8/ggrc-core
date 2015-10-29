# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

from ggrc import db
from ggrc.models.mixins import Base, Described
from ggrc.models.object_document import Documentable


class Comment(Described, Documentable, Base, db.Model):
  __tablename__ = "comments"
