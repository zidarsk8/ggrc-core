# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Locators for all the elements"""
# pylint: disable=too-few-public-methods

from selenium.webdriver.common.by import By   # pylint: disable=import-error


class Login(object):
  """All locators for the login page"""

  BUTTON_LOGIN = (By.CSS_SELECTOR, "a.btn.btn-large.btn-info")


class PageHeader(object):
  """All locators for the dashboard header (has the same name as the elemnt"""

  TOGGLE_LHN = (By.CSS_SELECTOR, ".lhn-trigger")
  BUTTON_DASHBOARD = (By.CSS_SELECTOR, '.header-content .to-my-work['
                                       'href="/dashboard"]')
  BUTTON_SEARCH = (By.CSS_SELECTOR, '.header-content ['
                                    'data-toggle="unified-search"]')
  BUTTON_MY_TASKS = (By.CSS_SELECTOR, '.header-content ['
                                      'href="/dashboard#task_widget"]')
  BUTTON_ALL_OBJECTS = (By.CSS_SELECTOR, '.header-content ['
                                         'href="/objectBrowser"]')
  TOGGLE_USER_DROPDOWN = (
      By.CSS_SELECTOR, '.header-content .dropdown-toggle')
  BUTTON_HELP = (By.CSS_SELECTOR, '.header-content [id="#page-help"]')

  # dropdown toggle
  BUTTON_ADMIN_DASHBOARD = (
      By.CSS_SELECTOR, '.dropdown-menu [href="/admin#people_list_widget"]')
  BUTTON_MY_WORK = (By.CSS_SELECTOR, '.dropdown-menu [href="/dashboard"]')
  BUTTON_DATA_IMPORT = (By.CSS_SELECTOR, '.dropdown-menu [href="/import"]')
  BUTTON_DATA_EXPORT = (By.CSS_SELECTOR, '.dropdown-menu [href="/export"]')
  BUTTON_LOGOUT = (By.CSS_SELECTOR, '.dropdown-menu [href="/logout"]')
  NOTIFICATIONS = (By.CSS_SELECTOR, '.menu .user-dropdown .notify-wrap')
  CHECKBOX_DAILY_DIGEST = (By.CSS_SELECTOR, '.menu .user-dropdown input')
  CHECKBOX_DISABLED = (By.CSS_SELECTOR, '.menu .user-dropdown input.disabled')


class Dashboard(object):
  """Locators for the dashbord page"""

  BUTTON_START_NEW_PROGRAM = (
      By.CSS_SELECTOR, '.quick-list [data-object-singular="Program"]')
  BUTTON_START_NEW_AUDIT = (
      By.CSS_SELECTOR, '.quick-list [data-object-singular="Audit"]')
  BUTTON_START_NEW_WORKFLOW = (
      By.CSS_SELECTOR, '.quick-list [data-object-singular="Workflow"]')
  BUTTON_CREATE_NEW_OBJECT = (
      By.CSS_SELECTOR, '.quick-list [href="#"]')
  BUTTON_ALL_OBJECTS = (By.CSS_SELECTOR, '.quick-list '
                                         '[href="/objectBrowser"]')


