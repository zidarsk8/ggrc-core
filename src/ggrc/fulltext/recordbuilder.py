# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for full text index record builder."""

import ggrc.models.all_models
from ggrc.models.reflection import AttributeInfo
from ggrc.fulltext import Record


class RecordBuilder(object):
  """Basic record builder for full text index table."""
  # pylint: disable=too-few-public-methods

  def __init__(self, tgt_class):
    self._fulltext_attrs = AttributeInfo.gather_attrs(
        tgt_class, '_fulltext_attrs')

  def _get_properties(self, obj):
    """Get indexable properties and values."""
    if obj.type == "Snapshot":
      # Snapshots do not have any indexable content. The object content for
      # snapshots is stored in the revision. Snapshots can also be made for
      # different models so we have to get fulltext attrs for the actual child
      # that was snapshotted and get data for those from the revision content.
      tgt_class = getattr(ggrc.models.all_models, obj.child_type, None)
      if not tgt_class:
        return {}
      attrs = AttributeInfo.gather_attrs(tgt_class, '_fulltext_attrs')
      return {attr: obj.revision.content.get(attr) for attr in attrs}

    return {attr: getattr(obj, attr) for attr in self._fulltext_attrs}

  def as_record(self, obj):
    """Generate record representation for an object."""
    # Defaults. These work when the record is not a custom attribute
    properties = self._get_properties(obj)
    record_id = obj.id
    record_type = obj.__class__.__name__

    # Override defaults to index custom attribute values as attributes of the
    # parent object (the CustomAttributable).
    if record_type == "CustomAttributeValue":
      record_id = obj.attributable_id
      record_type = obj.attributable_type
      # The name of the attribute property needs to be unique for each object,
      # the value comes from the custom_attribute_value
      attribute_name = obj.custom_attribute.title

      properties = {}
      if (obj.custom_attribute.attribute_type == "Map:Person" and
              obj.attribute_object_id):
        # Add both name and email for a Map:Person to the index
        properties[attribute_name + ".name"] = obj.attribute_object.name
        properties[attribute_name + ".email"] = obj.attribute_object.email
      else:
        properties[attribute_name] = obj.attribute_value

    return Record(
        # This logic saves custom attribute values as attributes of the object
        # that owns the attribute values. When obj is not a
        # CustomAttributeValue the values are saved directly.
        record_id,
        record_type,
        obj.context_id,
        **properties
    )


def model_is_indexed(tgt_class):
  fulltext_attrs = AttributeInfo.gather_attrs(tgt_class, '_fulltext_attrs')
  return len(fulltext_attrs) > 0


def get_record_builder(obj, builders={}):
  # pylint: disable=dangerous-default-value
  # This default value is used for simple memoization and should be refactored
  # with proper memoization in the future.
  """Get a record builder for a given class."""
  builder = builders.get(obj.__class__.__name__)
  if builder is None:
    builder = RecordBuilder(obj.__class__)
    builders[obj.__class__.__name__] = builder
  return builder


def fts_record_for(obj):
  builder = get_record_builder(obj)
  return builder.as_record(obj)
