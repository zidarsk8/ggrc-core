# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module containing dummy POST/PUT data for GGRC models.

The data is from copy pasted and cleaned up POST request on specific models.

Data should be access with get_template function that does a deep copy of these
templates.
"""

import copy

FACILITY = {
    "_pending_joins": [],
    "_transient": {},
    "status": "Draft",
    "owners": [],
    "access_control_list": [],
    "custom_attribute_definitions": [],
    "custom_attributes": {},
    "title": "aa",
    "description": "ee",
    "notes": "uuu",
    "url": "",
    "reference_url": "",
    "slug": "",
    "context": None
}

CONTROL = {
    "_pending_joins": [],
    "_transient": {},
    "selected": False,
    "title": "",
    "slug": "",
    "description": "",
    "url": "",
    "status": "Draft",
    "owners": [],
    "custom_attribute_definitions": [],
    "custom_attributes": {},
    "test_plan": "",
    "notes": "",
    "reference_url": "",
    "fraud_related": None,
    "key_control": None,
    "access_control_list": [],
    "kind": None,
    "means": None,
    "verify_frequency": None,
    "context": None
}

PERSON = {
    "_pending_joins": [],
    "_transient": {},
    "name": "",
    "email": "",
    "owners": None,
    "custom_attribute_definitions": [],
    "custom_attributes": {},
    "company": "",
    "context": None,
}

CUSTOM_ATTRIBUTE_DEFINITION = {
    "_pending_joins": [],
    "_transient": {},
    "title": "",
    "attribute_type": "",
    "custom_attributes": {},
    "definition_type": "",
    "modal_title": "Add Attribute",
    "mandatory": "",
    "helptext": "some help text",
    "placeholder": "placeholder tex",
    "context": {"id": None},
    "multi_choice_options": "one,two,three,four,five",
}

CUSTOM_ATTRIBUTE_VALUE = {
    "id": None,
    "custom_attribute_id": 1052,
    "attribute_value": None,
    "attribute_object": None,
    "validation": {
        "empty": True,
        "mandatory": False,
        "valid": True
    },
    "def": {},  # invalid property should be removed from front-end
    "attributeType": "person",
    "preconditions_failed": [],
    "errorsMap": {
        "comment": False,
        "evidence": False
    }
}

USER_ROLE = {
    "_pending_joins": [],
    "_transient": {},
    "role": "",
    "person": "",
    "context": None,
}

OBJECT_OWNER = {
    "context": None,
    "_pending_joins": [],
    "ownable": "",
    "person": "",
}

OBJECTIVE = {
    "_pending_joins": [],
    "_transient": {},
    "status": "Draft",
    "owners": [],
    "custom_attribute_definitions": [],
    "custom_attributes": {},
    "title": "",
    "description": "",
    "notes": "",
    "url": "",
    "reference_url": "",
    "slug": "",
    "access_control_list": [],
    "context": None,
}

MARKET = {
    "_pending_joins": [],
    "_transient": {},
    "status": "Draft",
    "owners": [],
    "custom_attribute_definitions": [],
    "custom_attributes": {},
    "title": "aou",
    "description": "uoe",
    "notes": "oe",
    "url": "aou",
    "reference_url": "aou",
    "slug": "",
    "access_control_list": [],
    "start_date": "2017-06-08",
    "end_date": "2017-06-20",
    "context": None,
}

REGULATION = {
    "_pending_joins": [],
    "_transient": {},
    "status": "Draft",
    "kind": "Regulation",
    "owners": [],
    "custom_attribute_definitions": [],
    "custom_attributes": {},
    "title": "eeee",
    "description": "eeeee",
    "notes": "o",
    "url": "ue",
    "reference_url": "ueo",
    "slug": "",
    "access_control_list": [],
    "start_date": "2017-06-08",
    "context": None,
}

PROGRAM = {
    "_pending_joins": [],
    "_transient": {},
    "status": "Draft",
    "custom_attribute_definitions": [],
    "custom_attributes": {},
    "kind": "Directive",
    "title": "aaa",
    "description": "aaa",
    "notes": "aaaa",
    "url": "Program url",
    "reference_url": "reference url",
    "slug": "",
    "access_control_list": [],
    "start_date": "2017-06-23",
    "end_date": "2017-06-26",
    "context": None,
}

AUDIT = {
    "status": "Planned",
    "custom_attribute_definitions": [],
    "custom_attributes": {},
    "_transient": {},
    "title": "",
    "program": {
        "id": 1,
        "href": "/api/programs/1",
        "type": "Program"
    },
    "description": "",
    "audit_firm": {
        "id": 1,
        "href": "/api/org_groups/1",
        "type": "OrgGroup"
    },
    "slug": "",
    "modified_by_id": "1",
    "start_date": "2017-06-15",
    "end_date": "2017-06-30",
    "report_start_date": "2017-06-01",
    "report_end_date": "2017-06-30",
    "changes": [],
    "context": {
        "id": 44,
        "href": "/api/contexts/44",
        "type": "Context"
    }
}

ASSESSMENT_TEMPLATE = {
    "test_plan_procedure": False,
    "template_object_type": "Control",
    "default_people": {
        "assessors": "Primary Contacts",
        "verifiers": "Auditors"
    },
    "assessorsList": {},
    "verifiersList": {},
    "people_values": [{
        "value": "Object Owners",
        "title": "Object Admins"
    }, {
        "value": "Audit Lead",
        "title": "Audit Lead"
    }, {
        "value": "Auditors",
        "title": "Auditors"
    }, {
        "value": "Principal Assignees",
        "title": "Principal Assignees"
    }, {
        "value": "Secondary Assignees",
        "title": "Secondary Assignees"
    }, {
        "value": "Primary Contacts",
        "title": "Primary Contacts"
    }, {
        "value": "Secondary Contacts",
        "title": "Secondary Contacts"
    }, {
        "value": "other",
        "title": "Others..."
    }],
    "_NON_RELEVANT_OBJ_TYPES": {},
    "ignore_ca_errors": True,
    "_pending_joins": [],
    "custom_attributes": {},
    "_transient": {},
    "custom_attribute_definitions": [],
    "_objectTypes": {},
    "assessorsListDisable": True,
    "verifiersListDisable": True,
    "title": "auoe",
    "procedure_description": "",
    "audit": {
        "id": 4,
        "href": "/api/audits/4",
        "type": "Audit"
    },
    "context": {
        "id": 137,
        "href": "/api/contexts/137",
        "type": "Context"
    },
    "slug": ""
}

ORG_GROUP = {
    "status": "Active",
    "_pending_joins": [],
    "owners": [],
    "access_control_list": [],
    "custom_attribute_definitions": [],
    "custom_attributes": {},
    "_transient": {},
    "title": "uoau",
    "description": "uoauoe",
    "notes": "uoauo",
    "url": "org group url",
    "reference_url": "org group referenc eurl",
    "slug": "",
    "start_date": "2017-06-22",
    "end_date": "2017-06-30",
    "context": None,
}

RELATIONSHIP = {
    "source": {},
    "destination": {},
    "context": None,
    "_pending_joins": [],
}


ASSESSMENT_GENERATION = {
    "audit": {},
    "context": {},
    "object": {},
    "owners": [],
    "recipients": "Assessor,Creator,Verifier",
    "run_in_background": False,
    "send_by_default": True,
    "status": "Not Started",
    "template": {},
    "title": "Generated Assessment for Audit title (2) R0QNI7VE",
    "_generated": True,
    "_pending_joins": [],
}


MAP = {
    # Basic objects
    "Control": CONTROL,
    "Facility": FACILITY,
    "Market": MARKET,
    "Objective": OBJECTIVE,
    "Program": PROGRAM,
    "Regulation": REGULATION,
    "Audit": AUDIT,
    "OrgGroup": ORG_GROUP,
    "AssessmentTemplate": ASSESSMENT_TEMPLATE,

    # special objects
    "Person": PERSON,
    "CustomAttributeDefinition": CUSTOM_ATTRIBUTE_DEFINITION,
    "CustomAttributeValue": CUSTOM_ATTRIBUTE_VALUE,
    "UserRole": USER_ROLE,
    "ObjectOwner": OBJECT_OWNER,
    "Relationship": RELATIONSHIP,
    "AssessmentGeneration": ASSESSMENT_GENERATION,
}


def get_template(model):
  return copy.deepcopy(MAP[model])
