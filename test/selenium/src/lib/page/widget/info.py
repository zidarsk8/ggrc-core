# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib import environment
from lib.constants import url
from lib.constants import locator
from lib.element import widget_info


class InfoWidget(base.Widget):
  """Model for a generic info widget"""

  _dropdown_settings_cls = None

  def __init__(self, driver):
    super(InfoWidget, self).__init__(driver)

    self.button_settings = base.Button(driver,
                                       locator.InfoWidget.BUTTON_SETTINGS)
    self.object_id = self.url.split("/")[-1]

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
  URL = environment.APP_URL + url.DASHBOARD

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


class ProgramInfo(InfoWidget):
  """Model for program object info widget"""

  _locators = locator.ProgramInfoWidget
  _dropdown_settings_cls = widget_info.DropdownSettingsPrograms

  def __init__(self, driver):
    """
    Args:
        driver (base.CustomDriver)
    """
    super(ProgramInfo, self).__init__(driver)
    self.show_advanced = base.Toggle(
        self._driver, self._locators.BUTTON_SHOW_ADVANCED)

    # activate all fields
    self.show_advanced.click()

    self.title = base.Label(self._driver, self._locators.TITLE)
    self.title_entered = base.Label(
        self._driver, self._locators.TITLE_ENTERED)
    self.object_review = base.Label(
        self._driver, self._locators.OBJECT_REVIEW)
    self.submit_for_review = base.Label(
        self._driver, self._locators.SUBMIT_FOR_REVIEW)
    self.description = base.Label(self._driver, self._locators.DESCRIPTION)
    self.description_entered = base.Label(
        self._driver, self._locators.DESCRIPTION_ENTERED)
    self.notes = base.Label(self._driver, self._locators.NOTES)
    self.notes_entered = base.Label(
        self._driver, self._locators.NOTES_ENTERED)
    self.manager = base.Label(self._driver, self._locators.MANAGER)
    self.manager_entered = base.Label(
        self._driver, self._locators.MANAGER_ENTERED)
    self.program_url = base.Label(self._driver, self._locators.PROGRAM_URL)
    self.program_url_entered = base.Label(
        self._driver, self._locators.PROGRAM_URL_ENTERED)
    self.code = base.Label(self._driver, self._locators.CODE)
    self.code_entered = base.Label(
        self._driver, self._locators.CODE_ENTERED)
    self.effective_date = base.Label(
        self._driver, self._locators.EFFECTIVE_DATE)
    self.effective_date_entered = base.Label(
        self._driver, self._locators.EFFECTIVE_DATE_ENTERED)
    self.stop_date = base.Label(self._driver, self._locators.STOP_DATE)
    self.stop_date_entered = base.Label(
        self._driver, self._locators.STOP_DATE_ENTERED)
    self.primary_contact = base.Label(
        self._driver, self._locators.PRIMARY_CONTACT)
    self.primary_contact_entered = base.Label(
        self._driver, self._locators.PRIMARY_CONTACT_ENTERED)
    self.secondary_contact = base.Label(
        self._driver, self._locators.SECONDARY_CONTACT)
    self.secondary_contact_entered = base.Label(
        self._driver, self._locators.SECONDARY_CONTACT_ENTERED)
    self.reference_url = base.Label(
        self._driver, self._locators.REFERENCE_URL)
    self.reference_url_entered = base.Label(
        self._driver, self._locators.REFERENCE_URL_ENTERED)


class WorkflowInfo(InfoWidget):
  """Model for workflow object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.WORKFLOWS


class AuditInfo(InfoWidget):
  """Model for audit object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.AUDITS


class AssessmentsInfo(InfoWidget):
  """Model for assessment object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.ASSESSMENTS


class RequestsInfo(InfoWidget):
  """Model for request object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.REQUESTS


class IssuesInfo(InfoWidget):
  """Model for issue object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.ISSUES


class RegulationsInfo(InfoWidget):
  """Model for regulation object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.REGULATIONS


class PoliciesInfo(InfoWidget):
  """Model for policies object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.POLICIES


class StandardsInfo(InfoWidget):
  """Model for standard object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.STANDARDS


class ContractsInfo(InfoWidget):
  """Model for contract object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.CONTRACTS


class ClausesInfo(InfoWidget):
  """Model for clause object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.CLAUSES


class SectionsInfo(InfoWidget):
  """Model for selection object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.SECTIONS


class ControlInfo(InfoWidget):
  """Model for control object info widget"""

  _locators = locator.WidgetInfoSettingsButton
  _dropdown_settings_cls = widget_info.DropdownSettingsControls

  def __init__(self, driver):
    """
    Args:
        driver (base.CustomDriver)
    """
    super(ControlInfo, self).__init__(driver)
    self.title_entered = base.Label(driver, self._locators.TITLE_ENTERED)


class ObjectivesInfo(InfoWidget):
  """Model for objectives object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.OBJECTIVES


class PeopleInfo(base.Widget):
  """Model for people object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.PEOPLE


class OrgGroupsInfo(InfoWidget):
  """Model for org groups object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.ORG_GROUPS


class VendorsInfo(InfoWidget):
  """Model for vendors object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.VENDORS


class AccessGroupInfo(InfoWidget):
  """Model for access group object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.ACCESS_GROUPS


class SystemInfo(InfoWidget):
  """Model for system object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.SYSTEMS


class ProcessInfo(InfoWidget):
  """Model for process object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.PROCESSES


class DataAssetInfo(InfoWidget):
  """Model for data asset object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.DATA_ASSETS


class ProductInfo(InfoWidget):
  """Model for product object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.PRODUCTS


class ProjectInfo(InfoWidget):
  """Model for project object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.PROJECTS


class FacilityInfo(InfoWidget):
  """Model for facility object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.FACILITIES


class MarketInfo(InfoWidget):
  """Model for market object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.MARKETS


class RiskInfo(InfoWidget):
  """Model for risk object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.RISKS


class ThreatInfo(InfoWidget):
  """Model for threat object info widget"""

  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.THREATS
