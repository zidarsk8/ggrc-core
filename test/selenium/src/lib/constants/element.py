# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Elements' labels and properties for objects."""
# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name

from collections import namedtuple

from lib.constants import objects, roles


class Lhn(object):
  """Elements' labels and properties for LHN menu."""
  class __metaclass__(type):
    def __init__(cls, *args):
      for object_ in objects.ALL_PLURAL:
        setattr(cls, object_, object_.lower())
      cls.DIRECTIVES_MEMBERS = (
          cls.REGULATIONS,
          cls.POLICIES,
          cls.STANDARDS,
          cls.CONTRACTS,
          cls.CLAUSES,
          cls.SECTIONS)
      cls.CONTROLS_OR_OBJECTIVES_MEMBERS = (
          cls.CONTROLS,
          cls.OBJECTIVES)
      cls.PEOPLE_OR_GROUPS_MEMBERS = (
          cls.PEOPLE,
          cls.ORG_GROUPS,
          cls.VENDORS,
          cls.ACCESS_GROUPS)
      cls.ASSETS_OR_BUSINESS_MEMBERS = (
          cls.SYSTEMS,
          cls.PROCESSES,
          cls.DATA_ASSETS,
          cls.PRODUCTS,
          cls.PROJECTS,
          cls.FACILITIES,
          cls.MARKETS)
      cls.RISKS_OR_THREATS_MEMBERS = (
          cls.RISKS,
          cls.THREATS)
  CONTROLS_OR_OBJECTIVES = "controls_or_objectives"
  PEOPLE_OR_GROUPS = "people_or_groups"
  ASSETS_OR_BUSINESS = "assets_or_business"
  RISKS_OR_THREATS = "risks_or_threats"
  MY_OBJS = "My objects"
  ALL_OBJS = "All objects"


class WidgetBar(object):
  """Elements' labels and properties for Generic widget bar."""

  class __metaclass__(type):
    def __init__(cls, *args):
      for object_ in objects.ALL_PLURAL:
        setattr(cls, object_, object_.lower())


class AdminWidgetRoles(object):
  """Elements' labels (role scopes) and properties for Roles widget
 at Admin Dashboard.
 """
  _ADMIN_SCOPE = roles.ADMIN.upper()
  _SYS_SCOPE = roles.SYSTEM.upper()
  _PRG_SCOPE = roles.PRIVATE_PROGRAM.upper()
  _WF_SCOPE = roles.WORKFLOW.upper()
  # role scopes
  ROLE_SCOPE_ADMINISTRATOR = (roles.ADMINISTRATOR, _ADMIN_SCOPE)
  ROLE_SCOPE_CREATOR = (roles.CREATOR, _SYS_SCOPE)
  ROLE_SCOPE_EDITOR = (roles.EDITOR, _SYS_SCOPE)
  ROLE_SCOPE_READER = (roles.READER, _SYS_SCOPE)
  ROLE_SCOPE_PROGRAM_EDITOR = (roles.PROGRAM_EDITOR, _PRG_SCOPE)
  ROLE_SCOPE_PROGRAM_MANAGER = (roles.PROGRAM_MANAGER, _PRG_SCOPE)
  ROLE_SCOPE_PROGRAM_READER = (roles.PROGRAM_READER, _PRG_SCOPE)
  ROLE_SCOPE_WORKFLOW_MEMBER = (roles.WORKFLOW_MEMBER, _WF_SCOPE)
  ROLE_SCOPE_WORKFLOW_MANAGER = (roles.WORKFLOW_MANAGER, _WF_SCOPE)
  ROLE_SCOPES_LIST = [
      ROLE_SCOPE_ADMINISTRATOR,
      ROLE_SCOPE_CREATOR,
      ROLE_SCOPE_EDITOR,
      ROLE_SCOPE_READER,
  ]
  ROLE_SCOPES_DICT = dict(ROLE_SCOPES_LIST)


class AdminWidgetEvents(object):
  """Elements' labels and properties (regular expression) for Event widget
 at Admin Dashboard.
 """
  WIDGET_HEADER = "Events"
  TREE_VIEW_ROW_REGEXP = r"^.+\s(by.+)\son\s" + \
      r"(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\s[A,P]M)"


class AdminWidgetCustomAttributes(object):
  """Elements' labels (custom attributes scopes) for Custom Attributes
 widget at Admin Dashboard.
 """
  WIDGET_HEADER = "Custom Attributes"
  # possible types of custom attributes
  TEXT = "Text"
  RICH_TEXT = "Rich Text"
  DATE = "Date"
  CHECKBOX = "Checkbox"
  DROPDOWN = "Dropdown"
  PERSON = "Map:Person"
  ALL_CA_TYPES = (TEXT, RICH_TEXT, DATE, CHECKBOX, DROPDOWN, PERSON)


