# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc.converters.sections import SectionsConverter
from ggrc.models import (
    Audit, Control, ControlAssessment, DataAsset, Directive, Contract,
    Policy, Regulation, Standard, Facility, Market, Objective, Option,
    OrgGroup, Vendor, Person, Product, Program, Project, Request, Response,
    Section, Clause, System, Process, Issue,
)


all_converters = [('sections', SectionsConverter)]

HANDLERS = {}


def get_converter(name):
  return all_converters(name)

COLUMN_ORDER = (
    "slug",
    "title",
    "description",
    "notes",
    "owners",
)

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
