# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Page object models for the info widget of the object"""

from lib import base
from lib.constants import locator
from lib.element import widget_info


class InfoWidget(base.Widget):
  """Model for a generic info widget"""
  _locator = None
  _dropdown_settings_cls = widget_info.DropdownSettingsControls

  def __init__(self, driver):
    # wait that the elements load before calling super
    self.button_settings = base.Button(
        driver, locator.InfoWidget.BUTTON_SETTINGS)

    super(InfoWidget, self).__init__(driver)

    self.object_id = self.url.split("/")[-1]
    self.title = base.Label(self._driver, self._locator.TITLE)
    self.title_entered = base.Label(
        self._driver, self._locator.TITLE_ENTERED)

  def press_object_settings(self):
    """
    Returns:
        widget_info.DropdownSettings
    """
    self.button_settings.click()
    return self._dropdown_settings_cls(self._driver)


class DashboardInfo(base.Widget):
  """Model for the dashboard info widget"""
  _locator = locator.Dashboard

  def __init__(self, driver):
    super(DashboardInfo, self).__init__(driver)

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

  def start_new_program(self):
    raise NotImplementedError

  def start_new_audit(self):
    raise NotImplementedError

  def start_new_workflow(self):
    raise NotImplementedError

  def create_new_object(self):
    raise NotImplementedError

  def browse_all_objects(self):
    raise NotImplementedError


class ProgramsInfo(InfoWidget):
  """Model for program object info widget"""
  _locator = locator.ProgramInfoWidget
  _dropdown_settings_cls = widget_info.DropdownSettingsPrograms

  def __init__(self, driver):
    """
    Args:
        driver (base.CustomDriver)
    """
    super(ProgramsInfo, self).__init__(driver)

    self.show_advanced = base.Toggle(
        self._driver, self._locator.TOGGLE_SHOW_ADVANCED)

    # activate all fields
    self.show_advanced.toggle()

    self.object_review = base.Label(
        self._driver, self._locator.OBJECT_REVIEW)
    self.submit_for_review = base.Label(
        self._driver, self._locator.SUBMIT_FOR_REVIEW)
    self.description = base.Label(self._driver, self._locator.DESCRIPTION)
    self.description_entered = base.Label(
        self._driver, self._locator.DESCRIPTION_ENTERED)
    self.notes = base.Label(self._driver, self._locator.NOTES)
    self.notes_entered = base.Label(
        self._driver, self._locator.NOTES_ENTERED)
    self.manager = base.Label(self._driver, self._locator.MANAGER)
    self.manager_entered = base.Label(
        self._driver, self._locator.MANAGER_ENTERED)
    self.program_url = base.Label(self._driver, self._locator.PROGRAM_URL)
    self.program_url_entered = base.Label(
        self._driver, self._locator.PROGRAM_URL_ENTERED)
    self.code = base.Label(self._driver, self._locator.CODE)
    self.code_entered = base.Label(
        self._driver, self._locator.CODE_ENTERED)
    self.effective_date = base.Label(
        self._driver, self._locator.EFFECTIVE_DATE)
    self.effective_date_entered = base.Label(
        self._driver, self._locator.EFFECTIVE_DATE_ENTERED)
    self.stop_date = base.Label(self._driver, self._locator.STOP_DATE)
    self.stop_date_entered = base.Label(
        self._driver, self._locator.STOP_DATE_ENTERED)
    self.primary_contact = base.Label(
        self._driver, self._locator.PRIMARY_CONTACT)
    self.primary_contact_entered = base.Label(
        self._driver, self._locator.PRIMARY_CONTACT_ENTERED)
    self.secondary_contact = base.Label(
        self._driver, self._locator.SECONDARY_CONTACT)
    self.secondary_contact_entered = base.Label(
        self._driver, self._locator.SECONDARY_CONTACT_ENTERED)
    self.reference_url = base.Label(
        self._driver, self._locator.REFERENCE_URL)
    self.reference_url_entered = base.Label(
        self._driver, self._locator.REFERENCE_URL_ENTERED)


class WorkflowInfo(InfoWidget):
  """Model for workflow object info widget"""
  _locator = locator.WorkflowInfoWidget


class AuditInfo(InfoWidget):
  """Model for audit object info widget"""
  _locator = locator.AuditInfoWidget


class AssessmentsInfo(InfoWidget):
  """Model for assessment object info widget"""
  _locator = locator.AssessmentInfoWidget


class RequestsInfo(InfoWidget):
  """Model for request object info widget"""
  _locator = locator.RequestInfoWidget


class IssuesInfo(InfoWidget):
  """Model for issue object info widget"""
  _locator = locator.IssueInfoWidget


class RegulationsInfo(InfoWidget):
  """Model for regulation object info widget"""
  _locator = locator.RegulationsInfoWidget


class PoliciesInfo(InfoWidget):
  """Model for policies object info widget"""
  _locator = locator.PolicyInfoWidget


class StandardsInfo(InfoWidget):
  """Model for standard object info widget"""
  _locator = locator.StandardInfoWidget


class ContractsInfo(InfoWidget):
  """Model for contract object info widget"""
  _locator = locator.ContractInfoWidget


class ClausesInfo(InfoWidget):
  """Model for clause object info widget"""
  _locator = locator.ClauseInfoWidget


class SectionsInfo(InfoWidget):
  """Model for selection object info widget"""
  _locator = locator.SectionInfoWidget


class ControlsInfo(InfoWidget):
  """Model for control object info widget"""
  _locator = locator.ControlInfoWidget


class ObjectivesInfo(InfoWidget):
  """Model for objectives object info widget"""
  _locator = locator.ObjectiveInfoWidget


class PeopleInfo(base.Widget):
  """Model for people object info widget"""
  _locator = locator.PeopleInfoWidget


class OrgGroupsInfo(InfoWidget):
  """Model for org groups object info widget"""
  _locator = locator.OrgGroupInfoWidget


class VendorsInfo(InfoWidget):
  """Model for vendors object info widget"""
  _locator = locator.VendorInfoWidget


class AccessGroupInfo(InfoWidget):
  """Model for access group object info widget"""
  _locator = locator.AccessGroupInfoWidget


class SystemInfo(InfoWidget):
  """Model for system object info widget"""
  _locator = locator.SystemInfoWidget


class ProcessesInfo(InfoWidget):
  """Model for process object info widget"""
  _locator = locator.ProcessInfoWidget


class DataAssetsInfo(InfoWidget):
  """Model for data asset object info widget"""
  _locator = locator.DataAssetInfoWidget


class ProductsInfo(InfoWidget):
  """Model for product object info widget"""
  _locator = locator.ProductInfoWidget


class ProjectsInfo(InfoWidget):
  """Model for project object info widget"""
  _locator = locator.ProjectInfoWidget


class FacilitiesInfo(InfoWidget):
  """Model for facility object info widget"""
  _locator = locator.FacilityInfoWidget


class MarketsInfo(InfoWidget):
  """Model for market object info widget"""
  _locator = locator.MarketInfoWidget


class RisksInfo(InfoWidget):
  """Model for risk object info widget"""
  _locator = locator.RiskInfoWidget


class ThreatsInfo(InfoWidget):
  """Model for threat object info widget"""
  _locator = locator.ThreatInfoWidget
