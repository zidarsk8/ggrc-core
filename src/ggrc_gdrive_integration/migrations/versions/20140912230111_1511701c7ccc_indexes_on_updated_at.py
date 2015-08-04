# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Indexes on updated_at

Revision ID: 1511701c7ccc
Revises: 1efacad0fff5
Create Date: 2014-09-12 23:01:11.835722

"""

# revision identifiers, used by Alembic.
revision = '1511701c7ccc'
down_revision = '1efacad0fff5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('ix_object_events_updated_at', 'object_events', ['updated_at'], unique=False)
    op.create_index('ix_object_files_updated_at', 'object_files', ['updated_at'], unique=False)
    op.create_index('ix_object_folders_updated_at', 'object_folders', ['updated_at'], unique=False)


def downgrade():
    op.drop_index('ix_object_folders_updated_at', table_name='object_folders')
    op.drop_index('ix_object_files_updated_at', table_name='object_files')
    op.drop_index('ix_object_events_updated_at', table_name='object_events')