class Base(object):
  """Base elements' labels and properties for objects."""
  WIDGET_INFO_HEADER_FORMAT = "{} Info"
  TYPE = "Type"
  STATE = "State"
  EFFECTIVE_DATE = "Effective Date"
  STOP_DATE = "Stop Date"


class Common(object):
  """Common elements' labels and properties for objects."""
  TITLE = "Title"
  DESCRIPTION = "Description"
  CODE = "Code"
  STATE = Base.STATE
  # fictional elements (need to convert UI attrs to Entities attrs)
  CAS = "CAs"
  MODIFIED_BY = "Last updated by"
  CREATED_AT = "Created date"
  UPDATED_AT = "Updated at"
  # roles
  OBJECT_ADMINS = "Object Admins"
  PRIMARY_CONTACTS = roles.PRIMARY_CONTACTS
  SECONDARY_CONTACTS = roles.SECONDARY_CONTACTS
  OTHERS = "Others"


class CommonModalCreate(object):
  """Common elements' labels and properties for Modal to Create object.
 """
  HIDE_ALL_OPT_FIELDS = "Hide all optional fields"
  SHOW_ALL_OPT_FIELDS = "Show all optional fields"
  SAVE_AND_CLOSE = "Save & Close"


class CommonModalSetVisibleFields(Common):
  """Common elements' labels and properties for Modal widow that Select visible
 fields for Tree View.
 """
  MODAL_HEADER_FORMAT = "Set visible fields for {}"
  TITLE = Common.TITLE
  CODE = Common.CODE
  STATE = Base.STATE
  LAST_UPDATED = "Last Updated Date"
  LAST_UPDATED_BY = "Last Updated By"
  SET_FIELDS = "Set Fields"


class TransformationSetVisibleFields(CommonModalSetVisibleFields):
  """To transformation elements' labels and properties for Modal to Set
 visible fields for object as Tree View headers.
 """
  ADMIN = roles.ADMIN
  PRIMARY_CONTACTS = roles.PRIMARY_CONTACTS
  SECONDARY_CONTACTS = roles.SECONDARY_CONTACTS
  VERIFIED = "Verified"
  STATUS = "Status"
  AUDIT_CAPTAINS = "Audit Captains"
  MANAGER = "Manager"
  MAPPED_OBJECTS = "Mapped Objects"
  REVIEW_STATE = "Review State"
  CREATORS = roles.CREATORS
  ASSIGNEES = roles.ASSIGNEES
  VERIFIERS = roles.VERIFIERS


class CommonProgram(Common):
  """Common elements' labels and properties for Programs objects."""
  # pylint: disable=too-many-instance-attributes
  PROGRAM = objects.get_normal_form(objects.get_singular(objects.PROGRAMS))
  TITLE = Common.TITLE
  MANAGER = "Manager"
  NOTES = "Notes"
  EFFECTIVE_DATE = Base.EFFECTIVE_DATE
  STATE = Base.STATE
  PROGRAM_MANAGERS = roles.PROGRAM_MANAGER + "s"


class CommonAudit(Common):
  """Common elements' labels and properties for Audits objects."""
  # pylint: disable=too-many-instance-attributes
  AUDIT = objects.get_normal_form(objects.get_singular(objects.AUDITS))
  STATUS = "Status"
  PLANNED_START_DATE = "Planned Start Date"
  PLANNED_END_DATE = "Planned End Date"
  PLANNED_REPORT_PERIOD = "Report Period"
  AUDIT_FIRM = " Audit Firm"
  ADD_AUDITOR = "+ Add Auditor"
  AUDIT_FOLDER = "Audit Folder"
  ASSIGN_FOLDER = "Assign folder"
  # roles
  AUDIT_CAPTAIN = "Audit Captain"
  AUDIT_CAPTAINS = AUDIT_CAPTAIN + "s"
  AUDITORS = roles.AUDITORS
  PRINCIPAL_ASSIGNEES = roles.PRINCIPAL_ASSIGNEES
  SECONDARY_ASSIGNEES = roles.SECONDARY_ASSIGNEES


class CommonControl(Common):
  """Common elements' labels and properties for Controls objects."""
  CONTROL = objects.get_normal_form(objects.get_singular(objects.CONTROLS))
  STATE = Base.STATE
  ADMIN = roles.ADMIN
  PRIMARY_CONTACTS = roles.PRIMARY_CONTACTS
  CREATORS = roles.CREATORS
  MAPPED_OBJECTS = TransformationSetVisibleFields.MAPPED_OBJECTS


