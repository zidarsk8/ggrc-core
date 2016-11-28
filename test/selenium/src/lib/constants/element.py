# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module containing element labels or properties e.g. date formatting"""
# pylint: disable=too-few-public-methods

from lib.constants import objects


# size of the header in px
SIZE_HEADER = 50


class LandingPage(object):
  BUTTON_LOGIN = "Login"
  PROGRAM_INFO_TAB = "Program Info"


class PageHeader(object):
  # dropdown toggle
  PROPLE_LIST_WIDGET = "Admin Dashboard"


class Lhn(object):
  """Labels in the LHN menu"""
  class __metaclass__(type):
    def __init__(self, *args):
      for object_ in objects.ALL_PLURAL:
        setattr(self, object_, object_.lower())

      self.DIRECTIVES_MEMBERS = (
          self.REGULATIONS,
          self.POLICIES,
          self.STANDARDS,
          self.CONTRACTS,
          self.CLAUSES,
          self.SECTIONS)
      self.CONTROLS_OR_OBJECTIVES_MEMBERS = (
          self.CONTROLS,
          self.OBJECTIVES)
      self.PEOPLE_OR_GROUPS_MEMBERS = (
          self.PEOPLE,
          self.ORG_GROUPS,
          self.VENDORS,
          self.ACCESS_GROUPS)
      self.ASSETS_OR_BUSINESS_MEMBERS = (
          self.SYSTEMS,
          self.PROCESSES,
          self.DATA_ASSETS,
          self.PRODUCTS,
          self.PROJECTS,
          self.FACILITIES,
          self.MARKETS)
      self.RISKS_OR_THREATS_MEMBERS = (
          self.RISKS,
          self.THREATS)

  CONTROLS_OR_OBJECTIVES = "controls_or_objectives"
  PEOPLE_OR_GROUPS = "people_or_groups"
  ASSETS_OR_BUSINESS = "assets_or_business"
  RISKS_OR_THREATS = "risks_or_threats"


class ModalLhnCreateProgram(object):
  """Modal for creating a Program."""
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

  class __metaclass__(type):
    def __init__(self, *args):
      for object_ in objects.ALL_PLURAL:
        setattr(self, object_, object_.lower())


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
  """Role scopes for Roles widget at Admin dashboard"""
  _SYS_SCOPE = "SYSTEM"
  _PRG_SCOPE = "PRIVATE PROGRAM"
  _WF_SCOPE = "WORKFLOW"

  ROLE_SCOPE_ADMINISTRATOR = ("Administrator", "ADMIN")
  ROLE_SCOPE_CREATOR = ("Creator", _SYS_SCOPE)
  ROLE_SCOPE_EDITOR = ("Editor", _SYS_SCOPE)
  ROLE_SCOPE_READER = ("Reader", _SYS_SCOPE)
  ROLE_SCOPE_PROGRAM_EDITOR = ("Program Editor", _PRG_SCOPE)
  ROLE_SCOPE_PROGRAM_MANAGER = ("Program Manager", _PRG_SCOPE)
  ROLE_SCOPE_PROGRAM_READER = ("Program Reader", _PRG_SCOPE)
  ROLE_SCOPE_WORKFLOW_MEMBER = ("Workflow Member", _WF_SCOPE)
  ROLE_SCOPE_WORKFLOW_MANAGER = ("Workflow Manager", _WF_SCOPE)
  ROLE_SCOPES_LIST = [ROLE_SCOPE_ADMINISTRATOR,
                      ROLE_SCOPE_CREATOR,
                      ROLE_SCOPE_EDITOR,
                      ROLE_SCOPE_PROGRAM_EDITOR,
                      ROLE_SCOPE_PROGRAM_MANAGER,
                      ROLE_SCOPE_PROGRAM_READER,
                      ROLE_SCOPE_READER,
                      ROLE_SCOPE_WORKFLOW_MEMBER,
                      ROLE_SCOPE_WORKFLOW_MANAGER]
  ROLE_SCOPES_DICT = dict(ROLE_SCOPES_LIST)


class AdminEventsWidget(object):
  """Label and regular expression for Event widget at Admin dashboard"""
  TREE_VIEW_HEADER = "Events"
  TREE_VIEW_ROW_REGEXP = r"^.+\s(by.+)\son\s" + \
      r"(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\s[A,P]M)"


class AttributesTypes(object):
  """Possible types of Custom Attributes."""
  TEXT = "Text"
  RICH_TEXT = "Rich Text"
  DATE = "Date"
  CHECKBOX = "Checkbox"
  DROPDOWN = "Dropdown"
  PERSON = "Map:Person"

  ALL_TYPES = (TEXT, RICH_TEXT, DATE, CHECKBOX, DROPDOWN, PERSON)
