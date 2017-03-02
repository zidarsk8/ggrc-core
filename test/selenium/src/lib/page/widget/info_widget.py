# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Info widgets and info panels."""

from lib import base
from lib.constants import locator, objects
from lib.element import widget_info
from lib.page.modal import update_object


class CommonInfo(base.Widget):
  """Abstract class of common info for Info widgets and Info panels."""
  _locator = locator.CommonWidgetInfo
  _dropdown_settings_cls = widget_info.CommonDropdownSettings
  list_headers = None
  list_values = None

  def __init__(self, driver):
    # wait that the elements load before calling super
    self.title = base.Label(driver, self._locator.TITLE)
    self.title_entered = base.Label(driver, self._locator.TITLE_ENTERED)
    self.state = base.Label(driver, self._locator.STATE)
    self.button_3bbs = None
    super(CommonInfo, self).__init__(driver)

  def open_info_3bbs(self):
    """Click to 3bbs button on Info widget or Info panel to open modal for
    further actions.
    """
    self.button_3bbs = base.Button(self._driver, self._locator.BUTTON_3BBS)
    self.button_3bbs.click()
    return self._dropdown_settings_cls(self._driver)

  def get_obj_as_dict(self):
    """Get dict from object (text scope) which displayed on info widget or
    info panel according to list of headers and list of values.
    """
    return dict(zip(self.list_headers, self.list_values))


class CommonSnapshotsInfo(base.Component):
  """Class of common info for Info panels of snapshotable objects."""
  # pylint: disable=too-few-public-methods
  def __init__(self, driver):
    super(CommonSnapshotsInfo, self).__init__(driver)
    self.link_get_latest_ver = None

  def open_link_get_latest_ver(self):
    """Click to link to open modal for further update object."""
    self.link_get_latest_ver = base.Button(
        self._driver, locator.CommonWidgetInfoSnapshots.LINK_GET_LAST_VER)
    self.link_get_latest_ver.click()
    return update_object.CompareUpdateObjectModal(self._driver)


class ProgramsInfoWidget(CommonInfo):
  """Model for program object Info widgets and Info panels."""
  # pylint: disable=too-many-instance-attributes
  _locator = locator.WidgetInfoProgram
  _dropdown_settings_cls = widget_info.Programs

  def __init__(self, driver):
    super(ProgramsInfoWidget, self).__init__(driver)
    # activate all fields
    self.show_advanced = base.Toggle(
        self._driver, self._locator.TOGGLE_SHOW_ADVANCED)
    self.show_advanced.toggle()
    self.object_review = base.Label(self._driver, self._locator.OBJECT_REVIEW)
    self.submit_for_review = base.Label(
        self._driver, self._locator.SUBMIT_FOR_REVIEW)
    self.description = base.Label(self._driver, self._locator.DESCRIPTION)
    self.description_entered = base.Label(
        self._driver, self._locator.DESCRIPTION_ENTERED)
    self.notes = base.Label(self._driver, self._locator.NOTES)
    self.notes_entered = base.Label(self._driver, self._locator.NOTES_ENTERED)
    self.manager = base.Label(self._driver, self._locator.MANAGER)
    self.manager_entered = base.Label(
        self._driver, self._locator.MANAGER_ENTERED)
    self.primary_contact = base.Label(
        self._driver, self._locator.PRIMARY_CONTACT)
    self.primary_contact_entered = base.Label(
        self._driver, self._locator.PRIMARY_CONTACT_ENTERED)
    self.secondary_contact = base.Label(
        self._driver, self._locator.SECONDARY_CONTACT)
    self.secondary_contact_entered = base.Label(
        self._driver, self._locator.SECONDARY_CONTACT_ENTERED)
    self.program_url = base.Label(self._driver, self._locator.PROGRAM_URL)
    self.program_url_entered = base.Label(
        self._driver, self._locator.PROGRAM_URL_ENTERED)
    self.reference_url = base.Label(self._driver, self._locator.REFERENCE_URL)
    self.reference_url_entered = base.Label(
        self._driver, self._locator.REFERENCE_URL_ENTERED)
    self.code = base.Label(self._driver, self._locator.CODE)
    self.code_entered = base.Label(self._driver, self._locator.CODE_ENTERED)
    self.effective_date = base.Label(
        self._driver, self._locator.EFFECTIVE_DATE)
    self.effective_date_entered = base.Label(
        self._driver, self._locator.EFFECTIVE_DATE_ENTERED)
    self.stop_date = base.Label(self._driver, self._locator.STOP_DATE)
    self.stop_date_entered = base.Label(
        self._driver, self._locator.STOP_DATE_ENTERED)