class CommonObjective(Common):
  """Common elements' labels and properties for Objective objects."""
  OBJECTIVE = objects.get_normal_form(objects.get_singular(objects.OBJECTIVES))
  STATE = Base.STATE
  ADMIN = roles.ADMIN
  PRIMARY_CONTACTS = roles.PRIMARY_CONTACTS
  CREATORS = roles.CREATORS
  MAPPED_OBJECTS = TransformationSetVisibleFields.MAPPED_OBJECTS


class CommonAssessment(Common):
  """Common elements' labels and properties for Assessments objects."""
  ASMT = objects.get_normal_form(objects.get_singular(objects.ASSESSMENTS))
  STATE = Base.STATE
  CREATORS = roles.CREATORS
  COMMENTS = "Comments"
  ASSIGNEES = roles.ASSIGNEES
  VERIFIERS = roles.VERIFIERS
  MAPPED_OBJECTS = TransformationSetVisibleFields.MAPPED_OBJECTS
  ASMT_TYPE = "Assessment Type"
  VERIFIED = TransformationSetVisibleFields.VERIFIED


class CommonAssessmentTemplate(Common):
  """Common elements' labels and properties for Assessment Templates objects.
 """
  ASMT_TMPL = objects.get_normal_form(
      objects.get_singular(objects.ASSESSMENT_TEMPLATES))


class CommonIssue(Common):
  """Common elements' labels and properties for Issues objects."""
  ISSUE = objects.get_normal_form(objects.get_singular(objects.ISSUES))
  STATE = Base.STATE


class ReviewStates(object):
  """Objects' from 'ALL_OBJS_W_REVIEW_STATE' Review labels and properties."""
  OBJECT_REVIEW = "Object Review"
  REVIEWED = "Reviewed"
  UNREVIEWED = "Unreviewed"


class ObjectStates(object):
  """States for objects."""
  DRAFT = "Draft"
  DEPRECATED = "Deprecated"
  ACTIVE = "Active"


class BaseStates(object):
  """Common states for Audit and Assessment objects."""
  IN_PROGRESS = "In Progress"
  COMPLETED = "Completed"


class AuditStates(BaseStates):
  """States for Audits objects."""
  PLANNED = "Planned"
  MANAGER_REVIEW = "Manager Review"
  READY_FOR_EXT_REVIEW = "Ready for External Review"


class AssessmentStates(BaseStates):
  """States for Assessments objects."""
  NOT_STARTED = "Not Started"
  READY_FOR_REVIEW = "In Review"
  VERIFIED = "Verified"
  REWORK_NEEDED = "Rework Needed"


class IssueStates(ObjectStates):
  """States for Issues objects."""
  FIXED = "Fixed"
  FIXED_AND_VERIFIED = "Fixed and Verified"


class ProgramInfoWidget(CommonProgram):
  """Elements' labels and properties for Programs Info widgets."""
  WIDGET_HEADER = Base.WIDGET_INFO_HEADER_FORMAT.format(CommonProgram.PROGRAM)


class AuditInfoWidget(CommonAudit):
  """Elements' labels and properties for Audits Info widgets."""
  WIDGET_HEADER = Base.WIDGET_INFO_HEADER_FORMAT.format(CommonAudit.AUDIT)


class ControlInfoWidget(CommonControl):
  """Elements' labels and properties for Controls Info widgets."""
  WIDGET_HEADER = Base.WIDGET_INFO_HEADER_FORMAT.format(CommonControl.CONTROL)


class AssessmentInfoWidget(CommonAssessment):
  """Elements' labels and properties for Assessments Info widgets."""
  WIDGET_HEADER = Base.WIDGET_INFO_HEADER_FORMAT.format(CommonAssessment.ASMT)
  TITLE_EDITED_PART = "[EDITED]"


class IssueInfoWidget(CommonIssue):
  """Elements' labels and properties for Issue Info widgets."""
  TITLE_UPPER = CommonIssue.TITLE.upper()


class AssessmentTemplateModalSetVisibleFields(CommonModalSetVisibleFields):
  """Common elements' labels and properties for Modal to Set visible
 fields for Assessment Templates.
 """
  MODAL_HEADER = CommonModalSetVisibleFields.MODAL_HEADER_FORMAT.format(
      CommonAssessmentTemplate.ASMT_TMPL)
  ADMIN = TransformationSetVisibleFields.ADMIN
  DEFAULT_SET_FIELDS = (
      CommonModalSetVisibleFields.TITLE,
      CommonModalSetVisibleFields.CODE,
      CommonModalSetVisibleFields.LAST_UPDATED_BY,
      CommonModalSetVisibleFields.STATE)


