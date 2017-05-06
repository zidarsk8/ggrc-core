# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Info widgets."""

from lib import base
from lib.constants import locator, objects
from lib.element import widget_info
from lib.page.modal import update_object
from lib.utils import selenium_utils


class CommonInfo(base.Widget):
  """Abstract class of common info for Info pages and Info panels."""
  _locators = locator.CommonWidgetInfo
  dropdown_settings_cls = widget_info.CommonDropdownSettings
  list_headers_text = None
  list_values_text = None

  def __init__(self, driver):
    # wait that the elements load before calling super
    self.title = base.Label(driver, self._locators.TITLE)
    self.title_entered = base.Label(driver, self._locators.TITLE_ENTERED)
    self.state = base.Label(driver, self._locators.STATE)
    super(CommonInfo, self).__init__(driver)
    self.locator_3bbs = (
        self._locators.BUTTON_3BBS_UNDER_AUDIT if self.is_under_audit
        else self._locators.BUTTON_3BBS)

  def open_info_3bbs(self):
    """Click to 3BBS button on Info page or Info panel to open info 3BBS modal.
    Return: lib.element.widget_info."obj_name"DropdownSettings
    """
    base.Button(self._driver, self.locator_3bbs).click()
    return self.dropdown_settings_cls(self._driver, self.is_under_audit)

  def get_value_by_header_text(self, header_text):
    """Get text of value element by header element text used searching in
    text scopes of headers and values.
    """
    # pylint: disable=not-an-iterable
    headers_and_values = selenium_utils.get_when_all_visible(
        self._driver, self._locators.HEADERS_AND_VALUES)
    return [scope.text.splitlines()[1] for scope in headers_and_values
            if header_text in scope.text][0]

  def get_obj_as_dict(self):
    """Get dict from object (text scope) which displayed on info page or
    info panel according to list of headers text and list of values text.
    """
    return dict(zip(self.list_headers_text, self.list_values_text))


class CommonSnapshotsInfo(base.Component):
  """Class of common info for Info pages and Info Panels of
  snapshotable objects."""
  # pylint: disable=too-few-public-methods
  _locators = locator.CommonWidgetInfoSnapshots
  locator_link_get_latest_ver = _locators.LINK_GET_LAST_VER

  def __init__(self, driver):
    super(CommonSnapshotsInfo, self).__init__(driver)

  def open_link_get_latest_ver(self):
    """Click on link get latest version under Info panel."""
    base.Button(self._driver, self.locator_link_get_latest_ver).click()
    return update_object.CompareUpdateObjectModal(self._driver)

  def is_link_get_latest_ver_exist(self):
    """Find link get latest version under Info panel.
    Return: True if link get latest version is exist,
            False if link get latest version is not exist.
    """
    return selenium_utils.is_element_exist(self._driver,
                                           self.locator_link_get_latest_ver)


class Programs(CommonInfo):
  """Model for program object Info pages and Info panels."""
  # pylint: disable=too-many-instance-attributes
  _locators = locator.WidgetInfoProgram
  dropdown_settings_cls = widget_info.Programs

  def __init__(self, driver):
    super(Programs, self).__init__(driver)
    # activate all fields
    self.show_advanced = base.Toggle(
        self._driver, self._locators.TOGGLE_SHOW_ADVANCED)
    self.show_advanced.toggle()
    self.object_review = base.Label(self._driver, self._locators.OBJECT_REVIEW)
    self.submit_for_review = base.Label(
        self._driver, self._locators.SUBMIT_FOR_REVIEW)
    self.description = base.Label(self._driver, self._locators.DESCRIPTION)
    self.description_entered = base.Label(
        self._driver, self._locators.DESCRIPTION_ENTERED)
    self.notes = base.Label(self._driver, self._locators.NOTES)
    self.notes_entered = base.Label(self._driver, self._locators.NOTES_ENTERED)
    self.manager = base.Label(self._driver, self._locators.MANAGER)
    self.manager_entered = base.Label(
        self._driver, self._locators.MANAGER_ENTERED)
    self.program_url = base.Label(self._driver, self._locators.PROGRAM_URL)
    self.program_url_entered = base.Label(
        self._driver, self._locators.PROGRAM_URL_ENTERED)
    self.reference_url = base.Label(self._driver, self._locators.REFERENCE_URL)
    self.reference_url_entered = base.Label(
        self._driver, self._locators.REFERENCE_URL_ENTERED)
    self.code = base.Label(self._driver, self._locators.CODE)
    self.code_entered = base.Label(self._driver, self._locators.CODE_ENTERED)
    self.effective_date = base.Label(
        self._driver, self._locators.EFFECTIVE_DATE)
    self.effective_date_entered = base.Label(
        self._driver, self._locators.EFFECTIVE_DATE_ENTERED)
    self.stop_date = base.Label(self._driver, self._locators.STOP_DATE)
    self.stop_date_entered = base.Label(
        self._driver, self._locators.STOP_DATE_ENTERED)