class LhnMenu(object):
  """Locators for the menu in header"""

  LHN_MENU = (By.ID, "lhn")
  MODAL = (By.CSS_SELECTOR, '[id="ajax-lhn_modal-javascript:--"]')
  EXTENDED_INFO = (By.CSS_SELECTOR, '.extended-info.in')

  FILTER = (By.CSS_SELECTOR, '.lhs-search')
  FILTER_TEXT_BOX = (By.CSS_SELECTOR, '.lhs-search>.widgetsearch')
  FILTER_SUBMIT_BUTTON = (
      By.CSS_SELECTOR, '.lhs-search>.widgetsearch-submit')
  FILTER_CLEAR_BUTTON = (
      By.CSS_SELECTOR, '.lhs-search [data-title="Clear filters"]')

  LHS_ITEM = (By.CSS_SELECTOR, '[test-data-id="lhs-item_3ad27b8b"]')
  ALL_OBJECTS = (By.CSS_SELECTOR, '[data-test-id="all_objects_e0345ec4"]')
  MY_OBJECTS = (By.CSS_SELECTOR, '[data-test-id="my_objects_6fa95ae1"]')
  PIN = (By.CSS_SELECTOR, '.lhn-pin')

  # lhn items
  PROGRAMS = (By.CSS_SELECTOR, '[data-model-name="Program"]>a')
  WORKFLOWS = (By.CSS_SELECTOR, '[data-model-name="Workflow"]>a')
  AUDITS = (By.CSS_SELECTOR, '[data-model-name="Audit"]>a')
  ASSESSMENTS = (By.CSS_SELECTOR,
                 '[data-model-name="Assessment"]>a')
  REQUESTS = (By.CSS_SELECTOR, '[data-model-name="Request"]>a')
  ISSUES = (By.CSS_SELECTOR, '[data-model-name="Issue"]>a')
  DIRECTIVES = (By.CSS_SELECTOR, '[data-test-id="directives_66116337"]')
  REGULATIONS = (By.CSS_SELECTOR,
                 '[data-model-name="Regulation"]>a')
  POLICIES = (By.CSS_SELECTOR, '[data-model-name="Policy"]>a')
  STANDARDS = (By.CSS_SELECTOR, '[data-model-name="Standard"]>a')
  CONTRACTS = (By.CSS_SELECTOR, '[data-model-name="Contract"]>a')
  CLAUSES = (By.CSS_SELECTOR, '[data-model-name="Clause"]>a')
  SECTIONS = (By.CSS_SELECTOR, '[data-model-name="Section"]>a')
  CONTROLS_OR_OBJECTIVES = (By.CSS_SELECTOR,
                            '[data-test-id="controls/objectives_66116337"]')
  CONTROLS = (By.CSS_SELECTOR, '[data-model-name="Control"]>a')
  OBJECTIVES = (By.CSS_SELECTOR, '[data-model-name="Objective"]>a')
  PEOPLE_OR_GROUPS = (By.CSS_SELECTOR,
                      '[data-test-id="people/groups_66116337"]')
  PEOPLE = (By.CSS_SELECTOR, '[data-model-name="Person"]>a')
  ORG_GROUPS = (By.CSS_SELECTOR, '[data-model-name="OrgGroup"]>a')
  ASSETS_OR_BUSINESS = (By.CSS_SELECTOR,
                        '[data-test-id="assets/business_66116337"]')
  SYSTEMS = (By.CSS_SELECTOR, '[data-model-name="System"]>a')
  PROCESSES = (By.CSS_SELECTOR, '[data-model-name="Process"]>a')
  DATA_ASSETS = (By.CSS_SELECTOR, '[data-model-name="DataAsset"]>a')
  ACCESS_GROUPS = (By.CSS_SELECTOR, '[data-model-name="AccessGroup"]>a')
  VENDORS = (By.CSS_SELECTOR, '[data-model-name="Vendor"]>a')
  PRODUCTS = (By.CSS_SELECTOR, '[data-model-name="Product"]>a')
  PROJECTS = (By.CSS_SELECTOR, '[data-model-name="Project"]>a')
  RISK_OR_THREATS = (By.CSS_SELECTOR,
                     '[data-test-id="risk/threats_66116337"]')
  RISKS = (By.CSS_SELECTOR, '[data-model-name="Risk"]>a')
  FACILITIES = (By.CSS_SELECTOR, '[data-model-name="Facility"]>a')
  MARKETS = (By.CSS_SELECTOR, '[data-model-name="Market"]>a')
  THREATS = (By.CSS_SELECTOR, '[data-model-name="Threat"]>a')

  # buttons create new lhn_modal
  BUTTON_CREATE_NEW_PROGRAM = (
      By.CSS_SELECTOR,
      '[data-model-name="Program"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_NEW_WORKFLOW = (
      By.CSS_SELECTOR,
      '[data-model-name="Workflow"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_NEW_AUDIT = (
      By.CSS_SELECTOR,
      '[data-model-name="Audit"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_NEW_CONTROL_ASSESSMENT = (
      By.CSS_SELECTOR,
      '[data-model-name="ControlAssessment"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_NEW_REQUEST = (
      By.CSS_SELECTOR,
      '[data-model-name="Request"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_ISSUE = (
      By.CSS_SELECTOR,
      '[data-model-name="Issue"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_REGULATION = (
      By.CSS_SELECTOR,
      '[data-model-name="Regulation"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_POLICY = (
      By.CSS_SELECTOR,
      '[data-model-name="Policy"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_STANDARD = (
      By.CSS_SELECTOR,
      '[data-model-name="Standard"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_CONTRACT = (
      By.CSS_SELECTOR,
      '[data-model-name="Contract"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_CLAUSE = (
      By.CSS_SELECTOR,
      '[data-model-name="Clause"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_SECTION = (
      By.CSS_SELECTOR,
      '[data-model-name="Section"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_CONTROL = (
      By.CSS_SELECTOR,
      '[data-model-name="Control"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_OBJECTIVE = (
      By.CSS_SELECTOR,
      '[data-model-name="Objective"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_PERSON = (
      By.CSS_SELECTOR,
      '[data-model-name="Person"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_ORG_GROUP = (
      By.CSS_SELECTOR,
      '[data-model-name="OrgGroup"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_VENDOR = (
      By.CSS_SELECTOR,
      '[data-model-name="Vendor"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_ACCESS_GROUP = (
      By.CSS_SELECTOR,
      '[data-model-name="AccessGroup"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_SYSTEM = (
      By.CSS_SELECTOR,
      '[data-model-name="System"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_PROCESS = (
      By.CSS_SELECTOR,
      '[data-model-name="Process"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_DATA_ASSET = (
      By.CSS_SELECTOR,
      '[data-model-name="DataAsset"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_PRODUCT = (
      By.CSS_SELECTOR,
      '[data-model-name="Product"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_PROJECT = (
      By.CSS_SELECTOR,
      '[data-model-name="Project"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_FACILITY = (
      By.CSS_SELECTOR,
      '[data-model-name="Facility"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_MARKET = (
      By.CSS_SELECTOR,
      '[data-model-name="Market"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_RISK = (
      By.CSS_SELECTOR,
      '[data-model-name="Risk"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')
  BUTTON_CREATE_THREAT = (
      By.CSS_SELECTOR,
      '[data-model-name="Threat"] ['
      'data-test-id="button_lhn_create_new_program_522c563f"]')

  # count locators
  PROGRAMS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Program"] '
                                     '.item-count')
  WORKFLOWS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Workflow"] '
                                      '.item-count')
  AUDITS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Audit"] .item-count')
  ASSESSMENTS_COUNT = (By.CSS_SELECTOR,
                       '[data-model-name="Assessment"] .item-count')
  ISSUES_COUNT = (By.CSS_SELECTOR, '[data-model-name="Issue"] .item-count')
  REQUESTS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Request"] '
                                     '.item-count')
  REGULATIONS_COUNT = (By.CSS_SELECTOR,
                       '[data-model-name="Regulation"] .item-count')
  POLICIES_COUNT = (By.CSS_SELECTOR,
                    '[data-model-name="Policy"] .item-count')
  STANDARDS_COUNT = (By.CSS_SELECTOR,
                     '[data-model-name="Standard"] .item-count')
  CONTRACTS_COUNT = (By.CSS_SELECTOR,
                     '[data-model-name="Clause"] .item-count')
  CLAUSES_COUNT = (By.CSS_SELECTOR,
                   '[data-model-name="Regulation"] .item-count')
  SECTIONS_COUNT = (By.CSS_SELECTOR,
                    '[data-model-name="Section"] .item-count')
  CONTROL_COUNT = (
      By.CSS_SELECTOR, '[data-model-name="Control"] .item-count')
  OBJECTIVES_COUNT = (By.CSS_SELECTOR, '[data-model-name="Objective"] '
                                       '.item-count')
  PEOPLE_COUNT = (By.CSS_SELECTOR, '[data-model-name="Person"] .item-count')
  ORG_GROUPS_COUNT = (By.CSS_SELECTOR, '[data-model-name="OrgGroup"] '
                                       '.item-count')
  VENDORS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Vendor"] .item-count')
  ACCESS_GROUPS_COUNT = (By.CSS_SELECTOR, '[data-model-name="AccessGroup"] '
                                          '.item-count')
  SYSTEMS_COUNT = (By.CSS_SELECTOR, '[data-model-name="System"] .item-count')
  PROCESSES_COUNT = (By.CSS_SELECTOR, '[data-model-name="Process"] '
                                      '.item-count')
  DATA_ASSETS_COUNT = (By.CSS_SELECTOR, '[data-model-name="DataAsset"] '
                                        '.item-count')
  PRODUCTS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Product"] '
                                     '.item-count')
  PROJECTS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Project"] '
                                     '.item-count')
  FACILITIES_COUNT = (By.CSS_SELECTOR, '[data-model-name="Facility"] '
                                       '.item-count')
  MARKETS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Market"] .item-count')
  RISKS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Risk"] .item-count')
  THREATS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Threat"] .item-count')

  # workflows labels
  WORKFLOWS_ACTIVE = (By.CSS_SELECTOR, '[data-for="Workflow"]>['
                                       'data-value="Active"]')
  WORKFLOWS_DRAFT = (By.CSS_SELECTOR, '[data-for="Workflow"]>['
                                      'data-value="Draft"]')
  WORKFLOWS_INACTIVE = (By.CSS_SELECTOR, '[data-for="Workflow"]>['
                                         'data-value="Inactive"]')

  # spinny
  SPINNY_PROGRAMS = (By.CSS_SELECTOR, '[data-model-name="Program"] .spinny')
  SPINNY_WORKFLOWS = (
      By.CSS_SELECTOR, '[data-model-name="Workflow"] .spinny')
  SPINNY_AUDITS = (By.CSS_SELECTOR, '[data-model-name="Audit"] .spinny')
  SPINNY_CONTROL_ASSESSMENTS = (
      By.CSS_SELECTOR, '[data-model-name="ControlAssessment"] .spinny')
  SPINNY_REQUESTS = (By.CSS_SELECTOR, '[data-model-name="Request"] .spinny')
  SPINNY_ISSUES = (By.CSS_SELECTOR, '[data-model-name="Issue"] .spinny')
  SPINNY_REGULATIONS = (
      By.CSS_SELECTOR, '[data-model-name="Regulation"] .spinny')
  SPINNY_POLICIES = (By.CSS_SELECTOR, '[data-model-name="Policy"] .spinny')
  SPINNY_STANDARDS = (
      By.CSS_SELECTOR, '[data-model-name="Standard"] .spinny')
  SPINNY_CONTRACTS = (
      By.CSS_SELECTOR, '[data-model-name="Contract"] .spinny')
  SPINNY_CLAUSES = (By.CSS_SELECTOR, '[data-model-name="Clause"] .spinny')
  SPINNY_SECTIONS = (By.CSS_SELECTOR, '[data-model-name="Section"] .spinny')
  SPINNY_CONTROLS = (By.CSS_SELECTOR, '[data-model-name="Control"] .spinny')
  SPINNY_OBJECTIVES = (
      By.CSS_SELECTOR, '[data-model-name="Objective"] .spinny')
  SPINNY_PEOPLE = (By.CSS_SELECTOR, '[data-model-name="Person"] .spinny')
  SPINNY_ORG_GROUPS = (
      By.CSS_SELECTOR, '[data-model-name="OrgGroup"] .spinny')
  SPINNY_VENDORS = (By.CSS_SELECTOR, '[data-model-name="Vendor"] .spinny')
  SPINNY_ACCESS_GROUPS = (
      By.CSS_SELECTOR, '[data-model-name="AccessGroup"] .spinny')
  SPINNY_SYSTEMS = (By.CSS_SELECTOR, '[data-model-name="System"] .spinny')
  SPINNY_PROCESSES = (By.CSS_SELECTOR, '[data-model-name="Process"] .spinny')
  SPINNY_DATA_ASSETS = (
      By.CSS_SELECTOR, '[data-model-name="DataAsset"] .spinny')
  SPINNY_PRODUCTS = (By.CSS_SELECTOR, '[data-model-name="Product"] .spinny')
  SPINNY_PROJECTS = (By.CSS_SELECTOR, '[data-model-name="Project"] .spinny')
  SPINNY_FACILITIES = (
      By.CSS_SELECTOR, '[data-model-name="Facility"] .spinny')
  SPINNY_MARKETS = (By.CSS_SELECTOR, '[data-model-name="Market"] .spinny')
  SPINNY_RISKS = (By.CSS_SELECTOR, '[data-model-name="Risk"] .spinny')
  SPINNY_THREATS = (By.CSS_SELECTOR, '[data-model-name="Threat"] .spinny')

  # accordeon members
  ACCORDEON_PROGRAMS_MEMBERS = (
      By.CSS_SELECTOR, '[data-model-name="Program"]>.content>.sub-level>li')
  ACCORDEON_REQUEST_MEMBERS = (
      By.CSS_SELECTOR, '[data-model-name="Request"]>.content>.sub-level>li')
  ACCORDEON_ISSUE_MEMBERS = (
      By.CSS_SELECTOR, '[data-model-name="Issue"]>.content>.sub-level>li')
  ACCORDEON_CONTROLS_MEMBERS = (
      By.CSS_SELECTOR, '[data-model-name="Control"]>.content>.sub-level>li')
  ACCORDEON_ORG_GROUP_MEMBERS = (
      By.CSS_SELECTOR, '[data-model-name="OrgGroup"]>.content>.sub-level>li')
  ACCORDEON_RISK_MEMBERS = (
      By.CSS_SELECTOR, '[data-model-name="Risk"]>.content>.sub-level>li')
  ACCORDEON_PROCESS_MEMBERS = (
      By.CSS_SELECTOR, '[data-model-name="Process"]>.content>.sub-level>li')
  ACCORDEON_DATA_ASSET_MEMBERS = (
      By.CSS_SELECTOR, '[data-model-name="DataAsset"]>.content>.sub-level>li')
  ACCORDEON_SYSTEM_MEMBERS = (
      By.CSS_SELECTOR, '[data-model-name="System"]>.content>.sub-level>li')
  ACCORDEON_PRODUCT_MEMBERS = (
      By.CSS_SELECTOR, '[data-model-name="Product"]>.content>.sub-level>li')
  ACCORDEON_PROJECT_MEMBERS = (
      By.CSS_SELECTOR, '[data-model-name="Project"]>.content>.sub-level>li')


