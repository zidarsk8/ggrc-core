# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

WRONG_FILE_TYPE = ("Line {line}: Wrong file type. Only .csv files are"
                   " supported. Please upload a .csv file.")

MISSING_COLUMN = ("Line {line}: Missing mandatory column{s} {column_names},"
                  " when adding object.")

MISSING_CUSTOM_ATTRIBUTE_COLUMN = ("Line {line}: Missing custom column"
                                   " {column_name}, when adding object.")

WRONG_OBJECT_TYPE = "Line {line}: Unknown object type '{object_name}'"

UNKNOWN_COLUMN = ("Line {line}: Attribute '{column_name}' does not"
                  " exist. Column will be ignored.")

DELETE_UNKNOWN_OBJECT = ("Line {line}: Object '{slug}' does not exist, so it"
                         " can't be deleted.")

DUPLICATE_VALUE = ("Line {line}: {column_name} '{title}' already exists."
                   "Record will be ignored.")

DUPLICATE_VALUE_IN_CSV = ("Lines {line_list} have same {column_name}"
                          " '{value}'. Line{s} {ignore_lines} will be"
                          " ignored.")

MAP_UNMAP_CONFLICT = ("Line {line}: Object '{slug}' scheduled for mapping and"
                      " unmapping at the same time. Mapping rule update will"
                      " be ignored.")

UNKNOWN_OBJECT = ("Line {line}: {object_type} '{slug}' doesn't exist, so it"
                  " can't be mapped/unmapped.")

WHITESPACE_WARNING = ("Line {line}: Field {column_name} contains multiple"
                      "spaces together, that will be merged into one.")

UNKNOWN_USER_WARNING = ("Line {line}: Specified user '{email}' does not exist."
                        " That user will be ignored.")

UNKNOWN_USER_ERROR = ("Specified user '{email}' does not exist. That user will"
                      " be ignored.")

OWNER_MISSING = ("Line {line}: Owner field does not contain a valid owner."
                 " You will be assigned as object owner.")

WRONG_VALUE = ("Line {line}: {column_name} contains invalid data. The value"
               " will be ignored.")

WRONG_REQUIRED_VALUE = ("Line {line}: Required field {column_name} contains"
                        " invalid data '{value}'. The default value will be"
                        "used.")

MISSING_VALUE_ERROR = ("Line {line}: Field {column_name} is required. The line"
                       " will be ignored.")

PERMISSION_ERROR = ("Line {line}: You don't have permission to update/delete"
                    " this record.")

MAPPING_PERMISSION_ERROR = ("Line {line}: You don't have permission to update"
                            " mappings for {object_type}: {title} ({slug}).")

UNKNOWN_ERROR = "Line {line}: Import failed due to unknown error."
