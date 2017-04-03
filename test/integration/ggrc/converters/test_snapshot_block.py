# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for Snapshot block converter class."""

import mock

from sqlalchemy import func
from sqlalchemy.sql.expression import tuple_

from ggrc import db
from ggrc import models
from ggrc.converters.snapshot_block import SnapshotBlockConverter
from integration.ggrc import TestCase
from integration.ggrc.models import factories


class TestSnapshotBlockConverter(TestCase):
  """Tests for Snapshot block converter."""
  # Removing protected access checks because we wish to tests even the
  # protected functions.
  # pylint: disable=protected-access

  @staticmethod
  def _get_latest_object_revisions(objects):
    """Get latest revisions of given objects."""
    object_tuples = [(o.id, o.type) for o in objects]
    revisions = models.Revision.query.filter(
        models.Revision.id.in_(
            db.session.query(func.max(models.Revision.id)).filter(
                tuple_(
                    models.Revision.resource_id,
                    models.Revision.resource_type,
                ).in_(object_tuples)
            ).group_by(
                models.Revision.resource_type,
                models.Revision.resource_id,
            )
        )
    )
    return revisions

  def _create_snapshots(self, objects):
    """Create snapshots of latest object revisions for given objects."""
    revisions = self._get_latest_object_revisions(objects)
    audit = factories.AuditFactory()
    snapshots = [
        factories.SnapshotFactory(
            child_id=revision.resource_id,
            child_type=revision.resource_type,
            revision=revision,
            parent=audit,
        )
        for revision in revisions
    ]
    return snapshots

  def test_empty_snapshots(self):
    """Test snapshots property for empty ids list."""
    converter = mock.MagicMock()
    block = SnapshotBlockConverter(converter, [])
    self.assertEqual(block.snapshots, [])

  def test_snapshots_property(self):
    """Test snapshots property and snapshot content."""
    snapshots = self._create_snapshots([factories.ControlFactory()])

    converter = mock.MagicMock()
    ids = [s.id for s in snapshots]
    block = SnapshotBlockConverter(converter, ids)
    self.assertEqual(block.snapshots, snapshots)
    for snapshot in snapshots:
      self.assertIn("audit", snapshot.revision.content)

  def test_valid_child_types(self):
    """Test child_type property with valid snapshots list."""
    snapshots = self._create_snapshots([
        factories.ControlFactory(),
        factories.ControlFactory(),
    ])
    converter = mock.MagicMock()
    ids = [s.id for s in snapshots]
    block = SnapshotBlockConverter(converter, ids)
    self.assertEqual(block.child_type, "Control")

  def test_empty_child_type(self):
    """Test child_type property with empty snapshots list."""
    converter = mock.MagicMock()
    block = SnapshotBlockConverter(converter, [])
    self.assertEqual(block.child_type, "")

  def test_invalid_child_types(self):
    """Test child_type property with invalid snapshots list."""
    snapshots = self._create_snapshots([
        factories.ControlFactory(),
        factories.PolicyFactory(),
    ])
    converter = mock.MagicMock()
    ids = [s.id for s in snapshots]
    block = SnapshotBlockConverter(converter, ids)
    with self.assertRaises(AssertionError):
      block.child_type = block.child_type

  def test_attribute_name_map(self):
    """Test Control snapshot name map and order."""
    converter = mock.MagicMock()
    block = SnapshotBlockConverter(converter, [])
    block.child_type = "Control"
    self.assertEqual(
        block._attribute_name_map.items(),
        [
            ('slug', 'Code'),
            ('audit', 'Audit'),  # inserted attribute
            ('title', 'Title'),
            ('description', 'Description'),
            ('notes', 'Notes'),
            ('test_plan', 'Test Plan'),
            ('owners', 'Admin'),
            ('start_date', 'Effective Date'),
            ('end_date', 'Stop Date'),
            ('status', 'State'),
            ('os_state', 'Review State'),
            ('assertions', 'Assertions'),
            ('categories', 'Categories'),
            ('contact', 'Primary Contact'),
            ('fraud_related', 'Fraud Related'),
            ('key_control', 'Significance'),
            ('kind', 'Kind/Nature'),
            ('means', 'Type/Means'),
            ('principal_assessor', 'Principal Assignee'),
            ('secondary_assessor', 'Secondary Assignee'),
            ('secondary_contact', 'Secondary Contact'),
            ('url', 'Control URL'),
            ('reference_url', 'Reference URL'),
            ('verify_frequency', 'Frequency'),
            ('created_at', 'Created On'),
            ('updated_at', 'Last Updated')
        ]
    )