class ExtendedInfo(object):
  """Locators for the extended info tooltip in LHN after hovering over a
  member object"""

  BUTTON_MAP_TO = (By.CSS_SELECTOR, '.extended-info.in .map-to-page-object')
  ALREADY_MAPPED = (
      By.CSS_SELECTOR,
      '.extended-info.in .links .primary:not(.map-to-page-object)')


class ModalCreateNewProgram(object):
  """Locators for the program modal visible when creating a new modal from
  LHN"""

  UI_TITLE = (By.CSS_SELECTOR,
              '[data-test-id="new_program_field_title_a63ed79d"]')
  UI_DESCRIPTION = (By.CSS_SELECTOR,
                    '[data-test-id="new_program_field_description_1fb8bc06"]'
                    '>iframe.wysihtml5-sandbox')
  UI_NOTES = (By.CSS_SELECTOR,
              '[data-test-id="new_program_field_notes_75b8bc05"]'
              '>iframe.wysihtml5-sandbox')
  UI_CODE = (By.CSS_SELECTOR,
             '[data-test-id="new_program_field_code_334276e2"]')
  UI_STATE = (By.CSS_SELECTOR,
              '[data-test-id="new_program_dropdown_state_036a1fa6"]')
  BUTTON_HIDE_OPTIONAL_FIELDS = (By.ID, "formHide")
  BUTTON_SHOW_ALL_OPTIONAL_FIELDS = (By.ID, "formHide")
  UI_PRIMARY_CONTACT = (By.CSS_SELECTOR, '[data-test-id='
                                         '"new_program_field_primary_contact_'
                                         '86160053"]')
  DROPDOWN_CONTACT = (By.CSS_SELECTOR, '.ui-menu-item')
  UI_SECONDARY_CONTACT = (By.CSS_SELECTOR, '[data-test-id='
                                           '"new_program_field_secondary_'
                                           'contact_'
                                           '86160053"]')

  UI_PROGRAM_URL = (By.CSS_SELECTOR, '[data-test-id='
                                     '"new_program_field_program_url_'
                                     '86160053"]')
  UI_REFERENCE_URL = (By.CSS_SELECTOR, '[data-test-id='
                                       '"new_program_field_reference_url_'
                                       '86160053"]')
  UI_EFFECTIVE_DATE = (By.CSS_SELECTOR, '[data-test-id='
                                        '"new_program_field_effective_date_'
                                        'f2783a28"]')
  UI_STOP_DATE = (By.CSS_SELECTOR, '[data-test-id='
                                   '"new_program_field_stop_date_f2783a28"]')
  DATE_PICKER = (By.CSS_SELECTOR, '.ui-datepicker-calendar ['
                                  'data-handler="selectDay"]')
  TITLE = (By.CSS_SELECTOR, '[data-test-id="label_title_2c925d94"]')
  DESCRIPTION = (By.CSS_SELECTOR,
                 '[data-test-id="label_description_2c925d94"]')

  PRIVACY = (By.CSS_SELECTOR, '[data-test-id="label_privacy_2c925d94"]')
  PROGRAM_URL = (By.CSS_SELECTOR,
                 '[data-test-id="label_program_url_2c925d94"]')


class ModalCreateNewOrgGroup(object):
  """Locators for the control modal visible when creating a new modal from
  LHN"""

  # labels
  MODAL_TITLE = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]>div>h2')
  TITLE = (By.CSS_SELECTOR, '.modal-body form>div:nth-child(2) .span6>label')

  # user input elements
  UI_TITLE = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(2) .span6>input')


class ModalCreateNewRisk(object):
  """Locators for the control modal visible when creating a new modal from
  LHN"""

  # labels
  MODAL_TITLE = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]>div>h2')
  TITLE = (By.CSS_SELECTOR, '.modal-body form>div:nth-child(2) .span6>label')

  # user input elements
  UI_TITLE = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(2) .span6>input')
  UI_DESCRIPTION = (
      By.CSS_SELECTOR, '.modal-body form>div:nth-child(3) iframe')


