# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

"""All gGRC model classes grouped together for convenience."""

# TODO: Implement with Authentication
#from .account import Account
from .categorization import Categorization
from .category import Category
from .context import Context
from .control import Control
from .control_assessment import ControlAssessment
from .control_control import ControlControl
from .control_risk import ControlRisk
from .control_section import ControlSection
from .cycle import Cycle
from .data_asset import DataAsset
from .directive import Directive
from .document import Document
from .facility import Facility
from .help import Help
from .market import Market
from .meeting import Meeting
from .object_control import ObjectControl
from .object_document import ObjectDocument
from .object_objective import ObjectObjective
from .object_person import ObjectPerson
from .object_section import ObjectSection
from .objective import Objective
from .objective_control import ObjectiveControl
from .option import Option
from .org_group import OrgGroup
from .pbc_list import PbcList
from .person import Person
from .population_sample import PopulationSample
from .product import Product
from .program import Program
from .program_directive import ProgramDirective
from .project import Project
from .relationship import Relationship, RelationshipType

#TODO: This isn't currently used
#from .relationship_type import RelationshipType
from .request import Request
from .response import Response
from .risk import Risk
from .risk_risky_attribute import RiskRiskyAttribute
from .risky_attribute import RiskyAttribute
from .section import Section
from .section_objective import SectionObjective
from .system import System
from .system_control import SystemControl

# TODO: Is this used?
#from .system_section import SystemSection
from .system_system import SystemSystem

# TODO: Include?
from .log_event import LogEvent

from .revision import Revision
from .event import Event
all_models = [
  Categorization,
  Category,
  Context,
  Control,
  ControlAssessment,
  ControlControl,
  ControlRisk,
  ControlSection,
  Cycle,
  DataAsset,
  Directive,
  Document,
  Facility,
  Help,
  Market,
  Meeting,
  Objective,
  ObjectiveControl,
  ObjectControl,
  ObjectDocument,
  ObjectObjective,
  ObjectPerson,
  ObjectSection,
  Option,
  OrgGroup,
  PbcList,
  Person,
  PopulationSample,
  Product,
  Program,
  ProgramDirective,
  Project,
  Relationship,
  RelationshipType,
  Request,
  Response,
  Risk,
  RiskRiskyAttribute,
  RiskyAttribute,
  Section,
  SectionObjective,
  System,
  SystemControl,
  SystemSystem,
  LogEvent,
  Revision,
  Event,
  ]

__all__ = [model.__name__ for model in all_models]
