# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from flask import Blueprint
from sqlalchemy import orm

from ggrc import settings
from ggrc.models import all_models
from ggrc.models.reflection import PublishOnly
from ggrc.rbac import permissions
from ggrc.services.registry import service
from ggrc_basic_permissions.contributed_roles import RoleContributions
from ggrc_risk_assessments import models
from ggrc_risk_assessments import converters


# Initialize Flask Blueprint for extension
blueprint = Blueprint(
    'risk_assessments',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/ggrc_risk_assessments',
)


def get_public_config(current_user):
  """Expose additional permissions-dependent config to client.
    Specifically here, expose RISK_ASSESSMENT_URL values to ADMIN users.
  """
  public_config = {}
  if permissions.is_admin():
    if hasattr(settings, 'RISK_ASSESSMENT_URL'):
      public_config['RISK_ASSESSMENT_URL'] = settings.RISK_ASSESSMENT_URL
  return public_config


# Initialize service endpoints

def contributed_services():
  return [
      service('risk_assessments', models.RiskAssessment),
  ]


def contributed_object_views():
  return []


# Mixin to mix risk_assessments into Program
class MixRiskAssessmentsIntoProgram(object):

  @classmethod
  def mix_risk_assessments_into_program(cls):
    # cls.risk_assessments = db.relationship(
    pass  # 'RiskAssessment', cascade='all, delete-orphan')

  _publish_attrs = [
      PublishOnly('risk_assessments')
  ]

  _include_links = []

  @classmethod
  def eager_query(cls):

    query = super(MixRiskAssessmentsIntoProgram, cls).eager_query()
    return cls.eager_inclusions(
        query, MixRiskAssessmentsIntoProgram._include_links).options(
        orm.subqueryload('risk_assessments'))

# Mix RiskAssessments into Program

program_type = getattr(all_models, "Program")
program_type.__bases__ = (MixRiskAssessmentsIntoProgram,) \
    + program_type.__bases__
program_type.mix_risk_assessments_into_program()


class RiskAssessmentRoleContributions(RoleContributions):
  contributions = {
      'ProgramOwner': {
          'create': ['RiskAssessment', 'Document'],
          'read': ['RiskAssessment', 'Document'],
          'update': ['RiskAssessment', 'Document'],
          'delete': ['RiskAssessment', 'Document'],
      },
      'ProgramEditor': {
          'read': ['RiskAssessment', 'Document']
      },
      'ProgramReader': {
          'read': ['RiskAssessment', 'Document']
      }
  }

ROLE_CONTRIBUTIONS = RiskAssessmentRoleContributions()
contributed_importables = converters.IMPORTABLE
