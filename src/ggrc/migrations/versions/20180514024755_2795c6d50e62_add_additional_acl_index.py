# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
add additional acl index

Create Date: 2018-05-14 02:47:55.761097
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name


from alembic import op

# revision identifiers, used by Alembic.
revision = '2795c6d50e62'
down_revision = '3db5f2027c92'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.create_index(
      'ix_person_object',
      'access_control_list',
      ['person_id', 'object_type', 'object_id'],
      unique=False,
  )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_index('ix_person_object', table_name='access_control_list')
