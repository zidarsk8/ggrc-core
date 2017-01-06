# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Crate missing snapshot revisions

Create Date: 2017-01-06 01:03:51.499447
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from ggrc.migrations.utils.snapshot_revisions import handle_objects


# revision identifiers, used by Alembic.
revision = '4bbb12265994'
down_revision = '440149c856a2'


def upgrade():
  """Create missing revisions for snapshottable objects."""

  # copy pasted from ggrc.snapshoter.rules.Types.all
  snapshot_objects = sorted([
      "Risk",
      "Threat",
  ])

  handle_objects(snapshot_objects)


def downgrade():
  """Data correction migrations can not be downgraded."""
