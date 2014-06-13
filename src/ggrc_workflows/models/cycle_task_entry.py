# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc import db
from ggrc.models.mixins import Base, Described


class CycleTaskEntry(Described, Base, db.Model):
  __tablename__ = 'cycle_task_entries'

  cycle_task_group_object_task_id = db.Column(
      db.Integer,
      db.ForeignKey('cycle_task_group_object_tasks.id'),
      nullable=False
      )
  cycle_task_group_object_task = db.relationship(
    'CycleTaskGroupObjectTask',
    foreign_keys='CycleTaskEntry.cycle_task_group_object_task_id'
    )

  _publish_attrs = [
      'cycle_task_group_object_task',
      ]
