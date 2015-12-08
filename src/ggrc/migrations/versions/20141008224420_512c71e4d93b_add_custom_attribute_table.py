# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""add custom attribute table

Revision ID: 512c71e4d93b
Revises: 3a4ce23d81b0
Create Date: 2014-10-08 22:44:20.424247

"""

# revision identifiers, used by Alembic.
revision = '512c71e4d93b'
down_revision = '36950678299f'

from alembic import op
import sqlalchemy as sa

def upgrade():
  op.create_table(
    'custom_attribute_definitions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.Column('context_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('helptext', sa.String(length=250), nullable=False),
    sa.Column('placeholder', sa.String(length=250), nullable=True),
    sa.Column('definition_type', sa.String(length=250), nullable=False),
    sa.Column('attribute_type', sa.String(length=250), nullable=False),
    sa.Column('multi_choice_options', sa.Text(), nullable=True),
    sa.Column('mandatory', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
  )
  op.create_index('ix_custom_attributes_title', 'custom_attribute_definitions', ['title'], unique=False)

  op.create_table(
    'custom_attribute_values',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.Column('context_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('custom_attribute_id', sa.Integer(), nullable=False),
    sa.Column('attributable_id', sa.Integer(), nullable=True),
    sa.Column('attributable_type', sa.String(length=250), nullable=True),
    sa.Column('attribute_value', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['custom_attribute_id'], ['custom_attribute_definitions.id'], ),
    sa.PrimaryKeyConstraint('id')
  )
  op.create_index('ix_custom_attributes_attributable', 'custom_attribute_values', ['attributable_id', 'attributable_type'], unique=False)

def downgrade():
  op.drop_constraint('custom_attribute_values_ibfk_1', 'custom_attribute_values', type_='foreignkey')
  op.drop_table('custom_attribute_definitions')
  op.drop_table('custom_attribute_values')
