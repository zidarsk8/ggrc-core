# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Add some more indexes

Revision ID: 16d7c239e894
Revises: 46fe552ca250
Create Date: 2014-04-30 06:42:51.739844

"""

# revision identifiers, used by Alembic.
revision = '16d7c239e894'
down_revision = '46fe552ca250'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('ix_controls_principal_assessor', 'controls', ['principal_assessor_id'], unique=False)
    op.create_index('ix_controls_secondary_assessor', 'controls', ['secondary_assessor_id'], unique=False)


def downgrade():
    op.drop_index('ix_controls_secondary_assessor', table_name='controls')
    op.drop_index('ix_controls_principal_assessor', table_name='controls')
