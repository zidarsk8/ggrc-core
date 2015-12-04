
"""Comment assignee type

Revision ID: 504f541411a5
Revises: 18cbdd3a7fd9
Create Date: 2015-12-04 13:57:07.047217

"""

# revision identifiers, used by Alembic.
revision = '504f541411a5'
down_revision = '18cbdd3a7fd9'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column(
      "comments",
      sa.Column("assignee_type", sa.Text(), nullable=True)
  )


def downgrade():
  op.drop_column("comments", "assignee_type")
