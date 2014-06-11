# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc import db
from ggrc.models.mixins import (
    Slugged, Titled, Described, Timeboxed, Stateful, WithContact
    )


class Cycle(
    WithContact, Stateful, Timeboxed, Described, Titled, Slugged, db.Model):
  __tablename__ = 'cycles'
  _title_uniqueness = False

  VALID_STATES = (None, "InProgress", "Completed")

  workflow_id = db.Column(
      db.Integer, db.ForeignKey('workflows.id'), nullable=False)
  cycle_task_groups = db.relationship(
      'CycleTaskGroup', backref='cycle', cascade='all, delete-orphan')

  _publish_attrs = [
      'workflow',
      'cycle_task_groups',
      ]
