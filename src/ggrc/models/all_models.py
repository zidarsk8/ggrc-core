# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""All gGRC model classes grouped together for convenience."""

# TODO: Implement with Authentication
# from .account import Account
from .audit import Audit
from .audit_object import AuditObject
from .categorization import Categorization
from .category import CategoryBase
from .context import Context
from .control import Control, ControlCategory, ControlAssertion
from .control_assessment import ControlAssessment
from .custom_attribute_definition import CustomAttributeDefinition
from .custom_attribute_value import CustomAttributeValue
from .data_asset import DataAsset
from .directive import Directive, Regulation, Policy, Contract, Standard
from .document import Document
from .facility import Facility
from .help import Help
from .market import Market
from .object_document import ObjectDocument
from .object_owner import ObjectOwner
from .object_person import ObjectPerson
from .object_type import ObjectType
from .objective import Objective
from .option import Option
from .org_group import OrgGroup
from .vendor import Vendor
from .person import Person
from .product import Product
from .program import Program
from .project import Project
from .relationship import Relationship, RelationshipType
from .request import Request
from .response import (
    Response, DocumentationResponse, InterviewResponse,
    PopulationSampleResponse
)
from .meeting import Meeting
from .background_task import BackgroundTask
from .notification import NotificationConfig, NotificationType, Notification
from .issue import Issue

# TODO: This isn't currently used
# from .relationship_type import RelationshipType
from .section import Section
from .clause import Clause
from .system import SystemOrProcess, System, Process

from .revision import Revision
from .event import Event
all_models = [
    Audit,
    AuditObject,
    Categorization,
    CategoryBase,
    ControlCategory,
    ControlAssertion,
    Context,
    Control,
    ControlAssessment,
    CustomAttributeDefinition,
    CustomAttributeValue,
    DataAsset,
    Directive,
    Contract,
    Policy,
    Regulation,
    Standard,
    Document,
    Facility,
    Help,
    Market,
    Meeting,
    Objective,
    ObjectDocument,
    ObjectOwner,
    ObjectPerson,
    ObjectType,
    Option,
    OrgGroup,
    Vendor,
    Person,
    Product,
    Program,
    Project,
    Relationship,
    RelationshipType,
    Request,
    Response,
    DocumentationResponse,
    InterviewResponse,
    PopulationSampleResponse,
    Section,
    Clause,
    SystemOrProcess,
    System,
    Process,
    Revision,
    Event,
    BackgroundTask,
    NotificationConfig,
    NotificationType,
    Notification,
    Issue
]

__all__ = [model.__name__ for model in all_models]


def register_model(model):
  import ggrc.models.all_models
  setattr(ggrc.models.all_models, model.__name__, model)
  model._inflector
  all_models.append(model)
  __all__.append(model.__name__)


def unregister_model(model):
  import ggrc.models.all_models
  import ggrc.models.inflector
  delattr(ggrc.models.all_models, model.__name__)
  ggrc.models.inflector.unregister_inflector(model._inflector)
  if model in all_models:
    all_models.remove(model)
  if model.__name__ in __all__:
    __all__.remove(model.__name__)
