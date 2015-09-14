# Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
# Unauthorized use, copying, distribution, displaying, or public performance
# of this file, via any medium, is strictly prohibited. All information
# contained herein is proprietary and confidential and may not be shared
# with any third party without the express written consent of Reciprocity, Inc.
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Add threat_actors table

Revision ID: 5ada65dc60b3
Revises: 5aa58c3b1867
Create Date: 2014-09-21 08:10:59.441988

"""

# revision identifiers, used by Alembic.
revision = '5ada65dc60b3'
down_revision = '5aa58c3b1867'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.create_table('threat_actors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('slug', sa.String(length=250), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('context_id', sa.Integer(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=250), nullable=True),
    sa.Column('reference_url', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
  )


def downgrade():
  op.drop_table('threat_actors')
