# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: silas@reciprocitylabs.com
# Maintained By: silas@reciprocitylabs.com

from datetime import date, timedelta
import calendar
from flask import Blueprint
from sqlalchemy import inspect

from ggrc import settings, db
from ggrc.login import get_current_user
#from ggrc.rbac import permissions
from ggrc.services.registry import service
from ggrc.views.registry import object_view
import ggrc_risk_assessment_v2.models as models


# Initialize signal handler for status changes
from blinker import Namespace
signals = Namespace()
status_change = signals.signal(
  'Status Changed',
  """
  This is used to signal any listeners of any changes in model object status
  attribute
  """)

# Initialize Flask Blueprint for extension
blueprint = Blueprint(
  'ggrc_risk_assessment_v2',
  __name__,
  template_folder='templates',
  static_folder='static',
  static_url_path='/static/ggrc_risk_assessment_v2',
)


from ggrc.models import all_models

_risk_object_types = [
    "Program",
    "Regulation", "Standard", "Policy", "Contract",
    "Objective", "Control", "Section", "Clause",
    "System", "Process",
    "DataAsset", "Facility", "Market", "Product", "Project"
    ]

for type_ in _risk_object_types:
  model = getattr(all_models, type_)
  model.__bases__ = (
    models.risk_object.Riskable,
    ) + model.__bases__
  model.late_init_riskable()


def get_public_config(current_user):
  """Expose additional permissions-dependent config to client.
  """
  return {}


def contributed_services():
  return [
      service('risks', models.Risk),
      service('risk_objects', models.RiskObject),
      ]


def contributed_object_views():
  from . import models

  return [
      object_view(models.Risk),
      ]

# Initialize non-RESTful views
import ggrc_risk_assessment_v2.views

def init_extra_views(app):
  ggrc_risk_assessment_v2.views.init_extra_views(app)
