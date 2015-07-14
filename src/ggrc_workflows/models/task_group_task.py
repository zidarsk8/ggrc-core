# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from sqlalchemy import orm
from sqlalchemy.orm import validates

from ggrc import db
from ggrc.login import get_current_user
from ggrc.models.mixins import Base, Titled, Described, WithContact
from ggrc.models.types import JsonType
from ggrc_workflows.models.mixins import RelativeTimeboxed


class TaskGroupTask(WithContact, Titled, Described, RelativeTimeboxed, Base,
                    db.Model):
  __tablename__ = 'task_group_tasks'
  _title_uniqueness = False

  @classmethod
  def default_task_type(cls):
    return "text"

  task_group_id = db.Column(
      db.Integer, db.ForeignKey('task_groups.id'), nullable=False)
  sort_index = db.Column(
      db.String(length=250), default="", nullable=False)
  object_approval = db.Column(
      db.Boolean, nullable=False, default=False)
  task_type = db.Column(
      db.String(length=250), default=default_task_type, nullable=False)
  response_options = db.Column(
      JsonType(), nullable=False, default='[]')

  VALID_TASK_TYPES = ['text', 'menu', 'checkbox']

  @validates('task_type')
  def validate_task_type(self, key, value):
    if value is None:
      value = self.default_task_type()
    if value not in self.VALID_TASK_TYPES:
      message = u"Invalid type '{}'".format(value)
      raise ValueError(message)
    return value

  _publish_attrs = [
      'task_group',
      'sort_index',
      'relative_start_month',
      'relative_start_day',
      'relative_end_month',
      'relative_end_day',
      'object_approval',
      'task_type',
      'response_options'
  ]
  _sanitize_html = []
  _aliases = {
      "title": "Summary",
      "description": "Task Description",
      "contact": {
          "display_name": "Assignee",
          "mandatory": True,
      },
      "secondary_contact": None,
      "start_date": None,
      "end_date": None,
      "task_group": {
          "display_name": "Task Group",
          "mandatory": True,
      },
      "relative_start_date": {
          "display_name": "Start",
          "mandatory": True,
      },
      "relative_end_date": {
          "display_name": "End",
          "mandatory": True,
      },
      "task_type": {
          "display_name": "Task Type",
          "mandatory": True,
      }
  }

  @classmethod
  def eager_query(cls):
    query = super(TaskGroupTask, cls).eager_query()
    return query.options(
        orm.subqueryload('task_group'),
    )

  def _display_name(self):
    return self.title + '<->' + self.task_group.display_name

  def copy(self, _other=None, **kwargs):
    columns = [
        'title', 'description',
        'task_group', 'sort_index',
        'relative_start_month', 'relative_start_day',
        'relative_end_month', 'relative_end_day',
        'start_date', 'end_date',
        'contact', 'modified_by',
        'task_type', 'response_options',
    ]

    contact = None
    if(kwargs.get('clone_people', False)):
      contact = self.contact
    else:
      contact = get_current_user()

    kwargs['modified_by'] = get_current_user()

    target = self.copy_into(_other, columns, contact=contact, **kwargs)
    return target
