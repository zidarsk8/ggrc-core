# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com
"""A page model for LHN"""
import lib.page.modal.create_new_object
from lib import base
from lib.constants import locator
from lib.element import lhn
from lib.page import modal
from lib.page import extended_info


class _Programs(lhn.AccordionGroup):
  """Programs dropdown in LHN"""

  _locator_spinny = locator.LhnMenu.SPINNY_PROGRAMS
  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_NEW_PROGRAM
  _locator_accordeon_members = locator.LhnMenu.ACCORDEON_PROGRAMS_MEMBERS
  _create_new_modal_cls = modal.create_new_object.NewProgramModal
  _modal_cls = lib.page.modal.create_new_object.NewProgramModal


class _Workflows(lhn.AccordionGroup):
  """Workflows dropdown in LHN"""

  _locator_spinny = locator.LhnMenu.SPINNY_WORKFLOWS
  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_NEW_WORKFLOW

  def __init__(self, driver):
    super(_Workflows, self).__init__(driver)
    self.button_active = base.Button(
        self._driver, locator.LhnMenu.WORKFLOWS_ACTIVE)
    self.button_inactive = base.Button(
        self._driver, locator.LhnMenu.WORKFLOWS_INACTIVE)
    self.button_draft = base.Button(
        self._driver, locator.LhnMenu.WORKFLOWS_DRAFT)


class _Audits(lhn.AccordionGroup):
  """Audits dropdown in LHN"""

  _locator_spinny = locator.LhnMenu.SPINNY_AUDITS
  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_NEW_AUDIT


class _Assessments(lhn.AccordionGroup):
  """Assessments dropdown in LHN"""

  _locator_spinny = locator.LhnMenu.SPINNY_CONTROL_ASSESSMENTS
  _locator_button_create_new = locator.LhnMenu \
      .BUTTON_CREATE_NEW_CONTROL_ASSESSMENT


class _Requests(lhn.AccordionGroup):
  """Requests dropdown in LHN"""

  _locator_spinny = locator.LhnMenu.SPINNY_REQUESTS
  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_NEW_REQUEST


class _Issues(lhn.AccordionGroup):
  """Issues dropdown in LHN"""

  _locator_spinny = locator.LhnMenu.SPINNY_ISSUES
  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_ISSUE


class _Directives(lhn.DropdownStatic):
  """Directives dropdown in LHN"""

  _locator_element = locator.LhnMenu.DIRECTIVES

  def __init__(self, driver):
    super(_Directives, self).__init__(driver)
    self.button_regulations = lhn.Button(
        self._driver,
        locator.LhnMenu.REGULATIONS,
        locator.LhnMenu.REGULATIONS_COUNT
    )
    self.button_policies = lhn.Button(
        self._driver,
        locator.LhnMenu.POLICIES,
        locator.LhnMenu.POLICIES_COUNT
    )
    self.button_standards = lhn.Button(
        self._driver,
        locator.LhnMenu.STANDARDS,
        locator.LhnMenu.STANDARDS_COUNT
    )
    self.button_contracts = lhn.Button(
        self._driver,
        locator.LhnMenu.CONTRACTS,
        locator.LhnMenu.CONTRACTS_COUNT
    )
    self.button_clauses = lhn.Button(
        self._driver,
        locator.LhnMenu.CLAUSES,
        locator.LhnMenu.CLAUSES_COUNT
    )
    self.button_sections = lhn.Button(
        self._driver,
        locator.LhnMenu.SECTIONS,
        locator.LhnMenu.SECTIONS_COUNT
    )

  def select_regulations(self):
    """
    Returns:
        _Regulations
    """
    self.button_regulations.click()
    return _Regulations(self._driver)

  def select_policies(self):
    """
    Returns:
        _Policies
    """
    self.button_policies.click()
    return _Policies(self._driver)

  def select_standards(self):
    """
    Returns:
        _Standards
    """
    self.button_standards.click()
    return _Standards(self._driver)

  def select_contracts(self):
    """
    Returns:
        _Contracts
    """
    self.button_contracts.click()
    return _Contracts(self._driver)

  def select_clauses(self):
    """
    Returns:
        _Clauses
    """
    self.button_clauses.click()
    return _Clauses(self._driver)

  def select_sections(self):
    """
    Returns:
        _Sections
    """
    self.button_sections.click()
    return _Sections(self._driver)


class _Regulations(lhn.AccordionGroup):
  """Regulations dropdown in LHN"""

  _locator_spinny = locator.LhnMenu.SPINNY_REGULATIONS
  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_REGULATION


class _Policies(lhn.AccordionGroup):
  """Policies dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_POLICY
  _locator_spinny = locator.LhnMenu.SPINNY_POLICIES


class _Standards(lhn.AccordionGroup):
  """Standards dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_STANDARD
  _locator_spinny = locator.LhnMenu.SPINNY_STANDARDS


