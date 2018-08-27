# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Risk Assessment module"""

from flask import Blueprint

from ggrc import settings
from ggrc.rbac import permissions


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
