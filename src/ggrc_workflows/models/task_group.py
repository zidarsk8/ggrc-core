# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc import db
from ggrc.models.mixins import (
    Titled, Slugged, Described, Timeboxed, WithContact
    )


class TaskGroup(
    WithContact, Timeboxed, Described, Titled, Slugged, db.Model):
  __tablename__ = 'task_groups'

  workflow_id = db.Column(
      db.Integer, db.ForeignKey('workflows.id'), nullable=False)

  _publish_attrs = [
      'workflow'
      ]