class AssessmentModalSetVisibleFields(CommonModalSetVisibleFields):
  """Common elements' labels and properties for Modal to Set visible
 fields for Assessments.
 """
  MODAL_HEADER = CommonModalSetVisibleFields.MODAL_HEADER_FORMAT.format(
      CommonAssessment.ASMT)
  CREATORS = TransformationSetVisibleFields.CREATORS
  ASSIGNEES = TransformationSetVisibleFields.ASSIGNEES
  VERIFIERS = TransformationSetVisibleFields.VERIFIERS
  VERIFIED = TransformationSetVisibleFields.VERIFIED
  CONCLUSION_DESIGN = "Conclusion: Design"
  CONCLUSION_OPERATION = "Conclusion: Operation"
  FINISHED_DATE = "Finished Date"
  VERIFIED_DATE = "Verified Date"
  TYPE = Base.TYPE
  DEFAULT_SET_FIELDS = (
      CommonModalSetVisibleFields.TITLE, CommonModalSetVisibleFields.STATE,
      VERIFIED, CommonModalSetVisibleFields.CODE, CREATORS, ASSIGNEES,
      VERIFIERS)


class ControlModalSetVisibleFields(CommonModalSetVisibleFields):
  """Common elements' labels and properties for Modal to Set visible
 fields for Controls.
 """
  # pylint: disable=too-many-instance-attributes
  MODAL_HEADER = CommonModalSetVisibleFields.MODAL_HEADER_FORMAT.format(
      CommonControl.CONTROL)
  REVIEW_STATE = TransformationSetVisibleFields.REVIEW_STATE
  ADMIN = TransformationSetVisibleFields.ADMIN
  PRIMARY_CONTACTS = TransformationSetVisibleFields.PRIMARY_CONTACTS
  SECONDARY_CONTACTS = TransformationSetVisibleFields.SECONDARY_CONTACTS
  EFFECTIVE_DATE = Base.EFFECTIVE_DATE
  KIND_NATURE = "Kind/Nature"
  FRAUD_RELATED = "Fraud Related"
  SIGNIFICANCE = "Significance"
  TYPE_MEANS = "Type/Means"
  FREQUENCY = "Frequency"
  ASSERTIONS = "Assertions"
  CATEGORIES = "Categories"
  DEFAULT_SET_FIELDS = (
      CommonModalSetVisibleFields.TITLE, CommonModalSetVisibleFields.CODE,
      CommonModalSetVisibleFields.STATE,
      CommonModalSetVisibleFields.LAST_UPDATED_BY, REVIEW_STATE,
      PRIMARY_CONTACTS, ADMIN)


class ObjectiveModalSetVisibleFields(CommonModalSetVisibleFields):
  """Common elements' labels and properties for Modal to Set visible
 fields for Controls.
 """
  # pylint: disable=too-many-instance-attributes
  MODAL_HEADER = CommonModalSetVisibleFields.MODAL_HEADER_FORMAT.format(
      CommonObjective.OBJECTIVE)
  REVIEW_STATE = TransformationSetVisibleFields.REVIEW_STATE
  ADMIN = TransformationSetVisibleFields.ADMIN
  EFFECTIVE_DATE = Base.EFFECTIVE_DATE
  DEFAULT_SET_FIELDS = (
      CommonModalSetVisibleFields.TITLE, ADMIN,
      CommonModalSetVisibleFields.CODE, CommonModalSetVisibleFields.STATE,
      REVIEW_STATE)


class IssueModalSetVisibleFields(CommonModalSetVisibleFields):
  """Common elements' labels and properties for Modal to Set visible
 fields for Issues.
 """
  # pylint: disable=too-many-instance-attributes
  MODAL_HEADER = CommonModalSetVisibleFields.MODAL_HEADER_FORMAT.format(
      CommonIssue.ISSUE)
  ADMIN = TransformationSetVisibleFields.ADMIN
  REVIEW_STATE = TransformationSetVisibleFields.REVIEW_STATE
  PRIMARY_CONTACTS = TransformationSetVisibleFields.PRIMARY_CONTACTS
  DEFAULT_SET_FIELDS = (
      CommonModalSetVisibleFields.TITLE, CommonModalSetVisibleFields.CODE,
      CommonModalSetVisibleFields.STATE,
      CommonModalSetVisibleFields.LAST_UPDATED_BY, REVIEW_STATE,
      PRIMARY_CONTACTS, ADMIN)


