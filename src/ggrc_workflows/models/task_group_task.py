# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from ggrc.models.mixins import (
    deferred, Base, Titled, Slugged, Described, Timeboxed, WithContact
    )
from ggrc.models.reflection import PublishOnly


class TaskGroupTask(
    WithContact, Titled, Described, Timeboxed, Base, db.Model):
  __tablename__ = 'task_group_tasks'

  task_group_id = db.Column(
      db.Integer, db.ForeignKey('task_groups.id'), nullable=False)
  sort_index = db.Column(
      db.String(length=250), default="", nullable=False)

  # Frequencies and offset:
  #   annual:
  #     month is the 1-indexed month (1 is January)
  #     day is the one-indexed offset day
  #   quarterly:
  #     month is in [0,1,2], as the offset within the quarter
  #     day is same as annual
  #   weekly:
  #     month is ignored
  #     day is in [0,1,2,3,4] where 0 is Monday

  relative_start_month = db.Column(db.Integer, nullable=True)
  relative_start_day = db.Column(db.Integer, nullable=True)
  relative_end_month = db.Column(db.Integer, nullable=True)
  relative_end_day = db.Column(db.Integer, nullable=True)

  @staticmethod
  def _extra_table_args(cls):
    return (
        #db.UniqueConstraint('task_group_id', 'task_id'),
        #db.Index('ix_task_group_id', 'task_group_id'),
        #db.Index('ix_task_id', 'task_id'),
        )

  _publish_attrs = [
      'task_group',
      'sort_index',
      'relative_start_month',
      'relative_start_day',
      'relative_end_month',
      'relative_end_day',
      ]
  _sanitize_html = []

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

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
        'contact',
        ]
    target = self.copy_into(_other, columns, **kwargs)
    return target
