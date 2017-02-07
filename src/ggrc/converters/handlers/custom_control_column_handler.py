# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Handler for imports and exports snapshoted control instances."""

from ggrc.converters import errors
from ggrc.converters.handlers import snapshot_instance_column_handler


class CustomControlSnapshotInstanceColumnHandler(
        snapshot_instance_column_handler.SnapshotInstanceColumnHandler):
  """Custom Control Column Handler

  return instances that mapped only over snapshot instance
  """

  def is_valid_creation(self, to_append_ids):
    "return True if data valid else False"
    if not to_append_ids:
      return True
    pool_ids = {i.child_id for i in self.audit_object_pool_query.all()}
    if to_append_ids - pool_ids:
      self.add_error(errors.ILLIGAL_APPEND_CONTROL_VALUE,
                     column_name=self.display_name)
      return False
    return True

  def is_valid_delete(self, to_delete_ids):
    "return True if data valid else False"
    if self.unmap:
      self.add_error(errors.INVALID_TO_UNMAP,
                     column_name=self.display_name)
    if to_delete_ids:
      self.add_error(errors.ILLIGAL_REMOVE_CONTROL_VALUE,
                     column_name=self.display_name)
    return not to_delete_ids

  def parse_item(self, *args, **kwargs):
    "parse items and make validation"
    item = super(
        CustomControlSnapshotInstanceColumnHandler, self
    ).parse_item(
        *args, **kwargs
    )
    exists_ids = {i for i, in self.snapshoted_instances_query.values("id")}
    import_ids = {i.id for i in item or []}
    to_delete_ids = exists_ids - import_ids
    to_append_ids = import_ids - exists_ids
    valid_append = self.is_valid_creation(to_append_ids)
    valid_delete = self.is_valid_delete(to_delete_ids)
    if not valid_append or not valid_delete:
      return None
    return item
