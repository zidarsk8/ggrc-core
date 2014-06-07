# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from ggrc.models.mixins import deferred, Mapping, Timeboxed
from ggrc.models.reflection import PublishOnly


class WorkflowObject(Timeboxed, Mapping, db.Model):
  __tablename__ = 'workflow_objects'

  workflow_id = db.Column(
      db.Integer, db.ForeignKey('workflows.id'), nullable=False)
  object_id = db.Column(db.Integer, nullable=False)
  object_type = db.Column(db.String, nullable=False)

  @property
  def object_attr(self):
    return '{0}_object'.format(self.object_type)

  @property
  def object(self):
    return getattr(self, self.object_attr)

  @object.setter
  def object(self, value):
    self.object_id = value.id if value is not None else None
    self.object_type = value.__class__.__name__ if value is not None \
        else None
    return setattr(self, self.object_attr, value)

  @staticmethod
  def _extra_table_args(cls):
    return (
        db.UniqueConstraint('workflow_id', 'object_id', 'object_type'),
        db.Index('ix_workflow_id', 'workflow_id'),
        )

  _publish_attrs = [
      'workflow',
      'object',
      ]
  _sanitize_html = [
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(WorkflowObject, cls).eager_query()
    return query.options(
        orm.subqueryload('workflow'))

  def _display_name(self):
    return self.object.display_name + '<->' + self.workflow.display_name


class Workflowable(object):
  @classmethod
  def late_init_workflowable(cls):
    def make_workflow_objects(cls):
      cls.workflows = association_proxy(
          'workflow_objects', 'workflow',
          creator=lambda workflow: WorkflowObject(
              workflow=workflow,
              object_type=cls.__name__,
              )
          )
      joinstr = 'and_(foreign(WorkflowObject.object_id) == {type}.id, '\
                     'foreign(WorkflowObject.object_type) == "{type}")'
      joinstr = joinstr.format(type=cls.__name__)
      return db.relationship(
          'WorkflowObject',
          primaryjoin=joinstr,
          backref='{0}_object'.format(cls.__name__),
          cascade='all, delete-orphan',
          )
    cls.workflow_objects = make_workflow_objects(cls)

  _publish_attrs = [
      PublishOnly('workflows'),
      'workflow_objects',
      ]

  _include_links = [
      #'workflow_objects',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Workflowable, cls).eager_query()
    return cls.eager_inclusions(query, Workflowable._include_links).options(
        orm.subqueryload('workflow_objects'))
