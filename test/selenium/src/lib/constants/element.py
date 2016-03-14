# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Module containing element labels or properties e.g. date formatting"""


class LandingPage(object):
  BUTTON_LOGIN = "Login"
  PROGRAM_INFO_TAB = "Program Info"


class PageHeader(object):
  # dropdown toggle
  PROPLE_LIST_WIDGET = "Admin Dashboard"


class Lhn(object):
  """Labels in the LHN menu"""
  PROGRAMS = "programs"
  WORKFLOWS = "workflows"
  AUDITS = "audits"
  ASSESSMENTS = "assessments"
  REQUESTS = "requests"
  ISSUES = "issues"

  DIRECTIVES = "directives"
  REGULATIONS = "regulations"
  POLICIES = "policies"
  STANDARDS = "standards"
  CONTRACTS = "contracts"
  CLAUSES = "clauses"
  SECTIONS = "sections"

  CONTROLS_OR_OBJECTIVES = "controls_or_objectives"
  CONTROLS = "controls"
  OBJECTIVES = "objectives"

  PEOPLE_OR_GROUPS = "people_or_groups"
  PEOPLE = "people"
  ORG_GROUPS = "org_groups"
  VENDORS = "vendors"
  ACCESS_GROUPS = "access_groups"

  ASSETS_OR_BUSINESS = "assets_or_business"
  SYSTEMS = "systems"
  PROCESSES = "processes"
  DATA_ASSETS = "data_assets"
  PRODUCTS = "products"
  PROJECTS = "projects"
  FACILITIES = "facilities"
  MARKETS = "markets"

  RISKS_OR_THREATS = "risks_or_threats"
  RISKS = "risks"
  THREATS = "threats"

  DIRECTIVES_MEMBERS = (
      REGULATIONS,
      POLICIES,
      STANDARDS,
      CONTRACTS,
      CLAUSES,
      SECTIONS)
  CONTROLS_OR_OBJECTIVES_MEMBERS = (
    CONTROLS,
    OBJECTIVES)
  PEOPLE_OR_GROUPS_MEMBERS = (
    PEOPLE,
    ORG_GROUPS,
    VENDORS,
    ACCESS_GROUPS)
  ASSETS_OR_BUSINESS_MEMBERS = (
    SYSTEMS,
    PROCESSES,
    DATA_ASSETS,
    PRODUCTS,
    PROJECTS,
    FACILITIES,
    MARKETS)
  RISKS_OR_THREATS_MEMBERS = (
    RISKS,
    THREATS)


class ModalLhnCreateProgram(object):
  # create new program
  DATE_FORMATTING = "%d/%m/%Y"
  OBJECT_REVIEW = "Object Review"
  PRIVATE_PROGRAM = "Private Program"
  DESCRIPTION = "Description"
  NOTES = "Notes"
  MANAGER = "Manager"
  PROGRAM_URL = "Program URL"
  STATE = "State"
  PRIMARY_CONTACT = "Primary Contact"
  SECONDARY_CONTACT = "Secondary Contact"
  REFERENCE_URL = "Reference URL"
  CODE = "Code"
  EFFECTIVE_DATE = "Effective Date"
  STOP_DATE = "Stop Date"


class WidgetBar(object):
  """Labels specific for a generic widget bar"""

  # identifier for the object's info page
  INFO = "Info"

  PROGRAMS = "programs"
  WORKFLOWS = "workflows"
  AUDITS = "audits"
  ASSESSMENTS = "assessments"
  REQUESTS = "requests"
  ISSUES = "issues"
  DIRECTIVES = "directives"
  REGULATIONS = "regulations"
  POLICIES = "policies"
  STANDARDS = "standards"
  CONTRACTS = "contracts"
  CLAUSES = "clauses"
  SECTIONS = "sections"
  CONTROLS = "controls"
  OBJECTIVES = "objectives"
  PEOPLE = "people"
  ORG_GROUPS = "org_groups"
  VENDORS = "vendors"
  ACCESS_GROUPS = "access_groups"
  SYSTEMS = "systems"
  PROCESSES = "processes"
  DATA_ASSETS = "data_assets"
  PRODUCTS = "products"
  PROJECTS = "projects"
  FACILITIES = "facilities"
  MARKETS = "markets"
  RISKS = "risks"
  THREATS = "threats"


class WidgetProgramInfo(object):
  """Labels specific to program info widget"""

  SUBMIT_FOR_REVIEW = "Submit For Review"

  # state in lhn_modal create new page
  DRAFT = "Draft"
  FINAL = "Final"
  EFFECTIVE = "Effective"
  INEFFECTIVE = "Ineffective"
  LAUNCHED = "Launched"
  NOT_LAUNCHED = "Not Launched"
  IN_SCOPE = "In Scope"
  NOT_IN_SCOPE = "Not in Scope"
  DEPRECATED = "Deprecated"

  # button settings dropdown elements
  EDIT_PROGRAM = "Edit Program"
  GET_PERMALINK = "Get permalink"
  DELETE = "Delete"
  BUTTON_SETTINGS_DROPDOWN_ITEMS = [EDIT_PROGRAM, GET_PERMALINK, DELETE]

  ALERT_LINK_COPIED = "Link has been copied to your clipboard."


class AdminRolesWidget(object):
  EDITOR = "Editor"
  GRC_ADMIN = "gGRC Admin"
  PROGRAM_EDITOR = "ProgramEditor"
  PROGRAM_OWNER = "ProgramOwner"
  PROGRAM_READER = "ProgramReader"
  READER = "Reader"
  WORKFLOW_MEMEMBER = "WorkflowMember"
  WORKFLOW_OWNER = "WorkflowOwner"

  SCOPE_SYSTEM = "SYSTEM"
  SCOPE_ADMIN = "ADMIN"
  SCOPE_PRIVATE_PROGRAM = "PRIVATE PROGRAM"
  SCOPE_WORKFLOW = "WORKFLOW"
