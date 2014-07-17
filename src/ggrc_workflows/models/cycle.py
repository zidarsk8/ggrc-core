# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc import db
from ggrc.models.mixins import (
    Slugged, Titled, Described, Timeboxed, Stateful, WithContact
    )
from sqlalchemy.ext.hybrid import hybrid_property


class Cycle(
    WithContact, Stateful, Timeboxed, Described, Titled, Slugged, db.Model):
  __tablename__ = 'cycles'
  _title_uniqueness = False

  VALID_STATES = (None, u'InProgress', u'Finished', u'Verified')

  workflow_id = db.Column(
      db.Integer, db.ForeignKey('workflows.id'), nullable=False)
  cycle_task_groups = db.relationship(
      'CycleTaskGroup', backref='cycle', cascade='all, delete-orphan')
  cycle_task_group_objects = db.relationship(
      'CycleTaskGroupObject', backref='cycle', cascade='all, delete-orphan')
  cycle_task_group_object_tasks = db.relationship(
      'CycleTaskGroupObjectTask', backref='cycle', cascade='all, delete-orphan')
  cycle_task_entries = db.relationship(
      'CycleTaskEntry', backref='cycle', cascade='all, delete-orphan')
  is_current = db.Column(db.Boolean, default=True, nullable=False)

  @hybrid_property
  def cycle_task_group_object_objects(self):
    return [o.object for o in self.cycle_task_group_objects]

  _publish_attrs = [
      'workflow',
      'cycle_task_groups',
      'is_current',
      ]
