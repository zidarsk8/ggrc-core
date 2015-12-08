# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Add Control Assessments

Revision ID: 1f7d8208aff2
Revises: 5254f4f31427
Create Date: 2015-02-27 14:32:59.757944

"""

# revision identifiers, used by Alembic.
revision = '1f7d8208aff2'
down_revision = '58a02f00fe0a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'control_assessments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('design', sa.String(length=250), nullable=True),
        sa.Column('operationally', sa.String(length=250), nullable=True),
        sa.Column('os_state', sa.String(length=250), nullable=False),
        sa.Column('test_plan', sa.Text(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=250), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('url', sa.String(length=250), nullable=True),
        sa.Column('reference_url', sa.String(length=250), nullable=True),
        sa.Column('secondary_contact_id', sa.Integer(), nullable=True),
        sa.Column('contact_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=250), nullable=False),
        sa.Column('slug', sa.String(length=250), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('modified_by_id', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('context_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['contact_id'], ['people.id'], ),
        sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], ),
        sa.ForeignKeyConstraint(['secondary_contact_id'], ['people.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug', name='uq_control_assessments'),
        sa.UniqueConstraint('title', name='uq_t_control_assessments')
    )


def downgrade():
    op.drop_table('control_assessments')
