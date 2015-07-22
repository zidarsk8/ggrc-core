# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Remove Request.auditor_contact

Revision ID: 58da8a74882c
Revises: 49c670c7d705
Create Date: 2013-12-24 18:24:48.090735

"""

# revision identifiers, used by Alembic.
revision = '58da8a74882c'
down_revision = '49c670c7d705'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('requests', u'auditor_contact')


def downgrade():
    op.add_column(
        'requests',
        sa.Column(u'auditor_contact', sa.String(length=250), nullable=True))