class Workflows(CommonInfo):
  """Model for Workflow object Info pages and Info panels."""
  _locators = locator.WidgetInfoWorkflow

  def __init__(self, driver):
    super(Workflows, self).__init__(driver)


class Audits(CommonInfo):
  """Model for Audit object Info pages and Info panels."""
  # pylint: disable=too-many-instance-attributes
  _locators = locator.WidgetInfoAudit
  dropdown_settings_cls = widget_info.Audits

  def __init__(self, driver):
    super(Audits, self).__init__(driver)
    self.title = base.Label(driver, self._locators.TITLE)
    self.title_entered = base.Label(driver, self._locators.TITLE_ENTERED)
    self.state = base.Label(driver, self._locators.STATE)
    self.audit_lead = base.Label(driver, self._locators.AUDIT_LEAD)
    self.code = base.Label(driver, self._locators.CODE)
    # scopes
    self.audit_lead_entered_text = self.get_value_by_header_text(
        self.audit_lead.text)
    self.code_entered_text = self.get_value_by_header_text(self.code.text)
    # scope
    self.list_headers_text = [
        self.title.text, self._locators.elements.STATUS.upper(),
        self.audit_lead.text, self.code.text]
    self.list_values_text = [
        self.title_entered.text, objects.get_normal_form(self.state.text),
        self.audit_lead_entered_text, self.code_entered_text]


class Assessments(CommonInfo):
  """Model for Assessment object Info pages and Info panels."""
  _locators = locator.WidgetInfoAssessment

  def __init__(self, driver):
    super(Assessments, self).__init__(driver)


class AssessmentTemplates(CommonInfo):
  """Model for Assessment Template object Info pages and Info panels."""
  _locators = locator.WidgetInfoAssessmentTemplate

  def __init__(self, driver):
    super(AssessmentTemplates, self).__init__(driver)


class Issues(CommonInfo):
  """Model for Issue object Info pages and Info panels."""
  _locators = locator.WidgetInfoIssue

  def __init__(self, driver):
    super(Issues, self).__init__(driver)


class Regulations(CommonInfo):
  """Model for Assessment object Info pages and Info panels."""
  _locators = locator.WidgetInfoRegulations

  def __init__(self, driver):
    super(Regulations, self).__init__(driver)


class Policies(CommonInfo):
  """Model for Policy object Info pages and Info panels."""
  _locators = locator.WidgetInfoPolicy

  def __init__(self, driver):
    super(Policies, self).__init__(driver)


class Standards(CommonInfo):
  """Model for Standard object Info pages and Info panels."""
  _locators = locator.WidgetInfoStandard

  def __init__(self, driver):
    super(Standards, self).__init__(driver)


class Contracts(CommonInfo):
  """Model for Contract object Info pages and Info panels."""
  _locators = locator.WidgetInfoContract

  def __init__(self, driver):
    super(Contracts, self).__init__(driver)


class Clauses(CommonInfo):
  """Model for Clause object Info pages and Info panels."""
  _locators = locator.WidgetInfoClause

  def __init__(self, driver):
    super(Clauses, self).__init__(driver)


class Sections(CommonInfo):
  """Model for Section object Info pages and Info panels."""
  _locators = locator.WidgetInfoSection

  def __init__(self, driver):
    super(Sections, self).__init__(driver)


