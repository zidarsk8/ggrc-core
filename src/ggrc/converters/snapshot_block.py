# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for snapshot block converter."""

from typing import Dict, List, Any

import logging

from collections import defaultdict
from collections import OrderedDict

from cached_property import cached_property

from ggrc import db
from ggrc import models
from ggrc import utils
from ggrc.utils import benchmark
from ggrc.models.reflection import AttributeInfo

logger = logging.getLogger(__name__)


class SnapshotBlockConverter(object):
  """Block converter for snapshots of a single object type."""

  # Name of the field that indicates if mappings should be included in the
  # export or not
  MAPPINGS_KEY = "mappings"

  DATE_FIELDS = {
      "start_date",
      "end_date",
  }

  CUSTOM_SNAPSHOT_ALIASES = {
      "audit": "Audit",
      "revision_date": "Revision Date",
  }

  SNAPSHOT_MAPPING_ALIASES = {
      "__mapping__:Assessment": "Map: Assessment",
      "__mapping__:Issue": "Map: Issue",
  }

  BOOLEAN_ALIASES = {
      True: "yes",
      "1": "yes",
      False: "no",
      None: "no",
      "0": "no",
      "": "no",
  }

  def __init__(self, converter, ids, fields=None):
    self.converter = converter
    self.ids = ids
    self.fields = fields or []

  @staticmethod
  def handle_row_data():
    pass

  @property
  def name(self):
    return "{} Snapshot".format(self.child_type)

  @cached_property
  def _content_value_map(self):
    """Mappings for all special value names.

    In the future these should be pulled from individual objects.
    """
    # pylint: disable=no-self-use
    return {
        "Control": {
            "key_control": {
                True: "key",
                False: "non-key",
            }
        }
    }

  def _generate_mapping_content(self, snapshot):
    # type: (Any) -> Dict[str, List[Dict[str, Any]]]
    """Generate mapping stub lists for snapshot mappings."""
    content = {}
    for key in self.SNAPSHOT_MAPPING_ALIASES:
      model_name = key.split(":")[1]
      content[key] = [
          {"type": rel.destination_type, "id": rel.destination_id}
          for rel in snapshot.related_destinations
          if rel.destination_type == model_name
      ] + [
          {"type": rel.source_type, "id": rel.source_id}
          for rel in snapshot.related_sources
          if rel.source_type == model_name
      ]
    return content

  def _extend_revision_content(self, snapshot):
    # type: Any -> Dict[str, Any]
    """Extend normal object content with attributes needed for export.

    When exporting snapshots we must add additional information to the original
    object content to show the version and what audit the snapshot of the
    object belongs to.
    """
    content = {}
    content.update(snapshot.revision.content)
    content["audit"] = {"type": "Audit", "id": snapshot.parent_id}
    content["slug"] = u"*{}".format(content["slug"])
    content["revision_date"] = unicode(snapshot.revision.created_at)
    if self.MAPPINGS_KEY in self.fields:
      content.update(self._generate_mapping_content(snapshot))
    return content

  @cached_property
  def snapshots(self):
    """List of all snapshots in the current block.

    The content of the given snapshots also contains the mapped audit field.
    """
    with benchmark("Gather selected snapshots"):
      if not self.ids:
        return []
      snapshots = models.Snapshot.eager_query().filter(
          models.Snapshot.id.in_(self.ids)
      ).all()

      for snapshot in snapshots:  # add special snapshot attribute
        snapshot.content = self._extend_revision_content(snapshot)
      return snapshots

  @cached_property
  def child_type(self):
    """Name of snapshot object types."""
    child_types = {snapshot.child_type for snapshot in self.snapshots}
    assert len(child_types) <= 1
    return child_types.pop() if child_types else ""

  @cached_property
  def _cad_map(self):
    """Get id to cad mapping for all cad ordered by title."""
    cad_map = {}
    for snap in self.snapshots:
      for cad in snap.content.get("custom_attribute_definitions", []):
        cad_map[cad["id"]] = cad
    return OrderedDict(
        sorted(cad_map.iteritems(), key=lambda x: x[1]["title"])
    )

  @cached_property
  def _cad_name_map(self):
    """Get id to name mapping for all cad ordered by title."""
    return OrderedDict([
        (key, value["title"])
        for key, value in self._cad_map.items()
    ])

  @cached_property
  def _attribute_name_map(self):
    """Get property to name mapping for object attributes."""
    model = getattr(models.all_models, self.child_type, None)
    if not model:
      logger.warning("Exporting invalid snapshot model: %s", self.child_type)
      return {}
    aliases = AttributeInfo.gather_visible_aliases(model)
    aliases.update(self.CUSTOM_SNAPSHOT_ALIASES)
    if self.MAPPINGS_KEY in self.fields:
      aliases.update(self.SNAPSHOT_MAPPING_ALIASES)
    name_map = {
        key: value["display_name"] if isinstance(value, dict) else value
        for key, value in aliases.iteritems()
    }
    orderd_keys = AttributeInfo.get_column_order(name_map.keys())
    return OrderedDict((key, name_map[key]) for key in orderd_keys)

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
      walk(snapshot.content, stubs)
    return stubs

  @cached_property
  def _stub_cache(self):
    """Generate cache for all stubbed values."""
    id_map = {
        "Person": "email",
        "Option": "title",
    }
    stubs = self._gather_stubs()
    cache = {}
    for model_name, ids in stubs.iteritems():
      with benchmark("Generate snapshot cache for: {}".format(model_name)):
        model = getattr(models.all_models, model_name, None)
        attr = getattr(model, id_map.get(model_name, "slug"), None)
        if not attr:
          continue
        model_count = model.query.count()
        if len(ids) > model_count / 2:
          cache[model_name] = dict(db.session.query(model.id, attr))
        else:
          cache[model_name] = dict(db.session.query(
              model.id, attr).filter(model.id.in_(ids)))
    return cache

  def get_value_string(self, value):
    """Get string representation of a given value."""
    if isinstance(value, dict) and "type" in value and "id" in value:
      return self._stub_cache.get(value["type"], {}).get(value["id"], u"")
    elif isinstance(value, list):
      return u"\n".join(self.get_value_string(val) for val in value)
    elif isinstance(value, bool):
      return self.BOOLEAN_ALIASES.get(value, u"")
    elif isinstance(value, basestring):
      return value
    return u""

  def get_content_string(self, content, name):
    """Get user visible string of the content value.

    Args:
      content: dict with keys and values.
      name: dict key that we want to read.
    Returns:
      User visible string representation of a content value.
    """
    value_map = self._content_value_map.get(self.child_type, {}).get(name)
    if value_map:
      return value_map.get(content.get(name), u"")
    if name in self.DATE_FIELDS:
      val = content.get(name)
      if not val:
        return u""
      if "T" in val or " " in val:
        # values in format of "YYYY-MM-DDThh:mm:ss" and "YYYY-MM-DD hh:mm:ss"
        return val.replace("T", " ")
      return utils.iso_to_us_date(val)
    return self.get_value_string(content.get(name))

  def get_cav_value_string(self, value):
    """Get string representation of a custom attribute value."""
    if value is None:
      return u""
    cad = self._cad_map[value["custom_attribute_id"]]
    val = value.get("attribute_value") or u""
    if cad["attribute_type"] == "Map:Person":
      return self._stub_cache.get(val, {}).get(
          value.get("attribute_object_id"), u"")
    if cad["attribute_type"] == "Checkbox":
      return self.BOOLEAN_ALIASES.get(val, u"")
    if cad["attribute_type"] == "Date" and val:
      return utils.iso_to_us_date(val)
    return val

  @property
  def _header_list(self):
    return [
        [],  # empty line reserved for column descriptions
        self._attribute_name_map.values() + self._cad_name_map.values()
    ]

  def _obj_attr_line(self, content):
    """Get object attribute CSV values."""
    return [
        self.get_content_string(content, name)
        for name in self._attribute_name_map
    ]

  def _cav_attr_line(self, content):
    """Get custom attribute CSV values."""
    cav_map = {
        cav["custom_attribute_id"]: cav
        for cav in content.get("custom_attribute_values", [])
    }
    return [
        self.get_cav_value_string(cav_map.get(cad_id))
        for cad_id in self._cad_name_map
    ]

  def _content_line_list(self, snapshot):
    """Get a CSV content line for a single snapshot."""
    content = snapshot.content
    return self._obj_attr_line(content) + self._cav_attr_line(content)

  @property
  def _body_list(self):
    """Get 2D representation of CSV content."""
    return [
        self._content_line_list(snapshot)
        for snapshot in self.snapshots
    ] or [[]]

  def to_array(self):
    """Get 2D list representing the CSV file."""
    return self._header_list, self._body_list
