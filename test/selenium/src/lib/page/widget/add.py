# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib.constants import locator
from lib.page.widget.base import Widget


class _ObjectsList(Widget):
    def __init__(self, driver):
        super(_ObjectsList, self).__init__(driver)
        self.filter = None


class Audits(_ObjectsList):
    pass


class Programs(_ObjectsList):
    pass


class People(_ObjectsList):
    pass


class AccessGroups(_ObjectsList):
    pass


class Clauses(_ObjectsList):
    pass


class Controls(_ObjectsList):
    pass


class Facilities(_ObjectsList):
    pass


class Markets(_ObjectsList):
    pass


class OrgGroups(_ObjectsList):
    pass


class Processes(_ObjectsList):
    pass


class Projects(_ObjectsList):
    pass


class Requests(_ObjectsList):
    pass


class Standards(_ObjectsList):
    pass


class Vendor(_ObjectsList):
    pass


class Risks(_ObjectsList):
    pass


class Workflows(_ObjectsList):
    pass


class Assessments(_ObjectsList):
    pass


class Contracts(_ObjectsList):
    pass


class DataAssets(_ObjectsList):
    pass


class Issues(_ObjectsList):
    pass


class Objectives(_ObjectsList):
    pass


class Policies(_ObjectsList):
    pass


class Products(_ObjectsList):
    pass


class Regulations(_ObjectsList):
    pass


class Sections(_ObjectsList):
    pass


class Systems(_ObjectsList):
    pass


class RiskAssessments(_ObjectsList):
    pass


class Threats(_ObjectsList):
    pass


class WorkflowTasks(_ObjectsList):
    pass


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
        return People(self._driver)

    def select_audits(self):
        """
        Returns:
            Audits
        """
        self._driver.find_element(*self._locator.AUDITS).click()
        return Audits(self._driver)

    def select_programs(self):
        """
        Returns:
            Programs
        """
        self._driver.find_element(*self._locator.PROGRAM).click()
        return Programs(self._driver)

    def select_access_groups(self):
        """
        Returns:
            AccessGroups
        """
        self._driver.find_element(*self._locator.ACCESS_GROUP).click()
        return AccessGroups(self._driver)

    def select_clauses(self):
        """
        Returns:
            Clauses
        """
        self._driver.find_element(*self._locator.CLAUSE).click()
        return Clauses(self._driver)

    def select_controls(self):
        """
        Returns:
            Controls
        """
        self._driver.find_element(*self._locator.CONTROLS).click()
        return Controls(self._driver)

    def select_facilities(self):
        """
        Returns:
            Facilities
        """
        self._driver.find_element(*self._locator.FACILITIES).click()
        return Facilities(self._driver)

    def select_markets(self):
        """
        Returns:
            Markets
        """
        self._driver.find_element(*self._locator.MARKETS).click()
        return Markets(self._driver)

    def select_org_groups(self):
        """
        Returns:
            OrgGroups
        """
        self._driver.find_element(*self._locator.ORG_GROUPS).click()
        return OrgGroups(self._driver)

    def select_processes(self):
        """
        Returns:
            Processes
        """
        self._driver.find_element(*self._locator.PROCESSES).click()
        return Processes(self._driver)

    def select_projects(self):
        """
        Returns:
            Projects
        """
        self._driver.find_element(*self._locator.PROJECTS).click()
        return Projects(self._driver)

    def select_requests(self):
        """
        Returns:
            Requests
        """
        self._driver.find_element(*self._locator.REQUEST).click()
        return Requests(self._driver)

    def select_standards(self):
        """
        Returns:
            Standards
        """
        self._driver.find_element(*self._locator.STANDARDS).click()
        return Standards(self._driver)

    def select_vendors(self):
        """
        Returns:
            Vendor
        """
        self._driver.find_element(*self._locator.VENDORS).click()
        return Vendor(self._driver)

    def select_risks(self):
        """
        Returns:
            Risks
        """
        self._driver.find_element(*self._locator.RISKS).click()
        return Risks(self._driver)

    def select_assessments(self):
        """
        Returns:
            Assessments
        """
        self._driver.find_element(*self._locator.ASSESSMENTS).click()
        return Assessments(self._driver)

    def select_contracts(self):
        """
        Returns:
            Contracts
        """
        self._driver.find_element(*self._locator.CONTRACTS).click()
        return Contracts(self._driver)

    def select_data_assets(self):
        """
        Returns:
            DataAssets
        """
        self._driver.find_element(*self._locator.DATA_ASSETS).click()
        return DataAssets(self._driver)

    def select_issues(self):
        """
        Returns:
            Issues
        """
        self._driver.find_element(*self._locator.ISSUES).click()
        return Issues(self._driver)

    def select_objectives(self):
        """
        Returns:
            Objectives
        """
        self._driver.find_element(*self._locator.OBJECTIVES).click()
        return Objectives(self._driver)

    def select_policies(self):
        """
        Returns:
            Policies
        """
        self._driver.find_element(*self._locator.POLICIES).click()
        return Policies(self._driver)

    def select_products(self):
        """
        Returns:
            Products
        """
        self._driver.find_element(*self._locator.PRODUCTS).click()
        return Products(self._driver)

    def select_regulations(self):
        """
        Returns:
            Regulations
        """
        self._driver.find_element(*self._locator.REGULATIONS).click()
        return Regulations(self._driver)

    def select_sections(self):
        """
        Returns:
            Sections
        """
        self._driver.find_element(*self._locator.SECTION).click()
        return Sections(self._driver)

    def select_systems(self):
        """
        Returns:
            Systems
        """
        self._driver.find_element(*self._locator.SYSTEMS).click()
        return Systems(self._driver)

    def select_threats(self):
        """
        Returns:
            Threats
        """
        self._driver.find_element(*self._locator.THREAT).click()
        return Threats(self._driver)
