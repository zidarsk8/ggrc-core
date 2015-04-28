
"""Remove ProgramDirective table

Revision ID: 3be12e136921
Revises: 57cc398ad417
Create Date: 2015-04-28 15:23:10.503624

"""

# revision identifiers, used by Alembic.
revision = '3be12e136921'
down_revision = '57cc398ad417'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
  sql = """
  INSERT INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT pd.modified_by_id, pd.created_at, pd.updated_at, pd.program_id as source_id,
         'Program' as source_type, pd.directive_id, IFNULL(d.kind,"Policy") as destination_type, pd.context_id
  FROM program_directives as pd JOIN directives as d ON pd.directive_id = d.id;
  """
  op.execute(sql)
  op.drop_table('program_directives')


def downgrade():
  op.create_table('calendar_entries',
  sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
  sa.Column('name', mysql.VARCHAR(length=250), nullable=True),
  sa.Column('calendar_id', mysql.VARCHAR(length=250), nullable=True),
  sa.Column('created_at', mysql.DATETIME(), nullable=True),
  sa.Column('modified_by_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
  sa.Column('updated_at', mysql.DATETIME(), nullable=True),
  sa.Column('context_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
  sa.Column('owner_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
  sa.ForeignKeyConstraint(['context_id'], [u'contexts.id'], name=u'calendar_entries_ibfk_1'),
  sa.ForeignKeyConstraint(['owner_id'], [u'people.id'], name=u'calendar_entries_ibfk_2'),
  sa.PrimaryKeyConstraint('id'),
  mysql_default_charset=u'utf8',
  mysql_engine=u'InnoDB'
  )
