# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc import db
from ggrc.models.mixins import (
    Base, Titled, Described, Timeboxed, Stateful, WithContact
    )


class CycleTaskGroupObject(
    WithContact, Stateful, Timeboxed, Described, Titled, Base, db.Model):
  __tablename__ = 'cycle_task_group_objects'
  _title_uniqueness = False

  VALID_STATES = (None, u'InProgress', u'Finished', u'Verified')

  cycle_id = db.Column(
      db.Integer, db.ForeignKey('cycles.id'), nullable=False)
  cycle_task_group_id = db.Column(
      db.Integer, db.ForeignKey('cycle_task_groups.id'), nullable=False)
  task_group_object_id = db.Column(
      db.Integer, db.ForeignKey('task_group_objects.id'), nullable=False)
  task_group_object = db.relationship(
    "TaskGroupObject",
    foreign_keys="CycleTaskGroupObject.task_group_object_id"
    )
  cycle_task_group_object_tasks = db.relationship(
      'CycleTaskGroupObjectTask',
      backref='cycle_task_group_object',
      cascade='all, delete-orphan'
      )

  _publish_attrs = [
      'cycle',
      'cycle_task_group',
      'task_group_object',
      'cycle_task_group_object_tasks',
      ]
