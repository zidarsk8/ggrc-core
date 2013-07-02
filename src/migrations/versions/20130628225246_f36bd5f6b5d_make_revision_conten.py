"""Make revision.content TEXT

Revision ID: 2a59bef8c738
Revises: f36bd5f6b5d
Create Date: 2013-06-28 22:52:46.373691

"""

# revision identifiers, used by Alembic.
revision = '2a59bef8c738'
down_revision = 'f36bd5f6b5d'
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.alter_column('revisions', u'content',
               existing_type=sa.TEXT,
               nullable=False)


def downgrade():
    op.alter_column('revisions', u'content',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
