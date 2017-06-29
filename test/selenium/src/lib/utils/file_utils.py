# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Utils for manipulation with directories and files."""

import csv
from collections import defaultdict


def get_list_objs_scopes_from_csv(path_to_csv):
  """Open according to 'path_to_csv' CSV file witch is expected to contain
  exported objects, parse through CSV file's structure and return list of
  objects scopes (dicts with keys as exportable field names, values as values
  of this field for current instance).
  """
  with open(path_to_csv) as csv_file:
    rows = csv.reader(csv_file)
    object_type = None
    keys = []
    results = defaultdict(list)
    for columns in rows:
      if not any(columns):
        continue
      if columns[0] == "Object type":
        # new block started
        object_type = None
        keys = []
        continue
      if object_type is None:
        keys = columns[1:]
        object_type = columns[0]
        continue
      columns = [unicode(val) for val in columns]
      results[object_type].append(dict(zip(keys, columns[1:])))
    return results
