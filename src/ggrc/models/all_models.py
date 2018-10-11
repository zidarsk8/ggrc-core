# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""All GGRC model classes grouped together for convenience."""

import sys

from ggrc.access_control.list import AccessControlList
from ggrc.access_control.people import AccessControlPeople
from ggrc.access_control.role import AccessControlRole
from ggrc.data_platform.attribute_definitions import AttributeDefinitions
from ggrc.data_platform.attribute_templates import AttributeTemplates
from ggrc.data_platform.attribute_types import AttributeTypes
from ggrc.data_platform.attributes import Attributes
from ggrc.data_platform.namespaces import Namespaces
from ggrc.data_platform.object_templates import ObjectTemplates
from ggrc.data_platform.object_types import ObjectTypes
from ggrc.models import inflector
from ggrc.models.access_group import AccessGroup
from ggrc.models.assessment import Assessment
from ggrc.models.assessment_template import AssessmentTemplate
from ggrc.models.audit import Audit
from ggrc.models.automapping import Automapping
from ggrc.models.background_operation_type import BackgroundOperationType
from ggrc.models.background_task import BackgroundTask
from ggrc.models.background_operation import BackgroundOperation
from ggrc.models.categorization import Categorization
from ggrc.models.category import CategoryBase
from ggrc.models.comment import Comment
from ggrc.models.context import Context
from ggrc.models.control import Control
from ggrc.models.control import ControlAssertion
from ggrc.models.control import ControlCategory
from ggrc.models.custom_attribute_definition import CustomAttributeDefinition
from ggrc.models.custom_attribute_value import CustomAttributeValue
from ggrc.models.data_asset import DataAsset
from ggrc.models.directive import Contract
from ggrc.models.directive import Directive
from ggrc.models.directive import Policy
from ggrc.models.directive import Regulation
from ggrc.models.directive import Standard
from ggrc.models.document import Document
from ggrc.models.event import Event
from ggrc.models.evidence import Evidence
from ggrc.models.facility import Facility
from ggrc.models.import_export import ImportExport
from ggrc.models.issue import Issue
from ggrc.models.issuetracker_issue import IssuetrackerIssue
from ggrc.models.label import Label
from ggrc.models.maintenance import Maintenance
from ggrc.models.market import Market
from ggrc.models.metric import Metric
from ggrc.models.notification import Notification
from ggrc.models.notification import NotificationConfig
from ggrc.models.notification import NotificationHistory
from ggrc.models.notification import NotificationType
from ggrc.models.object_label import ObjectLabel
from ggrc.models.object_person import ObjectPerson
from ggrc.models.objective import Objective
from ggrc.models.option import Option
from ggrc.models.org_group import OrgGroup
from ggrc.models.person import Person
from ggrc.models.person_profile import PersonProfile
from ggrc.models.product import Product
from ggrc.models.product_group import ProductGroup
from ggrc.models.program import Program
from ggrc.models.project import Project
from ggrc.models.proposal import Proposal
from ggrc.models.relationship import Relationship
from ggrc.models.requirement import Requirement
from ggrc.models.revision import Revision
from ggrc.models.risk import Risk
from ggrc.models.risk_assessment import RiskAssessment
from ggrc.models.snapshot import Snapshot
from ggrc.models.system import Process
from ggrc.models.system import System
from ggrc.models.system import SystemOrProcess
from ggrc.models.technology_environment import TechnologyEnvironment
from ggrc.models.threat import Threat
from ggrc.models.vendor import Vendor
from ggrc.models.review import Review

all_models = [  # pylint: disable=invalid-name
    # data platform models
    AttributeDefinitions,
    AttributeTemplates,
    AttributeTypes,
    Attributes,
    Namespaces,
    ObjectTemplates,
    ObjectTypes,
    PersonProfile,

    # ggrc models
    AccessControlList,
    AccessControlPeople,
    AccessControlRole,
    AccessGroup,
    Assessment,
    AssessmentTemplate,
    Audit,
    Automapping,
    BackgroundTask,
    BackgroundOperation,
    BackgroundOperationType,
    Categorization,
    CategoryBase,
    Comment,
    Context,
    Contract,
    Control,
    ControlAssertion,
    ControlCategory,
    CustomAttributeDefinition,
    CustomAttributeValue,
    DataAsset,
    Directive,
    Document,
    Event,
    Evidence,
    Facility,
    ImportExport,
    Issue,
    IssuetrackerIssue,
    Label,
    Maintenance,
    Market,
    Metric,
    Notification,
    NotificationConfig,
    NotificationHistory,
    NotificationType,
    ObjectLabel,
    ObjectPerson,
    Objective,
    Option,
    OrgGroup,
    Person,
    Policy,
    Process,
    Product,
    ProductGroup,
    Program,
    Project,
    Proposal,
    Regulation,
    Relationship,
    Requirement,
    Review,
    Revision,
    Risk,
    RiskAssessment,
    Snapshot,
    Standard,
    System,
    SystemOrProcess,
    TechnologyEnvironment,
    Threat,
    Vendor,
]

__all__ = [m.__name__ for m in all_models]


def register_model(model):
  """Add model to all models.

  This function is used for adding models from different ggrc modules, such as
  ggrc_workflows, to the list of all models in the ggrc module.

  Args:
    model: sqlalchemy model to be added to the list of all models.
  """
  current_module = sys.modules[__name__]
  setattr(current_module, model.__name__, model)
  inflector.register_inflections(model._inflector)
  all_models.append(model)
  __all__.append(model.__name__)


def unregister_model(model):
  """Remove model from all models.

  This function removes the given model from the main ggrc module and the
  all_models list.

  Args:
    model: sqlalchemy model that should be removed from the ggrc module
  """
  current_module = sys.modules[__name__]
  delattr(current_module, model.__name__)
  inflector.unregister_inflector(model._inflector)
  if model in all_models:
    all_models.remove(model)
  if model.__name__ in __all__:
    __all__.remove(model.__name__)
