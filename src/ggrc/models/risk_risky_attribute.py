# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import Base

class RiskRiskyAttribute(Base, db.Model):
  __tablename__ = 'risk_risky_attributes'

  risk_id = db.Column(db.Integer, db.ForeignKey('risks.id'), nullable=False)
  risky_attribute_id = db.Column(db.Integer, db.ForeignKey('risky_attributes.id'), nullable=False)

  __table_args__ = (
    db.UniqueConstraint('risk_id', 'risky_attribute_id'),
  )

