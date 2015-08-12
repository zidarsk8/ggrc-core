# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc import db
from ggrc.models.associationproxy import association_proxy
from ggrc.models.mixins import (
    Titled, Slugged, Described, Timeboxed, WithContact
)
from ggrc.models.reflection import AttributeInfo
from ggrc.models.reflection import PublishOnly


class TaskGroup(
        WithContact, Timeboxed, Described, Titled, Slugged, db.Model):
  __tablename__ = 'task_groups'
  _title_uniqueness = False

  workflow_id = db.Column(
      db.Integer, db.ForeignKey('workflows.id'), nullable=False)

  lock_task_order = db.Column(db.Boolean(), nullable=True)

  task_group_objects = db.relationship(
      'TaskGroupObject', backref='task_group', cascade='all, delete-orphan')

  objects = association_proxy(
      'task_group_objects', 'object', 'TaskGroupObject')

  task_group_tasks = db.relationship(
      'TaskGroupTask', backref='task_group', cascade='all, delete-orphan')

  cycle_task_groups = db.relationship(
      'CycleTaskGroup', backref='task_group')

  sort_index = db.Column(
      db.String(length=250), default="", nullable=False)

  _publish_attrs = [
      'workflow',
      'task_group_objects',
      PublishOnly('objects'),
      'task_group_tasks',
      'lock_task_order',
      'sort_index',
      # Intentionally do not include `cycle_task_groups`
      # 'cycle_task_groups',
  ]

  _aliases = {
      "title": "Summary",
      "description": "Details",
      "contact": {
          "display_name": "Assignee",
          "mandatory": True,
      },
      "secondary_contact": None,
      "start_date": None,
      "end_date": None,
      "workflow": {
          "display_name": "Workflow",
          "mandatory": True,
      },
      "task_group_objects": {
          "display_name": "Objects",
          "type": AttributeInfo.Type.SPECIAL_MAPPING,
      },
  }

  def copy(self, _other=None, **kwargs):
    columns = [
        'title', 'description', 'workflow', 'sort_index', 'modified_by',
        'context'
    ]

    if(kwargs.get('clone_people', False)):
      columns.append('contact')

    target = self.copy_into(_other, columns, **kwargs)

    if kwargs.get('clone_objects', False):
      self.copy_objects(target, **kwargs)

    if kwargs.get('clone_tasks', False):
      self.copy_tasks(target, **kwargs)

    return target

  def copy_objects(self, target, **kwargs):
    for task_group_object in self.task_group_objects:
      target.task_group_objects.append(task_group_object.copy(
          task_group=target,
          context=target.context,
      ))

    return target

  def copy_tasks(self, target, **kwargs):
    for task_group_task in self.task_group_tasks:
      target.task_group_tasks.append(task_group_task.copy(
          None,
          task_group=target,
          context=target.context,
          clone_people=kwargs.get("clone_people", False),
      ))

    return target
