
"""Add private column to programs table.

Revision ID: 49c670c7d705
Revises: a3afeab3302
Create Date: 2013-12-09 16:44:54.222398

"""

# revision identifiers, used by Alembic.
revision = '49c670c7d705'
down_revision = 'a3afeab3302'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column(
      'programs',
      sa.Column('private', sa.Boolean(), default=False, nullable=False),
      )

def downgrade():
  op.drop_column('programs', 'private')