class Controls(CommonInfo, CommonSnapshotsInfo):
  """Model for Control object Info pages and Info panels."""
  _locators = locator.WidgetInfoControl
  dropdown_settings_cls = widget_info.Controls

  def __init__(self, driver):
    super(Controls, self).__init__(driver)


class Objectives(CommonInfo):
  """Model for Objective object Info pages and Info panels."""
  _locators = locator.WidgetInfoObjective

  def __init__(self, driver):
    super(Objectives, self).__init__(driver)


class People(base.Widget):
  """Model for People object Info pages and Info panels."""
  # pylint: disable=too-few-public-methods
  _locators = locator.WidgetInfoPeople


class OrgGroups(CommonInfo):
  """Model for Org Group object Info pages and Info panels."""
  _locators = locator.WidgetInfoOrgGroup
  dropdown_settings_cls = widget_info.OrgGroups

  def __init__(self, driver):
    super(OrgGroups, self).__init__(driver)


class Vendors(CommonInfo):
  """Model for Vendor object Info pages and Info panels."""
  _locators = locator.WidgetInfoVendor

  def __init__(self, driver):
    super(Vendors, self).__init__(driver)


class AccessGroup(CommonInfo):
  """Model for Access Group object Info pages and Info panels."""
  _locators = locator.WidgetInfoAccessGroup

  def __init__(self, driver):
    super(AccessGroup, self).__init__(driver)


class Systems(CommonInfo):
  """Model for System object Info pages and Info panels."""
  _locators = locator.WidgetInfoSystem
  dropdown_settings_cls = widget_info.Systems

  def __init__(self, driver):
    super(Systems, self).__init__(driver)


class Processes(CommonInfo):
  """Model for Process object Info pages and Info panels."""
  _locators = locator.WidgetInfoProcess
  dropdown_settings_cls = widget_info.Processes

  def __init__(self, driver):
    super(Processes, self).__init__(driver)


class DataAssets(CommonInfo):
  """Model for Data Asset object Info pages and Info panels."""
  _locators = locator.WidgetInfoDataAsset
  dropdown_settings_cls = widget_info.DataAssets

  def __init__(self, driver):
    super(DataAssets, self).__init__(driver)


class Products(CommonInfo):
  """Model for Product object Info pages and Info panels."""
  _locators = locator.WidgetInfoProduct
  dropdown_settings_cls = widget_info.Products

  def __init__(self, driver):
    super(Products, self).__init__(driver)


class Projects(CommonInfo):
  """Model for Project object Info pages and Info panels."""
  _locators = locator.WidgetInfoProject
  dropdown_settings_cls = widget_info.Projects

  def __init__(self, driver):
    super(Projects, self).__init__(driver)


class Facilities(CommonInfo):
  """Model for Facility object Info pages and Info panels."""
  _locators = locator.WidgetInfoFacility

  def __init__(self, driver):
    super(Facilities, self).__init__(driver)


class Markets(CommonInfo):
  """Model for Market object Info pages and Info panels."""
  _locators = locator.WidgetInfoMarket

  def __init__(self, driver):
    super(Markets, self).__init__(driver)


class Risks(CommonInfo):
  """Model for Risk object Info pages and Info panels."""
  _locators = locator.WidgetInfoRisk

  def __init__(self, driver):
    super(Risks, self).__init__(driver)


class Threats(CommonInfo):
  """Model for Threat object Info pages and Info panels."""
  _locators = locator.WidgetInfoThreat

  def __init__(self, driver):
    super(Threats, self).__init__(driver)


class Dashboard(CommonInfo):
  """Model for Dashboard object Info pages and Info panels."""
  _locators = locator.Dashboard

  def __init__(self, driver):
    super(Dashboard, self).__init__(driver)
    self.button_start_new_program = base.Button(
        self._driver, self._locators.BUTTON_START_NEW_PROGRAM)
    self.button_start_new_audit = base.Button(
        self._driver, self._locators.BUTTON_START_NEW_AUDIT)
    self.button_start_new_workflow = base.Button(
        self._driver, self._locators.BUTTON_START_NEW_WORKFLOW)
    self.button_create_new_object = base.Button(
        self._driver, self._locators.BUTTON_CREATE_NEW_OBJECT)
    self.button_all_objects = base.Button(
        self._driver, self._locators.BUTTON_ALL_OBJECTS)
