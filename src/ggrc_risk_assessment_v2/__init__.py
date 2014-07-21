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


def get_public_config(current_user):
  """Expose additional permissions-dependent config to client.
  """
  return {}


def contributed_services():
  return [
      service('risks', models.Risk),
      ]


def contributed_object_views():
  from . import models

  return [
      object_view(models.Risk),
      ]