class WorkflowsInfoWidget(CommonInfo):
  """Model for Workflow object Info widgets."""
  _locator = locator.WidgetInfoWorkflow

  def __init__(self, driver):
    super(WorkflowsInfoWidget, self).__init__(driver)


class AuditsInfoWidget(CommonInfo):
  """Model for Audit object Info widgets."""
  # pylint: disable=too-many-instance-attributes
  _locator = locator.WidgetInfoAudit
  _dropdown_settings_cls = widget_info.Audits

  def __init__(self, driver):
    super(AuditsInfoWidget, self).__init__(driver)
    self.title = base.Label(driver, self._locator.TITLE)
    self.title_entered = base.Label(driver, self._locator.TITLE_ENTERED)
    self.state = base.Label(driver, self._locator.STATE)
    self.audit_lead = base.Label(driver, self._locator.AUDIT_LEAD)
    self.audit_lead_entered = base.Label(
        driver, self._locator.AUDIT_LEAD_ENTERED)
    self.code_common = base.Label(driver, self._locator.CODE_COMMON)
    self.list_headers = [
        self.title.text, self._locator.elements.STATUS.upper(),
        self.audit_lead.text, self.code_common.text.splitlines()[0]]
    self.list_values = [
        self.title_entered.text, objects.get_normal_form(self.state.text),
        self.audit_lead_entered.text, self.code_common.text.splitlines()[1]]


class AssessmentsInfoWidget(CommonInfo):
  """Model for Assessment object Info widgets."""
  _locator = locator.WidgetInfoAssessment

  def __init__(self, driver):
    super(AssessmentsInfoWidget, self).__init__(driver)


class AssessmentTemplatesInfoWidget(CommonInfo):
  """Model for Assessment Template object Info widgets."""
  _locator = locator.WidgetInfoAssessmentTemplate

  def __init__(self, driver):
    super(AssessmentTemplatesInfoWidget, self).__init__(driver)


class IssuesInfoWidget(CommonInfo):
  """Model for Issue object Info widgets."""
  _locator = locator.WidgetInfoIssue

  def __init__(self, driver):
    super(IssuesInfoWidget, self).__init__(driver)


class RegulationsInfoWidget(CommonInfo):
  """Model for Assessment object Info widgets."""
  _locator = locator.WidgetInfoRegulations

  def __init__(self, driver):
    super(RegulationsInfoWidget, self).__init__(driver)


class PoliciesInfoWidget(CommonInfo):
  """Model for Policy object Info widgets."""
  _locator = locator.WidgetInfoPolicy

  def __init__(self, driver):
    super(PoliciesInfoWidget, self).__init__(driver)


class StandardsInfoWidget(CommonInfo):
  """Model for Standard object Info widgets."""
  _locator = locator.WidgetInfoStandard

  def __init__(self, driver):
    super(StandardsInfoWidget, self).__init__(driver)


class ContractsInfoWidget(CommonInfo):
  """Model for Contract object Info widgets."""
  _locator = locator.WidgetInfoContract

  def __init__(self, driver):
    super(ContractsInfoWidget, self).__init__(driver)


class ClausesInfoWidget(CommonInfo):
  """Model for Clause object Info widgets."""
  _locator = locator.WidgetInfoClause

  def __init__(self, driver):
    super(ClausesInfoWidget, self).__init__(driver)


class SectionsInfoWidget(CommonInfo):
  """Model for Section object Info widgets."""
  _locator = locator.WidgetInfoSection

  def __init__(self, driver):
    super(SectionsInfoWidget, self).__init__(driver)


class ControlsInfoWidget(CommonInfo, CommonSnapshotsInfo):
  """Model for Control object Info widgets."""
  _locator = locator.WidgetInfoControl
  _dropdown_settings_cls = widget_info.Controls

  def __init__(self, driver):
    super(ControlsInfoWidget, self).__init__(driver)