class ProgramModalSetVisibleFields(CommonModalSetVisibleFields):
  """Common elements' labels and properties for Modal to Set visible
 fields for Programs.
 """
  # pylint: disable=too-many-instance-attributes
  MODAL_HEADER = CommonModalSetVisibleFields.MODAL_HEADER_FORMAT.format(
      CommonProgram.PROGRAM)
  REVIEW_STATE = TransformationSetVisibleFields.REVIEW_STATE
  MANAGER = CommonProgram.MANAGER
  EFFECTIVE_DATE = Base.EFFECTIVE_DATE
  PRIMARY_CONTACTS = TransformationSetVisibleFields.PRIMARY_CONTACTS
  SECONDARY_CONTACTS = TransformationSetVisibleFields.SECONDARY_CONTACTS
  DEFAULT_SET_FIELDS = (
      CommonModalSetVisibleFields.TITLE, CommonModalSetVisibleFields.CODE,
      CommonModalSetVisibleFields.STATE,
      CommonModalSetVisibleFields.LAST_UPDATED_BY, REVIEW_STATE, MANAGER,
      PRIMARY_CONTACTS)


class MappingStatusAttrs(namedtuple('_MappingStatusAttrs',
                                    ['title', 'is_checked', 'is_disabled'])):
  """Class for representation of html attributes for mapping checkboxes
   on unified mapper"""


class DropdownMenuItemTypes(object):
  """Class for types of DropdownMenu Item according to "icon" css class"""
  EDIT = "pencil-square-o"
  OPEN = "long-arrow-right"
  GET_PERMALINK = "link"
  DELETE = "trash"
  MAP = "code-fork"
  UNMAP = "ban"
  CLONE = "clone"
  UPDATE = "refresh"


class TransformationElements(TransformationSetVisibleFields, CommonAssessment):
  """All transformation elements' labels and properties witch are using to
  convert UI attributes to entities attributes.
  """
  OBJECT_REVIEW = ReviewStates.OBJECT_REVIEW
  COMMENTS_HEADER = "RESPONSES/COMMENTS"


class TabContainer(object):
  """Elements' labels for Common Tab Container."""
  OBJ_TAB = "Attributes"
  CHANGE_LOG_TAB = "Change Log"


class AssessmentTabContainer(TabContainer):
  """Elements' labels for Assessment Tab Container."""
  OBJ_TAB = "Assessment"
  RELATED_ASMTS_TAB = "Related Assessments"
  RELATED_ISSUES_TAB = "Related Issues"
  OTHER_ATTRS_TAB = "Other Attributes"


class AsmtAttrsTab(object):
  """Common elements' labels of Assessment Attributes Tab on Assessment Info
  Widget."""
  TAB_NAME = AssessmentTabContainer.OTHER_ATTRS_TAB


class AsmtLogTab(object):
  """Common elements' labels of Assessment Log Tab on Assessment Info
   Widget."""
  TAB_NAME = AssessmentTabContainer.CHANGE_LOG_TAB
  FIELD = "Field"
  ORIGINAL_VALUE = "Original value"
  NEW_VALUE = "New value"
  EMPTY_STATEMENT = u"\u2014"  # em-dash


class RelatedAsmtsTab(object):
  """Common elements' labels of Assessment Related Assessments Tab on
  Assessment InfoWidget.
  """
  TAB_NAME = AssessmentTabContainer.RELATED_ASMTS_TAB
  ASSESSMENT_TITLE = "Assessment Title"
  RELATED_OBJECTS = "Related {}"  # '{}' part depend on Assessment's type
  AUDIT_TITLE = "Audit Title"


class RelatedIssuesTab(object):
  """Common elements' labels of Assessment Related Issues Tab on
   Assessment InfoWidget.
   """
  TAB_NAME = AssessmentTabContainer.RELATED_ISSUES_TAB
  TITLE = Common.TITLE
  DESCRIPTION = Common.DESCRIPTION


class UnifiedMapperModal(object):
  """Class that represent ui of Unified Mapper."""
  ATTRIBUTE_TITLE = Common.TITLE


class GenericWidget(object):
  """Elements' labels and properties for Generic Widget."""
  NO_FILTER_RESULTS = "No results, please check your filter criteria"


class ExportPage(object):
  """Elements' labels and properties for Export Page."""
  GOOGLE_SHEET = "Google Sheet"
  CSV = "CSV File"