class _Contracts(lhn.AccordionGroup):
  """Contracts dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_CONTRACT
  _locator_spinny = locator.LhnMenu.SPINNY_REGULATIONS


class _Clauses(lhn.AccordionGroup):
  """Clauses dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_CLAUSE
  _locator_spinny = locator.LhnMenu.SPINNY_CLAUSES


class _Sections(lhn.AccordionGroup):
  """Sections dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_SECTION
  _locator_spinny = locator.LhnMenu.SPINNY_SECTIONS


class _ControlsOrObjectives(lhn.DropdownStatic):
  """Controls or objects dropdown in LHN"""

  _locator_element = locator.LhnMenu.CONTROLS_OR_OBJECTIVES

  def __init__(self, driver):
    super(_ControlsOrObjectives, self).__init__(driver)
    self.button_controls = lhn.Button(
        self._driver,
        locator.LhnMenu.CONTROLS,
        locator.LhnMenu.CONTROL_COUNT
    )
    self.button_objectives = lhn.Button(
        self._driver,
        locator.LhnMenu.OBJECTIVES,
        locator.LhnMenu.OBJECTIVES_COUNT
    )

  def select_controls(self):
    """
    Returns:
        _Controls
    """
    self.button_controls.click()
    return _Controls(self._driver)

  def select_objectives(self):
    """
    Returns:
        _Objectives
    """
    self.button_objectives.click()
    return _Objectives(self._driver)


class _Controls(lhn.AccordionGroup):
  """Controls dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_CONTROL
  _locator_spinny = locator.LhnMenu.SPINNY_CONTROLS
  _locator_accordeon_members = locator.LhnMenu.ACCORDEON_CONTROLS_MEMBERS
  _create_new_modal_cls = modal.create_new_object.NewControlModal
  _extended_info_cls = extended_info.Controls


class _Objectives(lhn.AccordionGroup):
  """Objectives dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_OBJECTIVE
  _locator_spinny = locator.LhnMenu.SPINNY_OBJECTIVES


class _PeopleOrGroups(lhn.DropdownStatic):
  """Peopl or groups dropdown in LHN"""

  _locator_element = locator.LhnMenu.PEOPLE_OR_GROUPS

  def __init__(self, driver):
    super(_PeopleOrGroups, self).__init__(driver)
    self.button_people = lhn.Button(
        self._driver,
        locator.LhnMenu.PEOPLE,
        locator.LhnMenu.PEOPLE_COUNT
    )
    self.button_org_groups = lhn.Button(
        self._driver,
        locator.LhnMenu.PEOPLE,
        locator.LhnMenu.PEOPLE_COUNT
    )
    self.button_vendors = lhn.Button(
        self._driver,
        locator.LhnMenu.PEOPLE,
        locator.LhnMenu.PEOPLE_COUNT
    )
    self.button_access_groups = lhn.Button(
        self._driver,
        locator.LhnMenu.PEOPLE,
        locator.LhnMenu.PEOPLE_COUNT
    )

  def select_people(self):
    """
    Returns:
        _People
    """
    self.button_people.click()
    return _People(self._driver)

  def select_org_groups(self):
    """
    Returns:
        _OrgGroups
    """
    self.button_org_groups.click()
    return _OrgGroups(self._driver)

  def select_vendors(self):
    """
    Returns:
        _Vendors
    """
    self.button_vendors.click()
    return _Vendors(self._driver)

  def select_access_groups(self):
    """
    Returns:
        _AccessGroups
    """
    self.button_access_groups.click()
    return _AccessGroups(self._driver)


class _People(lhn.AccordionGroup):
  """People dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_PERSON
  _locator_spinny = locator.LhnMenu.SPINNY_PEOPLE


class _OrgGroups(lhn.AccordionGroup):
  """Org groups dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_ORG_GROUP
  _locator_spinny = locator.LhnMenu.SPINNY_ORG_GROUPS


class _Vendors(lhn.AccordionGroup):
  """Vendors dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_VENDOR
  _locator_spinny = locator.LhnMenu.SPINNY_VENDORS


