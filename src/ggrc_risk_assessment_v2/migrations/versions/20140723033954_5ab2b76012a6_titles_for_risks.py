# Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
# Unauthorized use, copying, distribution, displaying, or public performance
# of this file, via any medium, is strictly prohibited. All information
# contained herein is proprietary and confidential and may not be shared
# with any third party without the express written consent of Reciprocity, Inc.
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Titles for Risks.

Revision ID: 5ab2b76012a6
Revises: 113eb68585b7
Create Date: 2014-07-23 03:39:54.105011

"""

# revision identifiers, used by Alembic.
revision = '5ab2b76012a6'
down_revision = '113eb68585b7'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('risks', sa.Column('title', sa.String(length=250), nullable=False))
    op.create_unique_constraint('uq_t_risks', 'risks', ['title'])


def downgrade():
    op.drop_column('risks', 'title')
