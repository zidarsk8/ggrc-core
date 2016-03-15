# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""
Add definition_id to custom attribute definitions

Create Date: 2016-03-14 15:50:56.407589
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from alembic import op

# revision identifiers, used by Alembic.
revision = '39aec99639d5'
down_revision = '204540106539'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.add_column('custom_attribute_definitions',
                sa.Column('definition_id', sa.Integer(), nullable=True))
  op.alter_column('custom_attribute_definitions', 'helptext',
                  existing_type=mysql.VARCHAR(length=250), nullable=True)
  op.create_index('ix_custom_attributes_definition',
                  'custom_attribute_definitions',
                  ['definition_type', 'definition_id'], unique=False)
  op.drop_constraint(u'uq_custom_attribute',
                     'custom_attribute_definitions', type_='unique')
  op.create_unique_constraint('uq_custom_attribute',
                              'custom_attribute_definitions',
                              ['title', 'definition_type', 'definition_id'])


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_constraint('uq_custom_attribute',
                     'custom_attribute_definitions', type_='unique')
  op.create_unique_constraint(u'uq_custom_attribute',
                              'custom_attribute_definitions',
                              ['title', 'definition_type'])
  op.drop_index('ix_custom_attributes_definition',
                table_name='custom_attribute_definitions')
  op.alter_column('custom_attribute_definitions', 'helptext',
                  existing_type=mysql.VARCHAR(length=250),
                  nullable=False)
  op.drop_column('custom_attribute_definitions', 'definition_id')
