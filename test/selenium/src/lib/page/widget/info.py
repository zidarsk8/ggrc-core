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
    return widget_info.DropdownSettingsPrograms(self._driver)


class DashboardInfo(base.Widget):
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
  _locators = locator.ProgramInfoWidget

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
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.WORKFLOWS


class AuditInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.AUDITS


class AssessmentsInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.ASSESSMENTS


class RequestsInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.REQUESTS


class IssuesInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.ISSUES


class RegulationsInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.REGULATIONS


class PoliciesInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.POLICIES


class StandardsInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.STANDARDS


class ContractsInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.CONTRACTS


class ClausesInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.CLAUSES


class SectionsInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.SECTIONS


class ControlInfo(InfoWidget):
  _locators = locator.ControlInfoWidget

  def __init__(self, driver):
    """
    Args:
        driver (base.CustomDriver)
    """
    super(ControlInfo, self).__init__(driver)
    self.title_entered = base.Label(driver, self._locators.TITLE_ENTERED)


class ObjectivesInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.OBJECTIVES


class PeopleInfo(base.Widget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.PEOPLE


class OrgGroupsInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.ORG_GROUPS


class VendorsInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.VENDORS


class AccessGroupInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.ACCESS_GROUPS


class SystemInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.SYSTEMS


class ProcessInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.PROCESSES


class DataAssetInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.DATA_ASSETS


class ProductInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.PRODUCTS


class ProjectInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.PROJECTS


class FacilityInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.FACILITIES


class MarketInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.MARKETS


class RiskInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.RISKS


class ThreatInfo(InfoWidget):
  _locators = locator.ProgramInfoWidget
  URL = environment.APP_URL + url.THREATS