class ModalCreateRequest(object):
  """Locators for the control modal visible when creating a new modal from
  LHN"""

  # labels
  MODAL_TITLE = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]>div>h2')
  TITLE = (By.CSS_SELECTOR, '.modal-body form>div:nth-child(2) .span6>label')

  # user input elements
  UI_TITLE = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(2) .span6>input')


class ModalCreateNewDataAsset(object):
  """Locators for the control modal visible when creating a new modal from
  LHN"""

  # labels
  MODAL_TITLE = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]>div>h2')
  TITLE = (By.CSS_SELECTOR, '.modal-body form>div:nth-child(2) .span6>label')

  # user input elements
  UI_TITLE = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(2) .span6>input')


class ModalCreateNewProcess(object):
  """Locators for the control modal visible when creating a new modal from
  LHN"""

  # labels
  MODAL_TITLE = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]>div>h2')
  TITLE = (By.CSS_SELECTOR, '.modal-body form>div:nth-child(2) .span6>label')

  # user input elements
  UI_TITLE = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(2) .span6>input')


class ModalCreateNewProject(object):
  """Locators for the control modal visible when creating a new modal from
  LHN"""

  # labels
  MODAL_TITLE = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]>div>h2')
  TITLE = (By.CSS_SELECTOR, '.modal-body form>div:nth-child(2) .span6>label')

  # user input elements
  UI_TITLE = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(2) .span6>input')


class ModalCreateNewSystem(object):
  """Locators for the control modal visible when creating a new modal from
  LHN"""

  # labels
  MODAL_TITLE = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]>div>h2')
  TITLE = (By.CSS_SELECTOR, '.modal-body form>div:nth-child(2) .span6>label')

  # user input elements
  UI_TITLE = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(2) .span6>input')


class ModalCreateNewProduct(object):
  """Locators for the control modal visible when creating a new modal from
  LHN"""

  # labels
  MODAL_TITLE = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]>div>h2')
  TITLE = (By.CSS_SELECTOR, '.modal-body form>div:nth-child(2) .span6>label')

  # user input elements
  UI_TITLE = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(2) .span6>input')


class ModalCreateNewControl(object):
  """Locators for the control modal visible when creating a new modal from
  LHN"""

  # labels
  MODAL_TITLE = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]>div>h2')
  TITLE = (By.CSS_SELECTOR, '.modal-body form>div:nth-child(2) .span6>label')
  DESCRIPTION = (
      By.CSS_SELECTOR, '.modal-body form>div:nth-child(3) .span6>label')
  TEST_PLAN = (By.CSS_SELECTOR, '[data-id="test_plan_hidden"] label')
  NOTES = (By.CSS_SELECTOR, '[data-id="note_hidden"] label')
  CODE = (By.CSS_SELECTOR, '[data-id="code_hidden"] label')
  KIND_OR_NATURE = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(6) div:nth-child(2) div:nth-child(1) label')
  FRAUD_RELATED = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(6) div:nth-child(2) div:nth-child(2) label')
  EFFECTIVE_DATE = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(3)>div:nth-child(1) label')
  FREQUENCY = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(4) div:nth-child(1) select')
  ASSERTIONS = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(4)>div:nth-child(2) label')
  PRINCIPAL_ASSESSOR = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(5)>div:nth-child(1) label')
  SECONDARY_ASSESSOR = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(5)>div:nth-child(2) label')
  OWNER = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(1)>form>div:nth-child(3) div:nth-child(2) '
      'label')
  PRIMARY_CONTACT = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(1)>form>div:nth-child(4) div:nth-child(2)>'
      'div:nth-child(1)>div>label')
  SECONDARY_CONTACT = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(1)>form>div:nth-child(4) div:nth-child(2)>'
      'div:nth-child(2)>div>label')
  CONTROL_URL = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(5) div:nth-child(2)>div:nth-child(1)>div'
      '>label')
  REFERENCE_URL = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(1)>form>div:nth-child(5) div:nth-child(2)>'
      'div:nth-child(2)>div>label')
  SIGNIFICANCE = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(6) div:nth-child(2) div:nth-child(3) label')
  TYPE_OR_MEANS = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(6) div:nth-child(2) div:nth-child(4) label')
  STOP_DATE = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(6) div:nth-child(3) div:nth-child(2) label')
  CATEGORIES = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(4)>div:nth-child(3) label')
  STATE = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(5)>div:nth-child(3) label')

  # user input elements
  UI_TITLE = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(2) .span6>input')
  UI_DESCRIPTION = (
      By.CSS_SELECTOR, '.modal-body form>div:nth-child(3) iframe')
  UI_TEST_PLAN = (By.CSS_SELECTOR, '[data-id="test_plan_hidden"] iframe')
  UI_NOTES = (By.CSS_SELECTOR, '[data-id="note_hidden"] iframe')
  UI_CODE = (By.CSS_SELECTOR, '[data-id="code_hidden"] input')
  UI_PRIMARY_CONTACT = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(1)>form>div:nth-child(4) div:nth-child(2)>'
      'div:nth-child(1)>div>input')
  UI_SECONDARY_CONTACT = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(1)>form>div:nth-child(4) div:nth-child(2)>'
      'div:nth-child(2)>div>input')
  UI_CONTROL_URL = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(5) div:nth-child(2)>div:nth-child(1)>div'
      '>input')
  UI_REFERENCE_URL = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(1)>form>div:nth-child(5) div:nth-child(2)>'
      'div:nth-child(2)>div>input')

  DATEPICKER_EFFECTIVE_DATE = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(3)>div:nth-child(1) input')
  DATEPICKER_STOP_DATE = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(3)>div:nth-child(2) input')

  # dorpdowns
  DROPDOWN_KIND_OR_NATURE = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(6) div:nth-child(2) div:nth-child(1) select')
  DROPDOWN_FRAUD_RELATED = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(6)>div:nth-child(2)>div:nth-child(2)>select')
  DROPDOWN_SIGNIFICANCE = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(6)>div:nth-child(2)>div:nth-child(3)>select')
  DROPDOWN_TYPE_OR_MEANS = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(6) div:nth-child(2) div:nth-child(4) select')
  DROPDOWN_FREQUENCY = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(4) div:nth-child(1) select')
  DROPDOWN_STATE = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(5)>div:nth-child(3) select')

  SELECTABLE_ASSERTIONS = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(4)>div:nth-child(2) select')
  SELECTABLE_CATEGORIES = (
      By.CSS_SELECTOR,
      '.modal-body div>form>div>div:nth-child(4)>div:nth-child(3) select')

  # buttons
  BUTTON_ADD_OWNER = (By.CSS_SELECTOR, 'isolate-form .btn')
  BUTTON_HIDE_ALL_OPTIONAL_FIELDS = (By.CSS_SELECTOR, '#formHide')


class ModalCreateNewIssue(object):
  """Locators for the issue modal visible when creating a new modal from
  LHN"""

  # labels
  MODAL_TITLE = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]>div>h2')
  TITLE = (By.CSS_SELECTOR, '.modal-body form>div:nth-child(2) .span6>label')

  # user input elements
  UI_TITLE = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(2) .span6>input')


class ModalCreateNewRequest(object):
  """Locators for the request modal visible when creating a new modal from
  LHN"""

  # labels
  MODAL_TITLE = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]>div>h2')
  TITLE = (By.CSS_SELECTOR, '.modal-body form>div:nth-child(2) .span6>label')

  # user input elements
  UI_TITLE = (
      By.CSS_SELECTOR,
      '.modal-body form>div:nth-child(2) .span6>input')


