# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""SQL routines for full-text indexing."""

from ggrc import db
from ggrc.fulltext import Indexer


class SqlIndexer(Indexer):
  """SqlIndexer class."""

  def records_generator(self, record):
    """Record generator method."""
    for prop, value in record.properties.items():
      for subproperty, content in value.items():
        if content is not None:
          yield self.record_type(
              key=record.key,
              type=record.type,
              context_id=record.context_id,
              tags=record.tags,
              property=prop,
              subproperty=unicode(subproperty),
              content=unicode(content),
          )

  def create_record(self, record, commit=True):
    """Create records in db."""
    for db_record in self.records_generator(record):
      db.session.add(db_record)
    if commit:
      db.session.commit()

  def update_record(self, record, commit=True):
    """Update records values in db."""
    # remove the obsolete index entries
    if record.properties:
      db.session.query(self.record_type).filter(
          self.record_type.key == record.key,
          self.record_type.type == record.type,
          self.record_type.property.in_(list(record.properties.keys())),
      ).delete(synchronize_session="fetch")
    # add new index entries
    self.create_record(record, commit=commit)

  def delete_record(self, key, type, commit=True):
    """Delete records values in db for specific types."""
    db.session.query(self.record_type).filter(
        self.record_type.key == key,
        self.record_type.type == type).delete()
    if commit:
      db.session.commit()

  def delete_records_by_ids(self, type, keys, commit=True):
    """Method to delete all records related to type and keys."""
    if not keys:
      return
    db.session.query(
        self.record_type
    ).filter(
        self.record_type.key.in_(keys),
        self.record_type.type == type,
    ).delete(
        synchronize_session="fetch"
    )
    if commit:
      db.session.commit()

  def delete_all_records(self, commit=True):
    """Clear index table."""
    db.session.query(self.record_type).delete()
    if commit:
      db.session.commit()

  def delete_records_by_type(self, type, commit=True):
    """Delete values from index table for selected type."""
    db.session.query(self.record_type).filter(
        self.record_type.type == type).delete()
    if commit:
      db.session.commit()
