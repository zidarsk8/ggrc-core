# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for keeping constants for ACR propagation rules
DO NOT MODIFY THESE VALUES.
These are just the common propagation dictionaries, that are used in different
migration files.
For migration consistency, do not update these values once they are merged.
If a modification is needed feel free to use these and modify them inside the
migration file, or add new common roles and propagation rules.
"""

COMMENT_DOCUMENT_RUD = {
    "Relationship R": {
        "Comment R": {},
        "Document RU": {
            "Relationship R": {
                "Comment R": {},
            }
        },
    },
}

NEW_ROLES_PROPAGATION = {
    "Assignee": COMMENT_DOCUMENT_RUD,
    "Verifier": COMMENT_DOCUMENT_RUD,
    "Compliance Contacts": COMMENT_DOCUMENT_RUD,
}

GGRC_NEW_ROLES_PROPAGATION = {
    "AccessGroup": NEW_ROLES_PROPAGATION,
    "DataAsset": NEW_ROLES_PROPAGATION,
    "Facility": NEW_ROLES_PROPAGATION,
    "Market": NEW_ROLES_PROPAGATION,
    "Metric": NEW_ROLES_PROPAGATION,
    "OrgGroup": NEW_ROLES_PROPAGATION,
    "Process": NEW_ROLES_PROPAGATION,
    "Product": NEW_ROLES_PROPAGATION,
    "ProductGroup": NEW_ROLES_PROPAGATION,
    "Project": NEW_ROLES_PROPAGATION,
    "System": NEW_ROLES_PROPAGATION,
    "TechnologyEnvironment": NEW_ROLES_PROPAGATION,
    "Vendor": NEW_ROLES_PROPAGATION,
}
