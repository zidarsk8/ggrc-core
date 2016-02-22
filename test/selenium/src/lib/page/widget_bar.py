# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Widget bar models. We have multiple models for the widget bar since each
object can have it's own rules what is mappable to it"""

from lib import base
from lib import selenium_utils
from lib.page import widget
from lib.element import widget_bar
from lib.constants import locator


class _WidgetBar(base.Component):
  """Root class for all widget bars"""

  def __init__(self, driver):
    super(_WidgetBar, self).__init__(driver)

  def get_active_widget_name(self):
    """In general multiple tabs are open. Here we get the name of the
    active one.

    Returns:
         str
    """
    active_widget = base.Button(self._driver, locator.WidgetBar.TAB_WIDGET)
    return active_widget.text


class _ObjectWidgetBar(_WidgetBar):
  """Model for a generic object widget bar (e.g. each info widget is object
  specific"""

  _info_cls = None

  def __init__(self, driver):
    super(_ObjectWidgetBar, self).__init__(driver)
    self.button_add_widget = base.Dropdown(driver,
                                           locator.WidgetBar.BUTTON_ADD)
    self.tab_info = base.Tab(self._driver, locator.WidgetBar.INFO)
    self.tab_controls = None

  def add_widget(self):
    """
    Returns:
        widget.AddWidget
    """
    self.button_add_widget.click()
    return widget.AddWidget(self._driver)

  def select_info(self):
    """Selects the info widget/tab. Note that each object has a different info
    page"""
    self.tab_info.click()
    return self._info_cls(self._driver)

  def select_controls(self):
    """
    Returns:
        widget.Controls
    """
    self.tab_controls = base.Tab(self._driver, locator.WidgetBar.CONTROLS)\
        .click()
    return widget.Controls(self._driver)


class AdminDashboardWidgetBarPage(_WidgetBar):
  """A model representing widget bar as seen only on admin dashboard"""

  def __init__(self, driver):
    super(AdminDashboardWidgetBarPage, self).__init__(driver)
    self.tab_people = widget_bar.Tab(self._driver,
                                     locator.WidgetBar.ADMIN_PEOPLE)
    self.tab_roles = widget_bar.Tab(self._driver,
                                    locator.WidgetBar.ADMIN_ROLES)
    self.tab_events = widget_bar.Tab(self._driver,
                                     locator.WidgetBar.ADMIN_EVENTS)
    self.tab_custom_attributes = widget_bar.Tab(
        self._driver, locator.WidgetBar.ADMIN_CUSTOM_ATTRIBUTE)

  def select_people(self):
    """
    Returns:
        widget.AdminPeople
    """
    self.tab_people.click()
    return widget.AdminPeople(self._driver)

  def select_roles(self):
    """
    Returns:
        widget.AdminRoles
    """
    self.tab_roles.click()

    # wait until elements are loaded
    selenium_utils.get_when_visible(
        self._driver, locator.AdminRolesWidget.ROLE_EDITOR)
    return widget.AdminRoles(self._driver)

  def select_events(self):
    """
    Returns:
        widget.AdminPeople
    """
    self.tab_events.click()
    return widget.AdminEvents(self._driver)

  def select_custom_attributes(self):
    """
    Returns:
        widget.AdminCustomAttributes
    """
    self.tab_custom_attributes.click()
    return widget.AdminCustomAttributes(self._driver)


class DashboardWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar on user's dashboard"""

  _info_cls = widget.DashboardInfo


class ProgramWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the program object"""

  _info_cls = widget.ProgramInfo


class WorkflowsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the workflow object"""

  _info_cls = widget.WorkflowInfo


class AuditsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the audit object"""

  _info_cls = widget.AuditInfo


class AssessmentsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the Assessments object"""

  _info_cls = widget.AssessmentsInfo


class RequestsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the requests object"""

  _info_cls = widget.RequestsInfo


class IssueWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the workflow object"""

  _info_cls = widget.IssuesInfo


class RegulationsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the regulations object"""

  _info_cls = widget.RegulationsInfo


class PoliciesWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the policies object"""

  _info_cls = widget.PoliciesInfo


class StandardsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the standards object"""

  _info_cls = widget.StandardsInfo


class ContractsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the contract object"""

  _info_cls = widget.ContractsInfo


class ClausesWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the clauses object"""

  _info_cls = widget.ClausesInfo


class SectionsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the section object"""

  _info_cls = widget.SectionsInfo


class ControlsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the controls object"""

  _info_cls = widget.ContractsInfo


class ObjectivesWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the objectives object"""

  _info_cls = widget.ObjectivesInfo


class PeopleWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the people object"""

  _info_cls = widget.PeopleInfo


class OrgGroupsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the OrgGroups object"""

  _info_cls = widget.OrgGroupsInfo


class VendorsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the vendors object"""

  _info_cls = widget.VendorsInfo


class AccessGroupsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the access group object"""

  _info_cls = widget.AccessGroupInfo


class SystemsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the system object"""

  _info_cls = widget.SystemInfo


class ProcessesWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the process object"""

  _info_cls = widget.ProcessInfo


class DataAssetsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the data asset object"""

  _info_cls = widget.DataAssetInfo


class ProductsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the product object"""

  _info_cls = widget.ProductInfo


class ProjectsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the project object"""

  _info_cls = widget.ProjectInfo


class FacilitiesWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the facility object"""

  _info_cls = widget.FacilityInfo


class MarketsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the market object"""

  _info_cls = widget.MarketInfo


class RisksWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the risk object"""

  _info_cls = widget.RiskInfo


class ThreatsWidgetBarPage(_ObjectWidgetBar):
  """A model representing widget bar of the threat object"""

  _info_cls = widget.ThreatInfo
