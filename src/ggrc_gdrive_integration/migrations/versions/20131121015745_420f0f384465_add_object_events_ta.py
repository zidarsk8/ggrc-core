# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Add object_events table

Revision ID: 420f0f384465
Revises: 126a93430a9e
Create Date: 2013-11-21 01:57:45.035753

"""

# revision identifiers, used by Alembic.
revision = '420f0f384465'
down_revision = '126a93430a9e'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.create_table('object_events',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('permissions_json', sa.Text(), nullable=False),
    sa.Column('modified_by_id', sa.Integer()),
    sa.Column(
      'created_at', sa.DateTime(), default=sa.text('current_timestamp')),
    sa.Column(
      'updated_at',
      sa.DateTime(),
      default=sa.text('current_timestamp'),
      onupdate=sa.text('current_timestamp')),
    sa.Column('context_id', sa.Integer()),
    sa.Column('calendar_id', sa.String(length=250), nullable=True),
    sa.Column('event_id', sa.String(length=250), nullable=False),
    sa.Column('eventable_id', sa.Integer(), nullable=False),
    sa.Column('eventable_type', sa.String(length=250), nullable=False),
    )


def downgrade():
  op.drop_table('object_events')
