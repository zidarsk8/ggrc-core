# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc.models import (
    Audit, Control, ControlAssessment, DataAsset, Directive, Contract,
    Policy, Regulation, Standard, Facility, Market, Objective, Option,
    OrgGroup, Vendor, Person, Product, Program, Project, Request, Response,
    Section, Clause, System, Process, Issue,
)
from ggrc.utils import get_mapping_rules


def get_shared_unique_rules():
  """ get rules for all cross checks betveen classes

  used for checking unique constraints on colums such as code and title
  """

  shared_tables = [
      (System, Process),
      (Section, Clause),
      (Policy, Regulation, Standard, Contract),
  ]
  rules = {}
  for tables in shared_tables:
    for table in tables:
      rules[table] = tables

  return rules


def get_allowed_mappings():
  """ get all mapping rules with lowercase names

  import export is case insensitive so we use lower case names for all
  comparisons.
  """
  mapping_rules = get_mapping_rules()
  for object_mappings in mapping_rules.values():
    map(str.lower, object_mappings)
  return mapping_rules


IMPORTABLE = {
    "audit": Audit,
    "control": Control,
    "control assessment": ControlAssessment,
    "control_assessment": ControlAssessment,
    "data asset": DataAsset,
    "data_asset": DataAsset,
    "directive": Directive,
    "contract": Contract,
    "policy": Policy,
    "regulation": Regulation,
    "standard": Standard,
    "facility": Facility,
    "market": Market,
    "objective": Objective,
    "option": Option,
    "org group": OrgGroup,
    "org_group": OrgGroup,
    "vendor": Vendor,
    "person": Person,
    "product": Product,
    "program": Program,
    "project": Project,
    "request": Request,
    "response": Response,
    "section": Section,
    "clause": Clause,
    "system": System,
    "process": Process,
    "issue": Issue,
}

COLUMN_ORDER = (
    "slug",
    "title",
    "description",
    "test_plan",
    "notes",
    "owners",
    "start_date",
    "end_date",
    "report_end_date",
    "report_start_date",
    "assertions",
    "audit",
    "categories",
    "contact",
    "control",
    "design",
    "directive_id",
    "fraud_related",
    "key_control",
    "kind",
    "link",
    "means",
    "network_zone",
    "operationally",
    "principal_assessor",
    "private",
    "program_id",
    "secondary_assessor",
    "secondary_contact",
    "status",
    "url",
    "reference_url",
    "_user_role_auditor",
    "verify_frequency",
    "name",
    "email",
    "is_enabled",
    "company",
    "_custom_attributes",
)
