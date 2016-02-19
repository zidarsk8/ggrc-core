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
    raise NotImplementedError

  def select_audits(self):
    """
    Returns:
        Audits
    """
    raise NotImplementedError

  def select_programs(self):
    """
    Returns:
        Programs
    """
    raise NotImplementedError

  def select_access_groups(self):
    """
    Returns:
        AccessGroups
    """
    raise NotImplementedError

  def select_clauses(self):
    """
    Returns:
        Clauses
    """
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
    raise NotImplementedError

  def select_markets(self):
    """
    Returns:
        Markets
    """
    raise NotImplementedError

  def select_org_groups(self):
    """
    Returns:
        OrgGroups
    """
    raise NotImplementedError

  def select_processes(self):
    """
    Returns:
        Processes
    """
    raise NotImplementedError

  def select_projects(self):
    """
    Returns:
        Projects
    """
    raise NotImplementedError

  def select_requests(self):
    """
    Returns:
        Requests
    """
    raise NotImplementedError

  def select_standards(self):
    """
    Returns:
        Standards
    """
    raise NotImplementedError

  def select_vendors(self):
    """
    Returns:
        Vendor
    """
    raise NotImplementedError

  def select_risks(self):
    """
    Returns:
        Risks
    """
    raise NotImplementedError

  def select_assessments(self):
    """
    Returns:
        Assessments
    """
    raise NotImplementedError

  def select_contracts(self):
    """
    Returns:
        Contracts
    """
    raise NotImplementedError

  def select_data_assets(self):
    """
    Returns:
        DataAssets
    """
    raise NotImplementedError

  def select_issues(self):
    """
    Returns:
        Issues
    """
    raise NotImplementedError

  def select_objectives(self):
    """
    Returns:
        Objectives
    """
    raise NotImplementedError

  def select_policies(self):
    """
    Returns:
        Policies
    """
    raise NotImplementedError

  def select_products(self):
    """
    Returns:
        Products
    """
    raise NotImplementedError

  def select_regulations(self):
    """
    Returns:
        Regulations
    """
    raise NotImplementedError

  def select_sections(self):
    """
    Returns:
        Sections
    """
    raise NotImplementedError

  def select_systems(self):
    """
    Returns:
        Systems
    """
    raise NotImplementedError

  def select_threats(self):
    """
    Returns:
        Threats
    """
    raise NotImplementedError
