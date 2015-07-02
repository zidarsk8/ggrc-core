# Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
# Unauthorized use, copying, distribution, displaying, or public performance
# of this file, via any medium, is strictly prohibited. All information
# contained herein is proprietary and confidential and may not be shared
# with any third party without the express written consent of Reciprocity, Inc.
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Required Risk fields.

Revision ID: dca3c8d9d68
Revises: 5ab2b76012a6
Create Date: 2014-07-24 19:12:25.208137

"""

# revision identifiers, used by Alembic.
revision = 'dca3c8d9d68'
down_revision = '5ab2b76012a6'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('risks', sa.Column('contact_id', sa.Integer(), nullable=True))
    op.add_column('risks', sa.Column('description', sa.Text(), nullable=False))


def downgrade():
    op.drop_column('risks', 'description')
    op.drop_column('risks', 'contact_id')
