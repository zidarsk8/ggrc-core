
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base

class SystemControl(Base, db.Model):
  __tablename__ = 'system_controls'

  system_id = db.Column(db.Integer, db.ForeignKey('systems.id'), nullable=False)
  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'), nullable=False)
  state = db.Column(db.Integer, default=1, nullable=False)
  cycle_id = db.Column(db.Integer, db.ForeignKey('cycles.id'))
  cycle = db.relationship('Cycle', uselist=False)

  __table_args__ = (
    db.UniqueConstraint('system_id', 'control_id'),
  )

  _publish_attrs = [
      'system',
      'control',
      'state',
      'cycle',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(SystemControl, cls).eager_query()
    return query.options(
        orm.joinedload('cycle'),
        orm.subqueryload('system'),
        orm.subqueryload('control'))

  def _display_name(self):
    return self.control.display_name + '<->' + self.system.display_name
