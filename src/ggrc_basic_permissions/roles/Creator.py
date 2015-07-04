scope = "System"
description = """
  This role grants a user basic object creation and editing permission.
  """

_is_owner = [
    "Categorization",
    {
        "type": "Category",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Issue",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "ControlAssessment",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Control",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "DataAsset",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Directive",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Contract",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Policy",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Regulation",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Standard",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Document",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Facility",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Market",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Objective",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    "ObjectDocument",
    "ObjectOwner",
    "ObjectPerson",
    {
        "type": "Option",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "OrgGroup",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Vendor",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    "PopulationSample",
    {
        "type": "Product",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Relationship",
        "terms": {},
        "condition": "relationship",
    },
    "RelationshipType",
    {
        "type": "SectionBase",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Section",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Clause",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "SystemOrProcess",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "System",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Process",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    {
        "type": "Project",
        "terms": {
            "list_property": "owners",
            "value": "$current_user"
        },
        "condition": "contains"
    },
    "Request",
    "Response",
    "Person"
]

permissions = {
    "read": _is_owner,
    "create": [
        "Workflow"
        "Categorization",
        "Category",
        "ControlCategory",
        "ControlAssertion",
        "Control",
        "ControlAssessment",
        "Issue",
        "DataAsset",
        "Directive",
        "Contract",
        "Policy",
        "Regulation",
        "Standard",
        "Document",
        "Facility",
        "Help",
        "Market",
        "Objective",
        "ObjectDocument",
        "ObjectPerson",
        "Option",
        "OrgGroup",
        "Vendor",
        "PopulationSample",
        "Product",
        "Project",
        "Relationship",
        "RelationshipType",
        "SectionBase",
        "Section",
        "Clause",
        "SystemOrProcess",
        "System",
        "Process",
        {
            "type": "ObjectOwner",
            "terms": {
                "property_name": "ownable.modified_by",
                "value": "$current_user"
            },
            "condition": "is"
        },
        "Person",
        "Program",
        "Role",
        "UserRole",
        "Request",
        "Response",
        "Context",
        {
            "type": "BackgroundTask",
            "terms": {
                "property_name": "modified_by",
                "value": "$current_user"
            },
            "condition": "is"
        },
    ],
    "view_object_page": _is_owner,
    "update": _is_owner,
    "delete": _is_owner,
}
