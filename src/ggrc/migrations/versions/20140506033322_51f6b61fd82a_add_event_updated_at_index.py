# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Add Event.updated_at index

Revision ID: 51f6b61fd82a
Revises: 32cd47b9521d
Create Date: 2014-05-06 03:33:22.548771

"""

# revision identifiers, used by Alembic.
revision = '51f6b61fd82a'
down_revision = '32cd47b9521d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('ix_events_updated_at', 'events', ['updated_at'], unique=False)


def downgrade():
    op.drop_index('ix_events_updated_at', table_name='events')
