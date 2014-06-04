# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from flask import Blueprint
from ggrc import settings
#from ggrc.app import app
#from ggrc.rbac import permissions
from ggrc.services.registry import service
from ggrc.views.registry import object_view
import ggrc_workflows.models as models


# Initialize Flask Blueprint for extension
blueprint = Blueprint(
  'ggrc_workflows',
  __name__,
  template_folder='templates',
  static_folder='static',
  static_url_path='/static/ggrc_workflows',
)


from ggrc.models import all_models

_workflow_object_types = [
    "Program",
    "Regulation", "Standard", "Policy", "Contract",
    "Objective", "Control", "Section", "Clause",
    "System", "Process",
    "DataAsset", "Facility", "Market", "Product", "Project"
    ]

for type_ in _workflow_object_types:
  model = getattr(all_models, type_)
  model.__bases__ = (models.workflow_object.Workflowable,) + model.__bases__
  model.late_init_workflowable()


def get_public_config(current_user):
  """Expose additional permissions-dependent config to client.
  """
  return {}
#  public_config = {}
#  if permissions.is_admin():
#    if hasattr(settings, 'RISK_ASSESSMENT_URL'):
#      public_config['RISK_ASSESSMENT_URL'] = settings.RISK_ASSESSMENT_URL
#  return public_config


# Initialize service endpoints

def contributed_services():
  return [
      service('workflows', models.Workflow),
      service('workflow_objects', models.WorkflowObject),
      service('workflow_people', models.WorkflowPerson),
      service('tasks', models.Task),
      service('workflow_tasks', models.WorkflowTask),
      service('task_groups', models.TaskGroup),
      service('task_group_tasks', models.TaskGroupTask),
      service('task_group_objects', models.TaskGroupObject),
      service('task_entries', models.TaskEntry),

      #service('cycles', models.Cycle),
      ]


def contributed_object_views():
  from . import models

  return [
      object_view(models.Workflow),
      object_view(models.Task),
      ]
