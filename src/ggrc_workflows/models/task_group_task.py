# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

import datetime, calendar

from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from ggrc.models.mixins import (
    deferred, Base, Titled, Slugged, Described, Timeboxed, WithContact
    )
from ggrc.models.reflection import PublishOnly


class RelativeTimeboxed(Timeboxed):
  # Frequencies and offset:
  #   annual:
  #     month is the 0-indexed month (0 is January)
  #     day is the 0-indexed offset day
  #   quarterly:
  #     month is in [0,1,2], as the offset within the quarter
  #     day is same as annual
  #   weekly:
  #     month is ignored
  #     day is in [1,2,3,4,5] where 0 is Monday

  relative_start_month = db.Column(db.Integer, nullable=True)
  relative_start_day = db.Column(db.Integer, nullable=True)
  relative_end_month = db.Column(db.Integer, nullable=True)
  relative_end_day = db.Column(db.Integer, nullable=True)

  @staticmethod
  def _normalize_date(year, month, day):
    """Given (year, month, day) after a naive addition, e.g., where it's
    possible month > 12 and/or day > 31, etc, normalize to a valid date
    """
    if month > 12:
      year = year + 1
      month = month - 12
    if calendar.monthrange(year, month)[1] < day:
      day = day - calendar.monthrange(year, month)[1]
      month = month + 1
    if month > 12:
      year = year + 1
      month = month - 12
    return datetime.date(year, month, day)

  @staticmethod
  def _nearest_work_day(date_, direction):
    holidays = []
    while date_.weekday() > 4 or date_ in holidays:
      date_ = date_ + datetime.timedelta(direction)
    return date_

  @staticmethod
  def _calc_base_date(start_date, frequency):
    if frequency == 'one_time':
      base_date = start_date
    elif frequency == 'weekly':
      base_date = start_date - datetime.timedelta(start_date.weekday())
    elif frequency == 'monthly':
      base_date = datetime.date(start_date.year, start_date.month, 1)
    elif frequency == 'quarterly':
      base_month = start_date.month - ((start_date.month - 1) % 3)
      base_date = datetime.date(start_date.year, base_month, 1)
    elif frequency == 'annually':
      base_date = datetime.date(start_date.year, 1, 1)
    return base_date

  @classmethod
  def _calc_relative_date(cls, base_date, frequency, rel_month, rel_day):
    base_date = cls._calc_base_date(base_date, frequency)

    if frequency == "one_time":
      ret = base_date
    elif frequency == "annually":
      ret = cls._normalize_date(
          base_date.year, rel_month, rel_day)
    elif frequency == "monthly":
      ret = cls._normalize_date(
          base_date.year, base_date.month, rel_day)
    elif frequency == "quarterly":
      new_month = base_date.month + rel_month - 1
      ret = cls._normalize_date(base_date.year, new_month, rel_day)
    elif frequency == "weekly":
      new_day = base_date.day - base_date.weekday() + rel_day - 1
      if new_day < 0:
        new_day = new_day + 7
      ret = cls._normalize_date(base_date.year, base_date.month, new_day)
    return ret

  @classmethod
  def _calc_start_date(
      cls, base_date, frequency, rel_month, rel_day):
    new_date = cls._calc_relative_date(base_date, frequency, rel_month, rel_day)
    new_date = cls._nearest_work_day(new_date, direction=1)
    return new_date

  @classmethod
  def _calc_end_date(
      cls, base_date, frequency, rel_month, rel_day):
    new_date = cls._calc_relative_date(base_date, frequency, rel_month, rel_day)
    new_date = cls._nearest_work_day(new_date, direction=-1)
    return new_date

  def calc_start_date(self, base_date):
    if self.task_group.workflow.frequency in ("one_time", "continuous"):
      return self.start_date
    else:
      return self._calc_start_date(
          base_date, self.task_group.workflow.frequency,
          self.relative_start_month, self.relative_start_day)

  def calc_end_date(self, base_date):
    if self.task_group.workflow.frequency in ("one_time", "continuous"):
      return self.end_date
    else:
      return self._calc_end_date(
          base_date, self.task_group.workflow.frequency,
          self.relative_end_month, self.relative_end_day)


class TaskGroupTask(
    WithContact, Titled, Described, RelativeTimeboxed, Base,
    db.Model):
  __tablename__ = 'task_group_tasks'

  task_group_id = db.Column(
      db.Integer, db.ForeignKey('task_groups.id'), nullable=False)
  sort_index = db.Column(
      db.String(length=250), default="", nullable=False)
  object_approval = db.Column(
      db.Boolean, nullable=False, default=False)

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
      'object_approval',
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
