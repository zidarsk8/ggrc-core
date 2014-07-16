# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from flask import Blueprint
from ggrc import settings
from ggrc.app import app
from ggrc.rbac import permissions
from ggrc.services.registry import service
from ggrc.views.registry import object_view
import ggrc_risk_assessments.models as models


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
  from . import models

  return [
      ]
