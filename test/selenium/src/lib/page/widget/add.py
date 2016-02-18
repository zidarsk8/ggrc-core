# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com
"""Models for the add widget button in the widget bar"""

from lib import base
from lib.constants import locator
import lib.page.widget


class AddWidget(base.Component):
  """No elements are initiated here because based on the context they may be
  missing"""

  _locator = locator.WidgetBarButtonAddDropdown

  def select_people(self):
    """
    Returns:
        People
    """
    self._driver.find_element(*self._locator.PERSON).click()
    raise NotImplementedError

  def select_audits(self):
    """
    Returns:
        Audits
    """
    self._driver.find_element(*self._locator.AUDITS).click()
    raise NotImplementedError

  def select_programs(self):
    """
    Returns:
        Programs
    """
    self._driver.find_element(*self._locator.PROGRAM).click()
    raise NotImplementedError

  def select_access_groups(self):
    """
    Returns:
        AccessGroups
    """
    self._driver.find_element(*self._locator.ACCESS_GROUP).click()
    raise NotImplementedError

  def select_clauses(self):
    """
    Returns:
        Clauses
    """
    self._driver.find_element(*self._locator.CLAUSE).click()
    raise NotImplementedError

  def select_controls(self):
    """
    Returns:
        Controls
    """
    self._driver.find_element(*self._locator.CONTROLS).click()
    return lib.page.widget.Controls(self._driver)

  def select_facilities(self):
    """
    Returns:
        Facilities
    """
    self._driver.find_element(*self._locator.FACILITIES).click()
    raise NotImplementedError

  def select_markets(self):
    """
    Returns:
        Markets
    """
    self._driver.find_element(*self._locator.MARKETS).click()
    raise NotImplementedError

  def select_org_groups(self):
    """
    Returns:
        OrgGroups
    """
    self._driver.find_element(*self._locator.ORG_GROUPS).click()
    raise NotImplementedError

  def select_processes(self):
    """
    Returns:
        Processes
    """
    self._driver.find_element(*self._locator.PROCESSES).click()
    raise NotImplementedError

  def select_projects(self):
    """
    Returns:
        Projects
    """
    self._driver.find_element(*self._locator.PROJECTS).click()
    raise NotImplementedError

  def select_requests(self):
    """
    Returns:
        Requests
    """
    self._driver.find_element(*self._locator.REQUEST).click()
    raise NotImplementedError

  def select_standards(self):
    """
    Returns:
        Standards
    """
    self._driver.find_element(*self._locator.STANDARDS).click()
    raise NotImplementedError

  def select_vendors(self):
    """
    Returns:
        Vendor
    """
    self._driver.find_element(*self._locator.VENDORS).click()
    raise NotImplementedError

  def select_risks(self):
    """
    Returns:
        Risks
    """
    self._driver.find_element(*self._locator.RISKS).click()
    raise NotImplementedError

  def select_assessments(self):
    """
    Returns:
        Assessments
    """
    self._driver.find_element(*self._locator.ASSESSMENTS).click()
    raise NotImplementedError

  def select_contracts(self):
    """
    Returns:
        Contracts
    """
    self._driver.find_element(*self._locator.CONTRACTS).click()
    raise NotImplementedError

  def select_data_assets(self):
    """
    Returns:
        DataAssets
    """
    self._driver.find_element(*self._locator.DATA_ASSETS).click()
    raise NotImplementedError

  def select_issues(self):
    """
    Returns:
        Issues
    """
    self._driver.find_element(*self._locator.ISSUES).click()
    raise NotImplementedError

  def select_objectives(self):
    """
    Returns:
        Objectives
    """
    self._driver.find_element(*self._locator.OBJECTIVES).click()
    raise NotImplementedError

  def select_policies(self):
    """
    Returns:
        Policies
    """
    self._driver.find_element(*self._locator.POLICIES).click()
    raise NotImplementedError

  def select_products(self):
    """
    Returns:
        Products
    """
    self._driver.find_element(*self._locator.PRODUCTS).click()
    raise NotImplementedError

  def select_regulations(self):
    """
    Returns:
        Regulations
    """
    self._driver.find_element(*self._locator.REGULATIONS).click()
    raise NotImplementedError

  def select_sections(self):
    """
    Returns:
        Sections
    """
    self._driver.find_element(*self._locator.SECTION).click()
    raise NotImplementedError

  def select_systems(self):
    """
    Returns:
        Systems
    """
    self._driver.find_element(*self._locator.SYSTEMS).click()
    raise NotImplementedError

  def select_threats(self):
    """
    Returns:
        Threats
    """
    self._driver.find_element(*self._locator.THREAT).click()
    raise NotImplementedError
