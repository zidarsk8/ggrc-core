# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add automappings table

Create Date: 2017-07-10 09:26:21.778041
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '2ada007df3ee'
down_revision = '436dc4cea0f3'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  # Rename automapping_id to parent_id
  op.drop_constraint(
      'relationships_automapping_parent', 'relationships', type_='foreignkey')
  op.alter_column(
      'relationships',
      'automapping_id',
      existing_type=sa.Integer(),
      new_column_name='parent_id')
  op.create_foreign_key(
      "fk_relationships_parent_id",
      "relationships", "relationships",
      ["parent_id"], ["id"],
      ondelete='SET NULL')


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  # Rename parent id to automapping id
  op.drop_constraint(
      'fk_relationship_parent_id', 'relationships', type_='foreignkey')
  op.alter_column(
      'relationships',
      'parent_id',
      existing_type=sa.Integer(),
      new_column_name='automapping_id')
  op.create_foreign_key(
      "relationships_automapping_parent",
      "relationships", "relationships",
      ["automapping_id"], ["id"],
      ondelete='SET NULL')
