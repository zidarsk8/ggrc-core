# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc.models.all_models import register_model

from .task import Task
from .task_entry import TaskEntry
from .task_group import TaskGroup
from .task_group_object import TaskGroupObject
from .task_group_task import TaskGroupTask
from .workflow import Workflow
from .workflow_object import WorkflowObject
from .workflow_person import WorkflowPerson
from .workflow_task import WorkflowTask
#from .cycle import Cycle
#from .cycle_task_group import CycleTaskGroup
#from .cycle_task_group_task import CycleTaskGroupTask
#from .cycle_task import CycleTask


register_model(Task)
register_model(TaskEntry)
register_model(TaskGroup)
register_model(TaskGroupObject)
register_model(TaskGroupTask)
register_model(Workflow)
register_model(WorkflowObject)
register_model(WorkflowPerson)
register_model(WorkflowTask)
#register_model(Cycle)
#register_model(CycleTask)
#register_model(CycleTaskGroup)
#register_model(CycleTaskGroupTask)

'''
from .risk_assessment import RiskAssessment
from .risk_assessment_mapping import RiskAssessmentMapping
from .risk_assessment_control_mapping import RiskAssessmentControlMapping
from .threat import Threat
from .vulnerability import Vulnerability


ggrc.models.all_models.Template = Template
ggrc.models.all_models.RiskAssessment = RiskAssessment
ggrc.models.all_models.RiskAssessmentMapping = RiskAssessmentMapping
ggrc.models.all_models.RiskAssessmentControlMapping = RiskAssessmentControlMapping
ggrc.models.all_models.Threat = Threat
ggrc.models.all_models.Vulnerability = Vulnerability

ggrc.models.all_models.all_models += [
    Template,
    RiskAssessment,
    RiskAssessmentMapping,
    RiskAssessmentControlMapping,
    Threat,
    Vulnerability,
    ]

ggrc.models.all_models.__all__ += [
    Template.__name__,
    RiskAssessment.__name__,
    RiskAssessmentMapping.__name__,
    RiskAssessmentControlMapping.__name__,
    Threat.__name__,
    Vulnerability.__name__,
    ]
'''
