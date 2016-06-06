
"""Rename admin role from gGRC Admin to Administrator.

Revision ID: c9218e757bc
Revises: 3bf028a83e79
Create Date: 2016-06-03 12:02:09.438599

"""

# revision identifiers, used by Alembic.
revision = 'c9218e757bc'
down_revision = '3bf028a83e79'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

roles_table = table(
  'roles',
  column('id', sa.Integer),
  column('name', sa.String),
  column('updated_at', sa.DateTime),
  column('description', sa.Text),
)


def upgrade():
  op.execute(roles_table.update()
             .where(roles_table.c.name == 'gGRC Admin')
             .values(name='Administrator',
                     description='System Administrator with super-user '
                                 'privileges'))


def downgrade():
  op.execute(roles_table.update()
             .where(roles_table.c.name == 'Administrator')
             .values(name='gGRC Admin',
                     description='gGRC System Administrator with super-user '
                                 'privileges'))
