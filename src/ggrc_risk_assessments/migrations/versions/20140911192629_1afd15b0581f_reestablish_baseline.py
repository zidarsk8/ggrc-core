# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Reestablish baseline

Revision ID: 1afd15b0581f
Revises: 51f2bcff9bcd
Create Date: 2014-09-11 19:26:29.182755

"""

# revision identifiers, used by Alembic.
revision = '1afd15b0581f'
down_revision = '51f2bcff9bcd'

from alembic import op


def upgrade():
    op.create_index('fk_risk_assessments_contexts', 'risk_assessments', ['context_id'], unique=False)


def downgrade():
    op.drop_index('fk_risk_assessments_contexts', table_name='risk_assessments')
