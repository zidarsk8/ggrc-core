# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""add vendor table

Revision ID: 5156e813935f
Revises: 3a4ce23d81b0
Create Date: 2014-10-07 21:53:49.969285

"""

# revision identifiers, used by Alembic.
revision = '5156e813935f'
down_revision = 'd47d1285cf5'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
      'vendors',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('description', sa.Text(), nullable=True),
      sa.Column('url', sa.String(length=250), nullable=True),
      sa.Column('start_date', sa.DateTime(), nullable=True),
      sa.Column('end_date', sa.DateTime(), nullable=True),
      sa.Column('slug', sa.String(length=250), nullable=False),
      sa.Column('title', sa.String(length=250), nullable=False),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.Column('contact_id', sa.Integer(), nullable=True),
      sa.Column('notes', sa.Text(), nullable=True),
      sa.Column('status', sa.String(length=250), nullable=False),
      sa.Column('reference_url', sa.String(length=250), nullable=False),
      sa.PrimaryKeyConstraint('id')
    )
    op.create_index('fk_vendors_context', 'vendors', ['context_id'], unique=False)
    op.create_index('fk_vendors_contact', 'vendors', ['contact_id'], unique=False)
    op.create_index('fk_vendors_modified_by', 'vendors', ['modified_by_id'], unique=False)
    op.create_index('fk_vendors_status', 'vendors', ['status'], unique=False)
    op.create_unique_constraint('uq_vendors_title', 'vendors', ['title'])
    op.create_index('ix_vendors_updated_at', 'vendors', ['updated_at'], unique=False)

def downgrade():
    op.drop_table('vendors')
