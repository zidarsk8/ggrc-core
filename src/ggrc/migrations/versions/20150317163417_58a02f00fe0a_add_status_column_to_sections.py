
"""Add status column to sections

Revision ID: 58a02f00fe0a
Revises: 4ceda387a468
Create Date: 2015-03-17 16:34:17.230962

"""

# revision identifiers, used by Alembic.
revision = '58a02f00fe0a'
down_revision = '4ceda387a468'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column('sections', sa.Column('status', sa.String(length=250), nullable=True) )


def downgrade():
  op.drop_column('sections', 'status')

