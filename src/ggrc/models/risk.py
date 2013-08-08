# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .associationproxy import association_proxy
from .control import ControlCategorized
from .mixins import deferred, BusinessObject, Timeboxed
from .object_document import Documentable
from .object_person import Personable
from .reflection import PublishOnly

class Risk(
    Documentable, Personable, Timeboxed, ControlCategorized, BusinessObject,
    db.Model):
  __tablename__ = 'risks'

  kind = deferred(db.Column(db.String), 'Risk')
  likelihood = deferred(db.Column(db.Text), 'Risk')
  threat_vector = deferred(db.Column(db.Text), 'Risk')
  trigger = deferred(db.Column(db.Text), 'Risk')
  preconditions = deferred(db.Column(db.Text), 'Risk')

  likelihood_rating = deferred(db.Column(db.Integer), 'Risk')
  financial_impact_rating = deferred(db.Column(db.Integer), 'Risk')
  reputational_impact_rating = deferred(db.Column(db.Integer), 'Risk')
  operational_impact_rating = deferred(db.Column(db.Integer), 'Risk')

  inherent_risk = deferred(db.Column(db.Text), 'Risk')
  risk_mitigation = deferred(db.Column(db.Text), 'Risk')
  residual_risk = deferred(db.Column(db.Text), 'Risk')
  impact = deferred(db.Column(db.Text), 'Risk')

  control_risks = db.relationship('ControlRisk', backref='risk', cascade='all, delete-orphan')
  controls = association_proxy('control_risks', 'control', 'ControlRisk')
  risk_risky_attributes = db.relationship(
      'RiskRiskyAttribute', backref='risk', cascade='all, delete-orphan')
  risky_attributes = association_proxy(
      'risk_risky_attributes', 'risky_attribute', 'RiskRiskyAttribute')

  _publish_attrs = [
      'categories',
      'controls',
      'financial_impact_rating',
      'inherent_risk',
      'impact',
      'kind',
      'likelihood',
      'likelihood_rating',
      'operational_impact_rating',
      'preconditions',
      'reputational_impact_rating',
      'residual_risk',
      'risky_attributes',
      'threat_vector',
      'trigger',
      PublishOnly('control_risks'),
      PublishOnly('risk_risky_attributes'),
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Risk, cls).eager_query()
    return query.options(
        orm.subqueryload_all('control_risks.control'),
        # FIXME: make eager-loading work for categorizations
        #orm.subqueryload_all('categorizations.categories'),
        orm.subqueryload_all('risk_risky_attributes.risky_attribute'))
