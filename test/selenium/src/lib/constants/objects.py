# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Constants and methods for work with objects."""


# objects
PROGRAMS = "programs"
WORKFLOWS = "workflows"
AUDITS = "audits"
ASSESSMENTS = "assessments"
ASSESSMENT_TEMPLATES = "assessment_templates"
ISSUES = "issues"
DIRECTIVES = "directives"
REGULATIONS = "regulations"
POLICIES = "policies"
STANDARDS = "standards"
CONTRACTS = "contracts"
CLAUSES = "clauses"
SECTIONS = "sections"
CONTROLS = "controls"
OBJECTIVES = "objectives"
PEOPLE = "people"
ORG_GROUPS = "org_groups"
VENDORS = "vendors"
ACCESS_GROUPS = "access_groups"
SYSTEMS = "systems"
PROCESSES = "processes"
DATA_ASSETS = "data_assets"
PRODUCTS = "products"
PROJECTS = "projects"
FACILITIES = "facilities"
MARKETS = "markets"
RISKS = "risks"
THREATS = "threats"
RISK_ASSESSMENTS = "risk_assessments"

ALL_CA_OBJECTS = (WORKFLOWS, RISK_ASSESSMENTS, THREATS, RISKS,
                  PROGRAMS, AUDITS, OBJECTIVES, SECTIONS,
                  CONTROLS, ISSUES, ASSESSMENTS, STANDARDS,
                  REGULATIONS, POLICIES, CONTRACTS, CLAUSES,
                  VENDORS, PEOPLE, ACCESS_GROUPS,
                  ORG_GROUPS, PRODUCTS, MARKETS, PROCESSES,
                  FACILITIES, PROJECTS, DATA_ASSETS, SYSTEMS)

# templates
COUNT = "count"


def _get_singular(plurals):
  """
 Return: list of basestring: Capitalized object names in singular form
 """
  singulars = []
  for name in plurals:
    name = name.lower()
    if name == PEOPLE:
      singular = "person"
    elif name == POLICIES:
      singular = "policy"
    elif name == PROCESSES:
      singular = "process"
    elif name == FACILITIES:
      singular = "facility"
    else:
      singular = name[:-1]
    singulars.append(singular.upper())
  return singulars


def _get_plural(singulars):
  """
 Return: list of basestring: Capitalized object names in plural form
 """
  plurals = []
  for name in singulars:
    name = name.lower()
    if name == "people":
      plural = PEOPLE
    elif name == "policy":
      plural = POLICIES
    elif name == "process":
      plural = PROCESSES
    elif name == "facility":
      plural = FACILITIES
    else:
      plural = name + "s"
    plurals.append(plural.upper())
  return plurals


def get_singular(plural):
  """Transform object name to singular and lower form.
 Example: risk_assessments -> risk_assessment
 """
  return _get_singular([plural])[0].lower()


def get_normal_form(obj_name, with_space=True):
  """Transform object name to title form.
 Example:
 if with_space=True then risk_assessments -> Risk Assessments
 if with_space=False then risk_assessments -> RiskAssessments
 """
  normal = obj_name.replace("_", " ").title()
  if with_space is True:
    return normal
  elif with_space is False:
    return normal.replace(" ", "")


ALL_PLURAL = [
    k for k in globals().keys() if not k.startswith("_") or k == "ALL"][1:]
ALL_SINGULAR = _get_singular(ALL_PLURAL)