class ObjectivesInfoWidget(CommonInfo):
  """Model for Objective object Info widgets."""
  _locator = locator.WidgetInfoObjective

  def __init__(self, driver):
    super(ObjectivesInfoWidget, self).__init__(driver)


class PeopleInfoWidget(base.Widget):
  """Model for People object Info widgets."""
  _locator = locator.WidgetInfoPeople


class OrgGroupsInfoWidget(CommonInfo):
  """Model for Org Group object Info widgets."""
  _locator = locator.WidgetInfoOrgGroup
  _dropdown_settings_cls = widget_info.OrgGroups

  def __init__(self, driver):
    super(OrgGroupsInfoWidget, self).__init__(driver)


class VendorsInfoWidget(CommonInfo):
  """Model for Vendor object Info widgets."""
  _locator = locator.WidgetInfoVendor

  def __init__(self, driver):
    super(VendorsInfoWidget, self).__init__(driver)


class AccessGroupInfoWidget(CommonInfo):
  """Model for Access Group object Info widgets."""
  _locator = locator.WidgetInfoAccessGroup

  def __init__(self, driver):
    super(AccessGroupInfoWidget, self).__init__(driver)


class SystemsInfoWidget(CommonInfo):
  """Model for System object Info widgets."""
  _locator = locator.WidgetInfoSystem
  _dropdown_settings_cls = widget_info.Systems

  def __init__(self, driver):
    super(SystemsInfoWidget, self).__init__(driver)


class ProcessesInfoWidget(CommonInfo):
  """Model for Process object Info widgets."""
  _locator = locator.WidgetInfoProcess
  _dropdown_settings_cls = widget_info.Processes

  def __init__(self, driver):
    super(ProcessesInfoWidget, self).__init__(driver)


class DataAssetsInfoWidget(CommonInfo):
  """Model for Data Asset object Info widgets."""
  _locator = locator.WidgetInfoDataAsset
  _dropdown_settings_cls = widget_info.DataAssets

  def __init__(self, driver):
    super(DataAssetsInfoWidget, self).__init__(driver)


class ProductsInfoWidget(CommonInfo):
  """Model for Product object Info widgets."""
  _locator = locator.WidgetInfoProduct
  _dropdown_settings_cls = widget_info.Products

  def __init__(self, driver):
    super(ProductsInfoWidget, self).__init__(driver)


class ProjectsInfoWidget(CommonInfo):
  """Model for Project object Info widgets."""
  _locator = locator.WidgetInfoProject
  _dropdown_settings_cls = widget_info.Projects

  def __init__(self, driver):
    super(ProjectsInfoWidget, self).__init__(driver)


class FacilitiesInfoWidget(CommonInfo):
  """Model for Facility object Info widgets."""
  _locator = locator.WidgetInfoFacility

  def __init__(self, driver):
    super(FacilitiesInfoWidget, self).__init__(driver)


class MarketsInfoWidget(CommonInfo):
  """Model for Market object Info widgets."""
  _locator = locator.WidgetInfoMarket

  def __init__(self, driver):
    super(MarketsInfoWidget, self).__init__(driver)


class RisksInfoWidget(CommonInfo):
  """Model for Risk object Info widgets."""
  _locator = locator.WidgetInfoRisk

  def __init__(self, driver):
    super(RisksInfoWidget, self).__init__(driver)


class ThreatsInfoWidget(CommonInfo):
  """Model for Threat object Info widgets."""
  _locator = locator.WidgetInfoThreat

  def __init__(self, driver):
    super(ThreatsInfoWidget, self).__init__(driver)


class DashboardInfoWidget(CommonInfo):
  """Model for Dashboard object Info widgets."""
  _locator = locator.Dashboard

  def __init__(self, driver):
    super(DashboardInfoWidget, self).__init__(driver)
    self.button_start_new_program = base.Button(
        self._driver, self._locator.BUTTON_START_NEW_PROGRAM)
    self.button_start_new_audit = base.Button(
        self._driver, self._locator.BUTTON_START_NEW_AUDIT)
    self.button_start_new_workflow = base.Button(
        self._driver, self._locator.BUTTON_START_NEW_WORKFLOW)
    self.button_create_new_object = base.Button(
        self._driver, self._locator.BUTTON_CREATE_NEW_OBJECT)
    self.button_all_objects = base.Button(
        self._driver, self._locator.BUTTON_ALL_OBJECTS)