class ModalEditObject(object):
  """Locators for a generic edit object modal"""

  BUTTON_DELETE = (
      By.CSS_SELECTOR, '.deny-buttons [data-toggle="modal-ajax-deleteform"]')


class ModalCreateNewObject(object):
  """Locators for a generic new object modal"""

  UI_TITLE = (By.CSS_SELECTOR, '[data-id="title_txtbx"]')

  BUTTON_SAVE_AND_CLOSE = (
      By.CSS_SELECTOR,
      '.modal-footer .confirm-buttons [data-toggle="modal-submit"]')
  BUTTON_SAVE_AND_ADD_ANOTHER = (
      By.CSS_SELECTOR,
      '.confirm-buttons [data-toggle="modal-submit-addmore"]')


class ModalCustomAttribute(object):
  """Locators for a generic custom attributes modal in admin dashboard"""

  MODAL_TITLE = (By.CSS_SELECTOR, '.modal-header h2')
  ATTRIBUTE_TITLE = (By.CSS_SELECTOR, '.modal-body div:nth-child(1)>label')
  INLINE_HELP = (By.CSS_SELECTOR, '.modal-body div:nth-child(2)>label')
  ATTRIBUTE_TYPE = (By.CSS_SELECTOR, '.modal-header h2')
  PLACEHOLDER = (By.CSS_SELECTOR, '.modal-header h2')
  MANDATORY = (By.CSS_SELECTOR, '.modal-header h2')
  UI_ATTRIBUTE_TITLE = (
      By.CSS_SELECTOR, '.modal-body div:nth-child(1)>input[tabindex="1"]')
  UI_INLINE_HELP = (
      By.CSS_SELECTOR,
      '.modal-body div:nth-child(1)>input[tabindex="4"]')
  UI_PLACEHOLDER = (By.CSS_SELECTOR, '.modal-body div:nth-child(2)>input')
  CHECKBOX_MANDATORY = (By.CSS_SELECTOR, '.modal-body [type="checkbox"]')
  BUTTON_ADD_ANOTHER = (
      By.CSS_SELECTOR,
      '.confirm-buttons [data-toggle="modal-submit-addmore"]')
  BUTTON_SAVE_AND_CLOSE = (
      By.CSS_SELECTOR,
      '.modal-footer .confirm-buttons [data-toggle="modal-submit"]')


class WidgetBar(object):
  """Locators for the bar containing the widgets/tabs"""

  BUTTON_ADD = (By.CSS_SELECTOR,
                '[data-test-id="button_widget_add_2c925d94"]')
  TAB_WIDGET = (By.CSS_SELECTOR, ".object-nav .active")
  ADMIN_PEOPLE = (By.CSS_SELECTOR, '[href="#people_list_widget"]')
  ADMIN_ROLES = (By.CSS_SELECTOR, '[href="#roles_list_widget"]')
  ADMIN_EVENTS = (By.CSS_SELECTOR, '[href="#events_list_widget"]')
  ADMIN_CUSTOM_ATTRIBUTE = (By.CSS_SELECTOR,
                            '[href="#custom_attribute_widget"]')

  INFO = (By.CSS_SELECTOR, '[href="#info_widget"]')
  CUSTOM_ATTRIBUTES = (By.CSS_SELECTOR, '[href="#custom_attribute_widget"]')
  EVENTS = (By.CSS_SELECTOR, '[href="#events_list_widget"]')
  ROLES = (By.CSS_SELECTOR, '[href="#roles_list_widget"]')
  PEOPLE = (By.CSS_SELECTOR, '[href="#person_widget"]')
  MARKETS = (By.CSS_SELECTOR, '[href="#market_widget"]')
  ACCESS_GROUPS = (By.CSS_SELECTOR, '[href="#access_group_widget"]')
  ASSESSMENT = (By.CSS_SELECTOR, '[href="#assessment_widget"]')
  AUDITS = (By.CSS_SELECTOR, '[href="#audit_widget"]')
  CLAUSES = (By.CSS_SELECTOR, '[href="#clause_widget"]')
  CONTRACTS = (By.CSS_SELECTOR, '[href="#contract_widget"]')
  CONTROLS = (By.CSS_SELECTOR, '[href="#control_widget"]')
  DATA_ASSETS = (By.CSS_SELECTOR, '[href="#data_asset_widget"]')
  ISSUES = (By.CSS_SELECTOR, '[href="#issue_widget"]')
  FACILITIES = (By.CSS_SELECTOR, '[href="#facility_widget"]')
  OBJECTIVES = (By.CSS_SELECTOR, '[href="#objective_widget"]')
  ORG_GROUPS = (By.CSS_SELECTOR, '[href="#org_group_widget"]')
  POLICIES = (By.CSS_SELECTOR, '[href="#policy_widget"]')
  PROCESSES = (By.CSS_SELECTOR, '[href="#process_widget"]')
  PRODUCTS = (By.CSS_SELECTOR, '[href="#product_widget"]')
  PROJECTS = (By.CSS_SELECTOR, '[href="#project_widget"]')
  PROGRAMS = (By.CSS_SELECTOR, '[href="#program_widget"]')
  REGULATIONS = (By.CSS_SELECTOR, '[href="#regulation_widget"]')
  REQUESTS = (By.CSS_SELECTOR, '[href="#request_widget"]')
  SECTIONS = (By.CSS_SELECTOR, '[href="#section_widget"]')
  STANDARDS = (By.CSS_SELECTOR, '[href="#standard_widget"]')
  SYSTEMS = (By.CSS_SELECTOR, '[href="#system_widget"]')
  VENDORS = (By.CSS_SELECTOR, '[href="#vendor_widget"]')
  RISKS = (By.CSS_SELECTOR, '[href="#risks_widget"]')
  THREATS = (By.CSS_SELECTOR, '[href="#threats_widget"]')
  RISK_ASSESSMENTS = (By.CSS_SELECTOR, '[href="#risk_assessments_widget"]')
  WORKFLOWS = (By.CSS_SELECTOR, '[href="#workflow_widget"]')
  TASKS = (By.CSS_SELECTOR, '[href="#task_widget"]')