class _AccessGroups(lhn.AccordionGroup):
  """Access groups dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_ACCESS_GROUP
  _locator_spinny = locator.LhnMenu.SPINNY_ACCESS_GROUPS


class _AssetsOrBusiness(lhn.DropdownStatic):
  """Assets or business dropdown in LHN"""

  _locator_element = locator.LhnMenu.ASSETS_OR_BUSINESS

  def __init__(self, driver):
    super(_AssetsOrBusiness, self).__init__(driver)
    self.button_systems = lhn.Button(
        self._driver,
        locator.LhnMenu.SYSTEMS,
        locator.LhnMenu.SYSTEMS_COUNT
    )
    self.button_processes = lhn.Button(
        self._driver,
        locator.LhnMenu.PROCESSES,
        locator.LhnMenu.PROCESSES_COUNT
    )
    self.button_data_assets = lhn.Button(
        self._driver,
        locator.LhnMenu.DATA_ASSETS,
        locator.LhnMenu.DATA_ASSETS_COUNT
    )
    self.button_products = lhn.Button(
        self._driver,
        locator.LhnMenu.PRODUCTS,
        locator.LhnMenu.PRODUCTS_COUNT
    )
    self.button_projects = lhn.Button(
        self._driver,
        locator.LhnMenu.PROJECTS,
        locator.LhnMenu.PROJECTS_COUNT
    )
    self.button_facilities = lhn.Button(
        self._driver,
        locator.LhnMenu.FACILITIES,
        locator.LhnMenu.FACILITIES_COUNT
    )
    self.button_markets = lhn.Button(
        self._driver,
        locator.LhnMenu.MARKETS,
        locator.LhnMenu.MARKETS_COUNT
    )

  def select_systems(self):
    """
    Returns:
        _Systems
    """
    self.button_systems.click()
    return _Systems(self._driver)

  def select_processes(self):
    """
    Returns:
        _Processes
    """
    self.button_processes.click()
    return _Processes(self._driver)

  def select_data_assets(self):
    """
    Returns:
        _DataAssets
    """
    self.button_data_assets.click()
    return _DataAssets(self._driver)

  def select_products(self):
    """
    Returns:
        _Products
    """
    self.button_products.click()
    return _Products(self._driver)

  def select_projects(self):
    """
    Returns:
        _Projects
    """
    self.button_projects.click()
    return _Projects(self._driver)

  def select_facilities(self):
    """
    Returns:
        _Facilities
    """
    self.button_facilities.click()
    return _Facilities(self._driver)

  def select_markets(self):
    """
    Returns:
        _Markets
    """
    self.button_markets.click()
    return _Markets(self._driver)


class _Systems(lhn.AccordionGroup):
  """Systems dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_SYSTEM
  _locator_spinny = locator.LhnMenu.SPINNY_SYSTEMS


class _Processes(lhn.AccordionGroup):
  """Processes dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_PROCESS
  _locator_spinny = locator.LhnMenu.SPINNY_PROCESSES


class _DataAssets(lhn.AccordionGroup):
  """Data assets dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_DATA_ASSET
  _locator_spinny = locator.LhnMenu.SPINNY_DATA_ASSETS


class _Products(lhn.AccordionGroup):
  """Products dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_PRODUCT
  _locator_spinny = locator.LhnMenu.SPINNY_PRODUCTS


class _Projects(lhn.AccordionGroup):
  """Projects dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_PROJECT
  _locator_spinny = locator.LhnMenu.SPINNY_PROJECTS


class _Facilities(lhn.AccordionGroup):
  """Facilities dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_FACILITY
  _locator_spinny = locator.LhnMenu.SPINNY_FACILITIES


class _Markets(lhn.AccordionGroup):
  """Markets dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_MARKET
  _locator_spinny = locator.LhnMenu.SPINNY_MARKETS


class _RisksOrThreats(lhn.DropdownStatic):
  """Risks or threats dropdown in LHN"""

  _locator_element = locator.LhnMenu.RISK_OR_THREATS

  def __init__(self, driver):
    super(_RisksOrThreats, self).__init__(driver)
    self.button_risks = lhn.Button(
        self._driver,
        locator.LhnMenu.RISKS,
        locator.LhnMenu.RISKS_COUNT
    )
    self.button_threats = lhn.Button(
        self._driver,
        locator.LhnMenu.THREATS,
        locator.LhnMenu.THREATS_COUNT
    )

  def select_risks(self):
    """
    Returns:
        _Risks
    """
    self.button_risks.click()
    return _Risks(self._driver)

  def select_threats(self):
    """
    Returns:
        _Threats
    """
    self.button_threats.click()
    return _Threats(self._driver)


