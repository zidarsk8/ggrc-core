# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc import db
from ggrc.models.mixins import (
    Titled, Slugged, Described, Timeboxed, WithContact
    )
from ggrc.models.associationproxy import association_proxy
from ggrc.models.reflection import PublishOnly


class TaskGroup(
    WithContact, Timeboxed, Described, Titled, Slugged, db.Model):
  __tablename__ = 'task_groups'

  workflow_id = db.Column(
      db.Integer, db.ForeignKey('workflows.id'), nullable=False)

  lock_task_order = db.Column(db.Boolean(), nullable=True)

  task_group_objects = db.relationship(
      'TaskGroupObject', backref='task_group', cascade='all, delete-orphan')
  objects = association_proxy(
      'task_group_objects', 'object', 'TaskGroupObject')

  task_group_tasks = db.relationship(
      'TaskGroupTask', backref='task_group', cascade='all, delete-orphan')
  tasks = association_proxy(
      'task_group_tasks', 'task', 'TaskGroupTask')

  cycle_task_groups = db.relationship(
      'CycleTaskGroup', backref='task_group', cascade='all, delete-orphan')

  _publish_attrs = [
      'workflow',
      'task_group_objects',
      PublishOnly('objects'),
      'task_group_tasks',
      PublishOnly('tasks'),
      'lock_task_order'
      # Intentionally do not include `cycle_task_groups`
      #'cycle_task_groups',
      ]
