# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for snapshot block converter."""

from collections import defaultdict
from collections import OrderedDict

from cached_property import cached_property

from ggrc import models


class SnapshotBlockConverter(object):
  """Block converter for snapshots of a single object type."""

  def __init__(self, converter, ids):
    self.converter = converter
    self.ids = ids

  @staticmethod
  def handle_row_data():
    pass

  @property
  def name(self):
    return "{} Snapshot".format(self.child_type)

  @cached_property
  def snapshots(self):
    """List of all snapshots in the current block.

    The content of the given snapshots also contains the mapped audit field.
    """
    if not self.ids:
      return []
    snapshots = models.Snapshot.eager_query().filter(
        models.Snapshot.id.in_(self.ids)
    ).all()

    for snapshot in snapshots:  # add special snapshot attribute
      snapshot.revision.content["audit"] = {
          "type": "Audit",
          "id": snapshot.parent_id
      }
    return snapshots

  @cached_property
  def child_type(self):
    """Name of snapshot object types."""
    child_types = {snapshot.child_type for snapshot in self.snapshots}
    assert len(child_types) <= 1
    return child_types.pop() if child_types else ""

  @cached_property
  def _cad_name_map(self):
    """Get id to name mapping for all custom attribute definitions."""
    cad_map = {}
    for snap in self.snapshots:
      for cad in snap.revision.content.get("custom_attribute_definitions", []):
        cad_map[cad["id"]] = cad["title"]
    return OrderedDict(sorted(cad_map.iteritems(), key=lambda x: x[1]))

  def _gather_stubs(self):
    """Gather all possible stubs from snapshot contents.

    Returns:
      dictionary of object types and their ids.
    """
    stubs = defaultdict(set)

    def walk(value, stubs):
      if isinstance(value, list):
        for val in value:
          walk(val, stubs)
      elif isinstance(value, dict):
        if "type" in value and "id" in value:
          stubs[value["type"]].add(value["id"])
        for val in value.values():
          walk(val, stubs)

    for snapshot in self.snapshots:
      walk(snapshot.revision.content, stubs)
    return stubs

  @staticmethod
  def to_array():
    return [[]], [[]]  # header and body
