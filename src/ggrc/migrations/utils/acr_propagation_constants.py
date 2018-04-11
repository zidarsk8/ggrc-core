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

BASIC_ROLES = (
    "Admin",
    "Primary Contacts",
    "Secondary Contacts",
)

COMMENT_DOCUMENT_R = {
    "Relationship R": {
        "Comment R": {},
        "Document R": {},
    },
}

COMMENT_DOCUMENT_RU = {
    "Relationship R": {
        "Comment R": {},
        "Document RU": {},
    },
}

PROPOSAL_RU = {
    "Relationship R": {
        "Comment R": {},
        "Document RU": {},
        "Proposal RU": {},
    },
}

PROPOSAL_R = {
    "Relationship R": {
        "Comment R": {},
        "Document RU": {},
        "Proposal RU": {},
    },
}

BASIC_PROPAGATION = {
    "Admin": COMMENT_DOCUMENT_RU,
}
