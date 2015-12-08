# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

scope = "System"
description = """
  This role grants a user the permission to create public and private programs.
  """
permissions = {
    "read": [
        "Program",
    ],
    "create": [
        "Program",
    ],
    "view_object_page": [
        "__GGRC_ALL__"
    ],
    "update": [
        {
            "type": "Program",
            "terms": {
                "list_property": "owners",
                "value": "$current_user"
            },
            "condition": "contains"
        }
    ],
    "delete": [
        {
            "type": "Program",
            "terms": {
                "list_property": "owners",
                "value": "$current_user"
            },
            "condition": "contains"
        },
    ]
}
