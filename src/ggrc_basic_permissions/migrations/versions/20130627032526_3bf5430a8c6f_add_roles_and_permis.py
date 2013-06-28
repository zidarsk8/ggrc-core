# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

"""Add roles and permissions tables

Revision ID: 3bf5430a8c6f
Revises: None
Create Date: 2013-06-27 03:25:26.571232

"""

# revision identifiers, used by Alembic.
revision = '3bf5430a8c6f'
down_revision = None

from alembic import op
import sqlalchemy as sa

def upgrade():
  op.create_table('roles',
    sa.Column('name', sa.String(length=128), nullable=False, primary_key=True),
    sa.Column('description', sa.Text(), nullable=True),
    )
  op.create_table('roles_permissions',
    sa.Column('role_name', sa.String(length=128), nullable=False),
    sa.Column('permission', sa.String(length=6), nullable=False),
    sa.Column('resource_type', sa.String(length=128), nullable=False),
    sa.Column('context_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint(
      'role_name', 'permission', 'resource_type', 'context_id',),
    sa.ForeignKeyConstraint('role_name', 'roles.name'),
    )
  op.create_table('users_roles',
    sa.Column('role_name', sa.String(length=128), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('role_name', 'user_id'),
    sa.ForeignKeyConstraint('role_name', 'roles.name'),
    )

def downgrade():
  op.drop_table('users_roles')
  op.drop_table('roles_permissions')
  op.drop_table('roles')

