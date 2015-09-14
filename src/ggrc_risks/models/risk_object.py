# Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
# Unauthorized use, copying, distribution, displaying, or public performance
# of this file, via any medium, is strictly prohibited. All information
# contained herein is proprietary and confidential and may not be shared
# with any third party without the express written consent of Reciprocity, Inc.
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com
#
# Borrows heavily from ggrc_workflows.models.workflow_object

from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from ggrc.models.mixins import deferred, Mapping
from ggrc.models.reflection import PublishOnly


class RiskObject(Mapping, db.Model):
  __tablename__ = 'risk_objects'

  risk_id = db.Column(
      db.Integer, db.ForeignKey('risks.id'), nullable=False)
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
        db.UniqueConstraint('risk_id', 'object_id', 'object_type'),
        db.Index('ix_risk_id', 'risk_id'),
        )

  _publish_attrs = [
      'risk',
      'object',
      ]
  _sanitize_html = [
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(RiskObject, cls).eager_query()
    return query.options(
        orm.subqueryload('risk'))

  def _display_name(self):
    return self.object.display_name + '<->' + self.risk.display_name


class Riskable(object):
  @classmethod
  def late_init_riskable(cls):
    def make_risk_objects(cls):
      cls.risks = association_proxy(
          'risk_objects', 'risk',
          creator=lambda risk: RiskObject(
              risk=risk,
              object_type=cls.__name__,
              )
          )
      joinstr = 'and_(foreign(RiskObject.object_id) == {type}.id, '\
                     'foreign(RiskObject.object_type) == "{type}")'
      joinstr = joinstr.format(type=cls.__name__)
      return db.relationship(
          'RiskObject',
          primaryjoin=joinstr,
          backref='{0}_object'.format(cls.__name__),
          cascade='all, delete-orphan',
          )
    cls.risk_objects = make_risk_objects(cls)

  _publish_attrs = [
      PublishOnly('risks'),
      'risk_objects',
      ]

  _include_links = [
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Riskable, cls).eager_query()
    return cls.eager_inclusions(query, Riskable._include_links).options(
        orm.subqueryload('risk_objects'))

