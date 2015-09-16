# Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
# Unauthorized use, copying, distribution, displaying, or public performance
# of this file, via any medium, is strictly prohibited. All information
# contained herein is proprietary and confidential and may not be shared
# with any third party without the express written consent of Reciprocity, Inc.
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""add missing columns to risks

Revision ID: 44d5969c897b
Revises: 1347acbb4dc2
Create Date: 2014-11-28 18:59:52.290005

"""

# revision identifiers, used by Alembic.
revision = '44d5969c897b'
down_revision = '1347acbb4dc2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('risks', sa.Column('start_date', sa.Date(), nullable=True))
    op.add_column('risks', sa.Column('end_date', sa.Date(), nullable=True))
    op.add_column('risks', sa.Column('status', sa.String(length=250), nullable=True))


def downgrade():
    op.drop_column('risks', 'start_date')
    op.drop_column('risks', 'end_date')
    op.drop_column('risks', 'status')
