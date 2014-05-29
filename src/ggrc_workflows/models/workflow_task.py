# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref

from ggrc import db
from ggrc.models.mixins import deferred, Mapping, Timeboxed
from ggrc.models.reflection import PublishOnly


class WorkflowTask(Timeboxed, Mapping, db.Model):
  __tablename__ = 'workflow_tasks'

  workflow_id = db.Column(
      db.Integer, db.ForeignKey('workflows.id'), nullable=False)
  #workflow = db.relationship(
  #    'Workflow', backref=backref('workflow_tasks', cascade='all, delete-orphan'))
  task_id = db.Column(
      db.Integer, db.ForeignKey('tasks.id'), nullable=False)
  task = db.relationship(
      'Task', backref=backref('workflow_tasks', cascade='all, delete-orphan'))

  @staticmethod
  def _extra_table_args(cls):
    return (
        db.UniqueConstraint('workflow_id', 'task_id'),
        #db.Index('ix_workflow_id', 'workflow_id'),
        #db.Index('ix_task_id', 'task_id'),
        )

  _publish_attrs = [
      'workflow',
      'task',
      ]
  _sanitize_html = [
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(WorkflowTask, cls).eager_query()
    return query.options(
        orm.subqueryload('workflow'),
        orm.subqueryload('task'),
        )

  def _display_name(self):
    return self.task.display_name + '<->' + self.workflow.display_name