class WidgetBarButtonAddDropdown(object):
  """Locators for the button/dropdown "add widget" in widget bar"""

  AUDITS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                             '[href="#audit_widget"]')
  CONTROLS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                               '[href="#control_widget"]')
  DATA_ASSETS = (By.CSS_SELECTOR,
                 '[data-test-id="button_widget_add_2c925d94"] '
                 '[href="#data_asset_widget"]')
  ISSUES = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                             '[href="#issues_widget"]')
  OBJECTIVES = (By.CSS_SELECTOR,
                '[data-test-id="button_widget_add_2c925d94"] '
                '[href="#objective_widget"]')
  POLICIES = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                               '[href="#policy_widget"]')
  PRODUCTS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                               '[href="#product_widget"]')
  REGULATIONS = (By.CSS_SELECTOR,
                 '[data-test-id="button_widget_add_2c925d94"] '
                 '[href="#regulation_widget"]')
  SYSTEMS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                              '[href="#system_widget"]')
  RISKS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                            '[href="#risk_widget"]')
  WORKFLOWS = (
      By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                       '[href="#workflow_widget"]')
  CONTRACTS = (
      By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                       '[href="#contract_widget"]')
  ASSESSMENTS = (By.CSS_SELECTOR,
                 '[data-test-id="button_widget_add_2c925d94"] '
                 '[href="#assessment_widget"]')
  FACILITIES = (By.CSS_SELECTOR,
                '[data-test-id="button_widget_add_2c925d94"] '
                '[href="#facility_widget"]')
  MARKETS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                              '[href="#market_widget"]')
  ORG_GROUPS = (By.CSS_SELECTOR,
                '[data-test-id="button_widget_add_2c925d94"] '
                '[href="#org_groups_widget"]')
  PROCESSES = (By.CSS_SELECTOR,
               '[data-test-id="button_widget_add_2c925d94"] '
               '[href="#process_widget"]')
  PROJECTS = (By.CSS_SELECTOR,
              '[data-test-id="button_widget_add_2c925d94"] '
              '[href="#project_widget"]')
  STANDARDS = (By.CSS_SELECTOR,
               '[data-test-id="button_widget_add_2c925d94"] '
               '[href="#standard_widget"]')
  VENDORS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                              '[href="#vendor_widget"]')
  THREAD_ACTORS = (By.CSS_SELECTOR,
                   '[data-test-id="button_widget_add_2c925d94"] '
                   '[href="#thread_actors_widget"]')
  WORKFLOW_TASKS = (By.CSS_SELECTOR,
                    '[data-test-id="button_widget_add_2c925d94"] '
                    '[href="#task_widget"]')
  PERSON = (By.CSS_SELECTOR,
            '[data-test-id="button_widget_add_2c925d94"] '
            '[href="#person_widget"]')
  PROGRAM = (By.CSS_SELECTOR,
             '[data-test-id="button_widget_add_2c925d94"] '
             '[href="#program_widget"]')
  ACCESS_GROUP = (By.CSS_SELECTOR,
                  '[data-test-id="button_widget_add_2c925d94"] '
                  '[href="#access_group_widget"]')
  CLAUSE = (By.CSS_SELECTOR,
            '[data-test-id="button_widget_add_2c925d94"] '
            '[href="#clause_widget"]')
  REQUEST = (By.CSS_SELECTOR,
             '[data-test-id="button_widget_add_2c925d94"] '
             '[href="#request_widget"]')
  SECTION = (By.CSS_SELECTOR,
             '[data-test-id="button_widget_add_2c925d94"] '
             '[href="#section_widget"]')
  THREAT = (By.CSS_SELECTOR,
            '[data-test-id="button_widget_add_2c925d94"] '
            '[href="#threat_widget"]')


class ObjectWidget(object):
  """Locators for a generic widget"""

  CONTROL_COLUMN_TITLE = (
      By.CSS_SELECTOR, '.header .span4 .title-heading .widget-col-title')
  CONTROL_OWNER = (
      By.CSS_SELECTOR, '.header .span4 [data-field="contact.name|email"]')
  COTNROL_STATE = (
      By.CSS_SELECTOR, '.header .span4 [data-field="status"]')
  MEMBERS_TITLE_LIST = (
      By.CSS_SELECTOR,
      '.object-area .tree-structure .select .span4:nth-child(1)')
  INFO_PANE = (By.CSS_SELECTOR, '.sticky-info-panel')


class InfoWidget(object):
  """Locators for the info widget"""

  BUTTON_SETTINGS = (By.CSS_SELECTOR, '.info-pane-utility')


class ModalDeleteObject(object):
  MODAL_TITLE = (By.CSS_SELECTOR, '.modal-header>h2')
  CONFIRMATION_TEXT = (By.CSS_SELECTOR, '.modal-body>div>p')
  OBJECT_TITLE = (By.CSS_SELECTOR, '.modal-body>div>p>span')
  BUTTON_DELETE = (
      By.CSS_SELECTOR, '.modal-footer .confirm-buttons>[data-toggle="delete"]')


class ProgramInfoWidget(object):
  """Locators for the info program widget"""

  PERMALINK_ALERT = (By.CSS_SELECTOR, '.content>.flash>.alert-success')

  ALERT_LINK_COPIED = (By.CSS_SELECTOR, '.alert.alert-success')
  MODAL_DELETE = (By.ID, '[id="ajax-lhn_modal-javascript:--"]')
  MODAL_DELETE_CLOSE = (By.CSS_SELECTOR, '.lhn_modal .grcicon-x-grey')

  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')
  OBJECT_REVIEW = (By.CSS_SELECTOR,
                   '[data-test-id="title_review_0ad9fbaf"] h6')
  SUBMIT_FOR_REVIEW = (By.CSS_SELECTOR,
                       '[data-test-id="title_review_0ad9fbaf"] '
                       '[href="javascript://"]')
  DESCRIPTION = (By.CSS_SELECTOR,
                 '[data-test-id="title_description_7a906d2e"] h6')
  DESCRIPTION_ENTERED = (By.CSS_SELECTOR,
                         '[data-test-id="title_description_'
                         'content_7a906d2e"]')
  NOTES = (By.CSS_SELECTOR, '[data-test-id="title_notes_ef5bc3a71e88"] '
                            'h6')
  NOTES_ENTERED = (By.CSS_SELECTOR,
                   '[data-test-id="title_notes_ef5bc3a71e88"]>div')
  MANAGER = (By.CSS_SELECTOR, '[data-test-id="title_manager_7a906d2e"] '
                              'h6')
  MANAGER_ENTERED = (By.CSS_SELECTOR,
                     '[data-test-id="title_manager_7a906d2e"] '
                     '[data-test-id="text_manager_7a906d2e"]')
  PROGRAM_URL = (By.CSS_SELECTOR,
                 '[data-test-id="title_program_url_aa7d1a65"] h6')
  PROGRAM_URL_ENTERED = (By.CSS_SELECTOR,
                         '[data-test-id="text_program_url_aa7d1a65"]')
  REFERENCE_URL = (By.CSS_SELECTOR,
                   '[data-test-id="title_reference_url_aa7d1a65"]')
  REFERENCE_URL_ENTERED = (By.CSS_SELECTOR,
                           '[data-test-id="text_reference_url_aa7d1a65"]')
  TOGGLE_SHOW_ADVANCED = (By.CSS_SELECTOR,
                          '[data-test-id="button_advanced_cf47bc01"]')
  TOGGLE_SHOW_ADVANCED_ACTIVATED = (
      By.CSS_SELECTOR, '[data-test-id="button_advanced_cf47bc01"].active')
  CODE = (By.CSS_SELECTOR, '[data-test-id="title_code_cf47bc01"] h6')
  CODE_ENTERED = (By.CSS_SELECTOR,
                  '[data-test-id="title_code_cf47bc01"] p')
  EFFECTIVE_DATE = (By.CSS_SELECTOR,
                    '[data-test-id="title_effective_date_cf47bc01"] h6')
  EFFECTIVE_DATE_ENTERED = (By.CSS_SELECTOR,
                            '[data-test-id="title_effective_date_'
                            'cf47bc01"] p')
  STOP_DATE = (By.CSS_SELECTOR,
               '[data-test-id="title_stop_date_cf47bc01"] h6')
  STOP_DATE_ENTERED = (By.CSS_SELECTOR,
                       '[data-test-id="title_stop_date_cf47bc01"] p')
  STATE = (By.CSS_SELECTOR,
           '[dadata-test-id="new_program_button_save_and_new_86160053"'
           ' ta-test-id="title_state_0ad9fbaf"] h6')
  STATE_ENTERED = (By.CSS_SELECTOR,
                   '[data-test-id="title_state_value_0ad9fbaf"]')
  PRIMARY_CONTACT = (By.CSS_SELECTOR, '[data-test-id="title_primary_'
                                      'contact_696de7244b84"] h6')
  PRIMARY_CONTACT_ENTERED = (
      By.CSS_SELECTOR, '[data-test-id="text_primary_contact_'
                       '696de7244b84"] [data-test-id="text_'
                       'manager_7a906d2e"]')
  SECONDARY_CONTACT = (
      By.CSS_SELECTOR, '[data-test-id="title_contacts_696de7244b84"] '
                       'h6:nth-child(2)')
  SECONDARY_CONTACT_ENTERED = (
      By.CSS_SELECTOR, '[data-test-id="text_secondary_contact_'
                       '696de7244b84"] [data-test-id="text_manager_'
                       '7a906d2e"]')
  PRIVATE_PROGRAM = (By.CSS_SELECTOR,
                     '[data-test-id="title_private_ec758af9"] h6')
  ICON_LOCK = (By.CSS_SELECTOR, '[data-test-id="icon_private_ec758af9"]')


