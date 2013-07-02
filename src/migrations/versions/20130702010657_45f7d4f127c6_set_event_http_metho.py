"""Set event.http_method to enum

Revision ID: 45f7d4f127c6
Revises: 2124bf6f0f9e
Create Date: 2013-07-02 01:06:57.460889

"""

# revision identifiers, used by Alembic.
revision = '45f7d4f127c6'
down_revision = '2124bf6f0f9e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('events', 'http_method', 
        type_ = sa.Enum(u'POST', u'PUT', u'DELETE'),
        existing_type = sa.VARCHAR(length=250),
        nullable = False
    )



def downgrade():
    op.alter_column('events', 'http_method', 
        type_ = sa.VARCHAR(length=250),
        existing_type = sa.Enum(u'POST', u'PUT', u'DELETE'),
        nullable = False
    )