class _Risks(lhn.AccordionGroup):
  """Risks dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.BUTTON_CREATE_RISK
  _locator_spinny = locator.LhnMenu.SPINNY_RISKS


class _Threats(lhn.AccordionGroup):
  """Threats dropdown in LHN"""

  _locator_button_create_new = locator.LhnMenu.THREATS
  _locator_spinny = locator.LhnMenu.SPINNY_THREATS


class LhnContents(base.Component):
  """Model for the highest level contents in LHN"""

  def __init__(self, driver):
    super(LhnContents, self).__init__(driver)
    self.filter = None
    self.button_programs = None
    self.button_workflows = None
    self.button_audits = None
    self.button_assessments = None
    self.button_requests = None
    self.button_issues = None
    self.button_directives = None
    self.button_controls_or_objectives = None
    self.button_people_or_groups = None
    self.button_assets_or_business = None
    self.button_risks_or_threats = None

    self.reload_elements()

  def reload_elements(self):
    """Each dropdown in LHN has a count of members in brackets which we
    update."""
    self.filter = base.Filter(
        self._driver,
        locator.LhnMenu.FILTER_TEXT_BOX,
        locator.LhnMenu.FILTER_SUBMIT_BUTTON,
        locator.LhnMenu.FILTER_CLEAR_BUTTON)
    self.button_programs = lhn.Button(
        self._driver,
        locator.LhnMenu.PROGRAMS,
        locator.LhnMenu.PROGRAMS_COUNT)
    self.button_workflows = lhn.Button(
        self._driver,
        locator.LhnMenu.WORKFLOWS,
        locator.LhnMenu.WORKFLOWS_COUNT)
    self.button_audits = lhn.Button(
        self._driver,
        locator.LhnMenu.AUDITS,
        locator.LhnMenu.AUDITS_COUNT)
    self.button_assessments = lhn.Button(
        self._driver,
        locator.LhnMenu.ASSESSMENTS,
        locator.LhnMenu.ASSESSMENTS_COUNT)
    self.button_requests = lhn.Button(
        self._driver,
        locator.LhnMenu.REQUESTS,
        locator.LhnMenu.REQUESTS_COUNT)
    self.button_issues = lhn.Button(
        self._driver,
        locator.LhnMenu.ISSUES,
        locator.LhnMenu.ISSUES_COUNT)
    self.button_directives = base.Button(
        self._driver,
        locator.LhnMenu.DIRECTIVES)
    self.button_controls_or_objectives = base.Button(
        self._driver,
        locator.LhnMenu.CONTROLS_OR_OBJECTIVES)
    self.button_people_or_groups = base.Button(
        self._driver,
        locator.LhnMenu.PEOPLE_OR_GROUPS)
    self.button_assets_or_business = base.Button(
        self._driver,
        locator.LhnMenu.ASSETS_OR_BUSINESS)
    self.button_risks_or_threats = base.Button(
        self._driver,
        locator.LhnMenu.RISK_OR_THREATS)

  def filter_query(self, query):
    self.filter.filter_query(query)

  def submit_query(self):
    self.filter.submit_query()
    self.reload_elements()

  def select_programs(self):
    """
    Returns:
        _Programs
    """
    self.button_programs.click()
    return _Programs(self._driver)

  def select_workflows(self):
    """
    Returns:
        _Workflows
    """
    self.button_workflows.click()
    return _Workflows(self._driver)

  def select_audits(self):
    """
    Returns:
        _Audits
    """
    self.button_audits.click()
    return _Audits(self._driver)

  def select_assessments(self):
    """
    Returns:
        _Assessments
    """
    self.button_assessments.click()
    return _Assessments(self._driver)

  def select_requests(self):
    """
    Returns:
        _Requests
    """
    self.button_requests.click()
    return _Requests(self._driver)

  def select_issues(self):
    """
    Returns:
        _Issues
    """
    self.button_issues.click()
    return _Issues(self._driver)

  def select_directives(self):
    """
    Returns:
        _Directives
    """
    self.button_directives.click()
    return _Directives(self._driver)

  def select_controls_or_objectives(self):
    """
    Returns:
        _ControlsOrObjectives
    """
    self.button_controls_or_objectives.click()
    return _ControlsOrObjectives(self._driver)

  def select_people_or_groups(self):
    """
    Returns:
        _PeopleOrGroups
    """
    self.button_people_or_groups.click()
    return _PeopleOrGroups(self._driver)

  def select_assests_or_business(self):
    """
    Returns:
        _AssetsOrBusiness
    """
    self.button_assets_or_business.click()
    return _AssetsOrBusiness(self._driver)

  def select_risks_or_threats(self):
    """
    Returns:
        _RisksOrThreats
    """
    self.button_risks_or_threats.click()
    return _RisksOrThreats(self._driver)


class Menu(base.AnimatedComponent):
  """Model of the LHN menu"""

  def __init__(self, driver):
    super(Menu, self).__init__(
        driver,
        [lhn.MyObjectsTab.locator_element,
         lhn.AllObjectsTab.locator_element],
        wait_until_visible=True,
    )
    self.my_objects = lhn.MyObjectsTab(driver)
    self.all_objects = lhn.AllObjectsTab(driver)

  def select_my_objects(self):
    """In LHN selects the tab "My Objects"

    Returns:
        LhnContents
    """
    self.my_objects.click()
    self.all_objects.is_activated = False
    return LhnContents(self._driver)

  def select_all_objects(self):
    """ In LHN selects the tab "All Objects"

    Returns:
        LhnContents
    """
    self.all_objects.click()
    self.my_objects.is_activated = False
    return LhnContents(self._driver)
