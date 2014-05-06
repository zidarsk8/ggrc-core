
"""Add people indexes

Revision ID: 32cd47b9521d
Revises: 2ab3ec6c8f2
Create Date: 2014-05-06 03:20:53.266617

"""

# revision identifiers, used by Alembic.
revision = '32cd47b9521d'
down_revision = '2ab3ec6c8f2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('ix_people_name_email', 'people', ['name', 'email'], unique=False)


def downgrade():
    op.drop_index('ix_people_name_email', table_name='people')