class RequestInfoWidget(object):
  """Locators for the request info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class RiskInfoWidget(object):
  """Locators for the risk info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class OrgGroupInfoWidget(object):
  """Locators for the org group info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class IssueInfoWidget(object):
  """Locators for the org group info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class RegulationsInfoWidget(object):
  """Locators for the regulation info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class WorkflowInfoWidget(object):
  """Locators for the workflow info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class AuditInfoWidget(object):
  """Locators for the audit info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class AssessmentInfoWidget(object):
  """Locators for the assessment info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class PolicyInfoWidget(object):
  """Locators for the regulation info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class StandardInfoWidget(object):
  """Locators for the standard info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class ContractInfoWidget(object):
  """Locators for the contract info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class ClauseInfoWidget(object):
  """Locators for the clause info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class SectionInfoWidget(object):
  """Locators for the section info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class ControlInfoWidget(object):
  """Locators for the control info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class ObjectiveInfoWidget(object):
  """Locators for the objective info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class PeopleInfoWidget(object):
  """Locators for the people info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class VendorInfoWidget(object):
  """Locators for the vendor info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class AccessGroupInfoWidget(object):
  """Locators for the access group info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class SystemInfoWidget(object):
  """Locators for the system info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class ProcessInfoWidget(object):
  """Locators for the process info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class ProductInfoWidget(object):
  """Locators for the product info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class FacilityInfoWidget(object):
  """Locators for the facility info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class ProjectInfoWidget(object):
  """Locators for the project info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class MarketInfoWidget(object):
  """Locators for the market info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class DataAssetInfoWidget(object):
  """Locators for the data asset info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class ThreatInfoWidget(object):
  """Locators for the data asset info widget"""
  TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')


class AdminRolesWidget(object):
  """Locators for the roles widget on the admin dashboard"""

  ROLE_EDITOR = (
      By.CSS_SELECTOR, '[id="roles_list_widget"] li:nth-child(2) .span8>div')
  ROLE_GRC_ADMIN = (
      By.CSS_SELECTOR, '[id="roles_list_widget"] li:nth-child(3) .span8>div')
  ROLE_PROGRAM_EDITOR = (
      By.CSS_SELECTOR, '[id="roles_list_widget"] li:nth-child(4) .span8>div')
  ROLE_PROGRAM_OWNER = (
      By.CSS_SELECTOR, '[id="roles_list_widget"] li:nth-child(5) .span8>div')
  ROLE_PROGRAM_READER = (
      By.CSS_SELECTOR, '[id="roles_list_widget"] li:nth-child(6) .span8>div')
  ROLE_READER = (
      By.CSS_SELECTOR, '[id="roles_list_widget"] li:nth-child(7) .span8>div')
  ROLE_WORKFLOW_MEMBER = (
      By.CSS_SELECTOR, '[id="roles_list_widget"] li:nth-child(8) .span8>div')
  ROLE_WORKFLOW_OWNER = (
      By.CSS_SELECTOR, '[id="roles_list_widget"] li:nth-child(9) .span8>div')

  SCOPE_EDITOR = (
      By.CSS_SELECTOR,
      '[id="roles_list_widget"] li:nth-child(2) .span4 .scope')
  SCOPE_GRC_ADMIN = (
      By.CSS_SELECTOR,
      '[id="roles_list_widget"] li:nth-child(3) .span4 .scope')
  SCOPE_PROGRAM_EDITOR = (
      By.CSS_SELECTOR,
      '[id="roles_list_widget"] li:nth-child(4) .span4 .scope')
  SCOPE_PROGRAM_OWNER = (
      By.CSS_SELECTOR,
      '[id="roles_list_widget"] li:nth-child(5) .span4 .scope')
  SCOPE_PROGRAM_READER = (
      By.CSS_SELECTOR,
      '[id="roles_list_widget"] li:nth-child(6) .span4 .scope')
  SCOPE_READER = (
      By.CSS_SELECTOR,
      '[id="roles_list_widget"] li:nth-child(7) .span4 .scope')
  SCOPE_WORKFLOW_MEMBER = (
      By.CSS_SELECTOR,
      '[id="roles_list_widget"] li:nth-child(8) .span4 .scope')
  SCOPE_WORKFLOW_OWNER = (
      By.CSS_SELECTOR,
      '[id="roles_list_widget"] li:nth-child(9) .span4 .scope')


class WidgetInfoSettingsButton(object):
  """Locators for the control info widget"""

  TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"]>h3')

  DROPDOWN_SETTINGS_EDIT = (
      By.CSS_SELECTOR, '.info-pane-utility .dropdown-menu li:nth-child(1)')
  DROPDOWN_SETTINGS_PERMALINK = (
      By.CSS_SELECTOR, '.info-pane-utility .dropdown-menu li:nth-child(2)')
  DROPDOWN_SETTINGS_DELETE = (
      By.CSS_SELECTOR, '.info-pane-utility .dropdown-menu li:nth-child(3)')


class WidgetControls(object):
  TITLE = (By.CSS_SELECTOR, '#control_widget .sticky-filter .filter-title h6')
  TEXTFIELD = (By.CSS_SELECTOR, '#control_widget .sticky-filter .filter-input')
  BUTTON_SUBMIT = (
      By.CSS_SELECTOR,
      '#control_widget .sticky-filter .filter-button  [type="submit"]')
  BUTTON_RESET = (
      By.CSS_SELECTOR,
      '#control_widget .sticky-filter .filter-button  [type="reset"]')
  BUTTON_HELP = (
      By.CSS_SELECTOR,
      '#control_widget .sticky-filter .filter-button  #page-help')


class WidgetProducts(object):
  TITLE = (By.CSS_SELECTOR, '#product_widget .sticky-filter .filter-title h6')
  TEXTFIELD = (By.CSS_SELECTOR, '#product_widget .sticky-filter .filter-input')
  BUTTON_SUBMIT = (
      By.CSS_SELECTOR,
      '#product_widget .sticky-filter .filter-button [type="submit"]')
  BUTTON_RESET = (
      By.CSS_SELECTOR,
      '#product_widget .sticky-filter .filter-button [type="reset"]')
  BUTTON_HELP = (
      By.CSS_SELECTOR,
      '#product_widget .sticky-filter .filter-button #page-help')


class WidgetProjects(object):
  TITLE = (By.CSS_SELECTOR, '#project_widget .sticky-filter .filter-title h6')
  TEXTFIELD = (By.CSS_SELECTOR, '#project_widget .sticky-filter .filter-input')
  BUTTON_SUBMIT = (
      By.CSS_SELECTOR,
      '#project_widget .sticky-filter .filter-button [type="submit"]')
  BUTTON_RESET = (
      By.CSS_SELECTOR,
      '#project_widget .sticky-filter .filter-button [type="reset"]')
  BUTTON_HELP = (
      By.CSS_SELECTOR,
      '#project_widget .sticky-filter .filter-button #page-help')


class WidgetSystems(object):
  TITLE = (By.CSS_SELECTOR, '#system_widget .sticky-filter .filter-title h6')
  TEXTFIELD = (By.CSS_SELECTOR, '#system_widget .sticky-filter .filter-input')
  BUTTON_SUBMIT = (
      By.CSS_SELECTOR,
      '#system_widget .sticky-filter .filter-button [type="submit"]')
  BUTTON_RESET = (
      By.CSS_SELECTOR,
      '#system_widget .sticky-filter .filter-button [type="reset"]')
  BUTTON_HELP = (
      By.CSS_SELECTOR,
      '#system_widget .sticky-filter .filter-button #page-help')


class WidgetDataAssets(object):
  TITLE = (By.CSS_SELECTOR, '#data_asset_widget .sticky-filter .filter-title '
                            'h6')
  TEXTFIELD = (By.CSS_SELECTOR, '#data_asset_widget .sticky-filter '
                                '.filter-input')
  BUTTON_SUBMIT = (
      By.CSS_SELECTOR,
      '#data_asset_widget .sticky-filter .filter-button [type="submit"]')
  BUTTON_RESET = (
      By.CSS_SELECTOR,
      '#data_asset_widget .sticky-filter .filter-button [type="reset"]')
  BUTTON_HELP = (
      By.CSS_SELECTOR,
      '#data_asset_widget .sticky-filter .filter-button #page-help')


class WidgetProcesses(object):
  TITLE = (By.CSS_SELECTOR, '#process_widget .sticky-filter .filter-title h6')
  TEXTFIELD = (By.CSS_SELECTOR, '#process_widget .sticky-filter .filter-input')
  BUTTON_SUBMIT = (
      By.CSS_SELECTOR,
      '#process_widget .sticky-filter .filter-button [type="submit"]')
  BUTTON_RESET = (
      By.CSS_SELECTOR,
      '#process_widget .sticky-filter .filter-button [type="reset"]')
  BUTTON_HELP = (
      By.CSS_SELECTOR,
      '#process_widget .sticky-filter .filter-button #page-help')


class WidgetIssues(object):
  TITLE = (By.CSS_SELECTOR, '#issue_widget .sticky-filter .filter-title h6')
  TEXTFIELD = (By.CSS_SELECTOR, '#issue_widget .sticky-filter .filter-input')
  BUTTON_SUBMIT = (
      By.CSS_SELECTOR,
      '#issue_widget .sticky-filter .filter-button [type="submit"]')
  BUTTON_RESET = (
      By.CSS_SELECTOR,
      '#issue_widget .sticky-filter .filter-button [type="reset"]')
  BUTTON_HELP = (
      By.CSS_SELECTOR,
      '#issue_widget .sticky-filter .filter-button #page-help')


class AdminCustomAttributes(object):
  """Locators for the widget custom attributes in admin dashboard"""

  FILTER_INPUT_FIELD = (By.CLASS_NAME, 'filter-input')
  FILTER_BUTTON_SUBMIT = (By.CSS_SELECTOR, '.filter-button>[type="submit"]')
  FILTER_BUTTON_RESET = (By.CSS_SELECTOR, '.filter-button>[type="reset"]')

  TOGGLE_WORKFLOWS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(1) div '
                                       '.openclose')
  TOGGLE_RISK_ASSESSMENTS = (By.CSS_SELECTOR, '.tree-structure li:nth-child('
                                              '2) div .openclose')
  TOGGLE_THREATS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(3) div '
                                     '.openclose')
  TOGGLE_RISKS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(4) div '
                                   '.openclose')
  TOGGLE_PROGRAMS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(5) div '
                                      '.openclose')
  TOGGLE_AUDITS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(6) div '
                                    '.openclose')
  TOGGLE_OBJECTIVES = (By.CSS_SELECTOR,
                       '.tree-structure li:nth-child(7) div .openclose')
  TOGGLE_SECTIONS = (By.CSS_SELECTOR,
                     '.tree-structure li:nth-child(8) div .openclose')
  TOGGLE_CONTROLS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(9) div '
                                      '.openclose')
  TOGGLE_ISSUES = (By.CSS_SELECTOR, '.tree-structure li:nth-child(10) div '
                                    '.openclose')
  TOGGLE_ASSESSMENTS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(11) '
                                         'div .openclose')
  TOGGLE_STANDARDS = (By.CSS_SELECTOR,
                      '.tree-structure li:nth-child(12) div .openclose')
  TOGGLE_REGULATIONS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(13) '
                                         'div .openclose')
  TOGGLE_POLICIES = (By.CSS_SELECTOR, '.tree-structure li:nth-child(14) div '
                                      '.openclose')
  TOGGLE_CONTRACTS = (By.CSS_SELECTOR,
                      '.tree-structure li:nth-child(15) div .openclose')
  TOGGLE_CLAUSES = (By.CSS_SELECTOR, '.tree-structure li:nth-child(16) div '
                                     '.openclose')
  TOGGLE_REQUESTS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(17) div '
                                      '.openclose')
  TOGGLE_VENDORS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(18) div '
                                     '.openclose')
  TOGGLE_PEOPLE = (By.CSS_SELECTOR, '.tree-structure li:nth-child(19) div '
                                    '.openclose')
  TOGGLE_ACCESS_GROUPS = (By.CSS_SELECTOR,
                          '.tree-structure li:nth-child(20) div .openclose')
  TOGGLE_ORG_GROUPS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(21) '
                                        'div .openclose')
  TOGGLE_PRODUCTS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(22) div '
                                      '.openclose')
  TOGGLE_MARKETS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(23) div '
                                     '.openclose')
  TOGGLE_PROCESSES = (By.CSS_SELECTOR,
                      '.tree-structure li:nth-child(24) div .openclose')
  TOGGLE_FACILITIES = (By.CSS_SELECTOR, '.tree-structure li:nth-child(25) '
                                        'div .openclose')
  TOGGLE_PROJECTS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(26) div '
                                      '.openclose')
  TOGGLE_DATA_ASSETS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(27) '
                                         'div .openclose')
  TOGGLE_SYSTEMS = (By.CSS_SELECTOR, '.tree-structure li:nth-child(28) div '
                                     '.openclose')

  # programs dropdown
  BUTTON_ADD_CUSTOM_PROGRAM_ATTR = (
      By.CSS_SELECTOR, '.tree-structure li:nth-child(5)'
                       ' [data-toggle="modal-ajax-form"]')
  PROGRAMS_LABEL_ATTRIBUTE_NAME = (
      By.CSS_SELECTOR,
      '.tree-structure li:nth-child(5) div thead>tr>th:nth-child(1)')
  PROGRAMS_LABEL_ATTRIBUTE_TYPE = (
      By.CSS_SELECTOR,
      '.tree-structure li:nth-child(5) div thead>tr>th:nth-child(2)')
  PROGRAMS_LABEL_MANDATORY = (
      By.CSS_SELECTOR,
      '.tree-structure li:nth-child(5) div thead>tr>th:nth-child(3)')
  PROGRAMS_LABEL_EDIT = (
      By.CSS_SELECTOR,
      '.tree-structure li:nth-child(5) div thead>tr>th:nth-child(4)')
  LISTED_MEMBERS = (
      By.CSS_SELECTOR,
      '.tree-structure li:nth-child(5) div tbody>tr')
  BUTTON_LISTED_MEMBERS_EDIT = (
      By.CSS_SELECTOR,
      '.tree-structure li:nth-child(5) div tbody>tr>td>ul .fa-pencil-square-o')
